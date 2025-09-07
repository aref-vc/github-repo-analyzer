"""
GitHub API Client for Repository Analysis
Handles all GitHub API interactions with rate limiting and error handling
"""

import requests
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import time
from urllib.parse import urlparse
import base64

class GitHubAnalyzer:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        
        # Set up authentication headers
        if self.token:
            self.session.headers.update({
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "GitHub-Repo-Analyzer/1.0"
            })
    
    def _make_request(self, endpoint: str, params: Dict = None, timeout: int = 10) -> Dict[str, Any]:
        """Make authenticated request to GitHub API with rate limiting and error boundaries"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params or {}, timeout=timeout)
            
            # Handle rate limiting
            if response.status_code == 403:
                if "rate limit" in response.text.lower():
                    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                    remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
                    
                    if remaining == 0:
                        sleep_time = max(0, reset_time - int(time.time()) + 1)
                        print(f"⚠️ Rate limit reached. Waiting {sleep_time} seconds...")
                        
                        # If wait is too long, return degraded response
                        if sleep_time > 60:
                            print(f"⚠️ Rate limit wait too long ({sleep_time}s), returning partial data")
                            return {"error": "rate_limited", "partial": True}
                        
                        time.sleep(sleep_time)
                        response = self.session.get(url, params=params or {}, timeout=timeout)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            print(f"⚠️ Request timeout for {endpoint}, returning empty result")
            return {"error": "timeout", "partial": True}
        except requests.exceptions.RequestException as e:
            print(f"⚠️ API request failed for {endpoint}: {str(e)}")
            return {"error": str(e), "partial": True}
    
    def parse_repo_url(self, repo_url: str) -> tuple[str, str]:
        """Extract owner and repo name from GitHub URL"""
        # Handle different URL formats
        if repo_url.startswith("http"):
            parsed = urlparse(repo_url)
            path_parts = parsed.path.strip("/").split("/")
            if len(path_parts) >= 2:
                return path_parts[0], path_parts[1]
        else:
            # Handle "owner/repo" format
            parts = repo_url.split("/")
            if len(parts) == 2:
                return parts[0], parts[1]
        
        raise ValueError(f"Invalid GitHub repository URL: {repo_url}")
    
    def get_repository_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get basic repository information with error handling"""
        endpoint = f"repos/{owner}/{repo}"
        result = self._make_request(endpoint)
        
        # Return default structure if error
        if result.get("error"):
            return {
                "name": repo,
                "owner": {"login": owner},
                "description": "Unable to fetch description",
                "stargazers_count": 0,
                "forks_count": 0,
                "open_issues_count": 0,
                "size": 0,
                "default_branch": "main",
                "partial": True
            }
        return result
    
    def get_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """Get repository language composition"""
        endpoint = f"repos/{owner}/{repo}/languages"
        return self._make_request(endpoint)
    
    def get_contributors(self, owner: str, repo: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get repository contributors"""
        endpoint = f"repos/{owner}/{repo}/contributors"
        params = {"per_page": min(limit, 100)}
        return self._make_request(endpoint, params)
    
    def get_commits(self, owner: str, repo: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent commits"""
        endpoint = f"repos/{owner}/{repo}/commits"
        params = {"per_page": min(limit, 100)}
        return self._make_request(endpoint, params)
    
    def get_releases(self, owner: str, repo: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get repository releases"""
        endpoint = f"repos/{owner}/{repo}/releases"
        params = {"per_page": min(limit, 100)}
        try:
            return self._make_request(endpoint, params)
        except:
            return []  # Some repos don't have releases
    
    def get_issues(self, owner: str, repo: str, state: str = "all", limit: int = 100) -> List[Dict[str, Any]]:
        """Get repository issues and pull requests"""
        endpoint = f"repos/{owner}/{repo}/issues"
        params = {"state": state, "per_page": min(limit, 100)}
        return self._make_request(endpoint, params)
    
    def get_pull_requests(self, owner: str, repo: str, state: str = "all", limit: int = 100) -> List[Dict[str, Any]]:
        """Get repository pull requests"""
        endpoint = f"repos/{owner}/{repo}/pulls"
        params = {"state": state, "per_page": min(limit, 100)}
        return self._make_request(endpoint, params)
    
    def get_readme(self, owner: str, repo: str) -> Optional[str]:
        """Get repository README content"""
        endpoint = f"repos/{owner}/{repo}/readme"
        try:
            readme_data = self._make_request(endpoint)
            # Decode base64 content
            if readme_data.get("encoding") == "base64":
                content = base64.b64decode(readme_data["content"]).decode("utf-8")
                return content
            return readme_data.get("content", "")
        except:
            return None
    
    def get_package_json(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Get package.json for Node.js projects"""
        endpoint = f"repos/{owner}/{repo}/contents/package.json"
        try:
            file_data = self._make_request(endpoint)
            if file_data.get("encoding") == "base64":
                content = base64.b64decode(file_data["content"]).decode("utf-8")
                import json
                return json.loads(content)
            return None
        except:
            return None
    
    def get_requirements_txt(self, owner: str, repo: str) -> Optional[str]:
        """Get requirements.txt for Python projects"""
        endpoint = f"repos/{owner}/{repo}/contents/requirements.txt"
        try:
            file_data = self._make_request(endpoint)
            if file_data.get("encoding") == "base64":
                content = base64.b64decode(file_data["content"]).decode("utf-8")
                return content
            return None
        except:
            return None
    
    def search_files(self, owner: str, repo: str, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for files in repository"""
        endpoint = "search/code"
        params = {
            "q": f"{query} repo:{owner}/{repo}",
            "per_page": min(limit, 100)
        }
        try:
            result = self._make_request(endpoint, params)
            return result.get("items", [])
        except:
            return []
    
    def get_workflow_runs(self, owner: str, repo: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get GitHub Actions workflow runs"""
        endpoint = f"repos/{owner}/{repo}/actions/runs"
        params = {"per_page": min(limit, 100)}
        try:
            result = self._make_request(endpoint, params)
            return result.get("workflow_runs", [])
        except:
            return []
    
    def check_rate_limit(self) -> Dict[str, Any]:
        """Check current rate limit status"""
        endpoint = "rate_limit"
        return self._make_request(endpoint)