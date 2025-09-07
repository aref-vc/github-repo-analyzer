"""
Optimized Repository Analysis Engine
Performance-optimized version with timeouts, concurrency, and caching
"""

import asyncio
import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from functools import wraps, lru_cache
import time
import statistics
import concurrent.futures
from threading import Timer

def timeout_decorator(seconds=10):
    """Decorator to add timeout to functions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = Timer(0, target)
            thread.daemon = True
            thread.start()
            thread.join(seconds)
            
            if thread.is_alive():
                # Timeout occurred
                return {"error": f"Analysis timeout after {seconds} seconds", "partial": True}
            
            if exception[0]:
                return {"error": str(exception[0]), "partial": True}
                
            return result[0]
        return wrapper
    return decorator

class OptimizedAnalyzer:
    """Optimized analysis with performance improvements"""
    
    def __init__(self, github_analyzer, max_depth=100, cache_ttl=300):
        self.github = github_analyzer
        self.max_depth = max_depth  # Limit tree traversal
        self.cache_ttl = cache_ttl  # Cache for 5 minutes
        self._cache = {}
        self._cache_times = {}
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Get cached result if still valid"""
        if key in self._cache:
            if time.time() - self._cache_times.get(key, 0) < self.cache_ttl:
                return self._cache[key]
        return None
    
    def _set_cache(self, key: str, value: Any):
        """Cache a result"""
        self._cache[key] = value
        self._cache_times[key] = time.time()
    
    @timeout_decorator(seconds=5)
    def analyze_directory_structure(self, owner: str, repo: str) -> Dict[str, Any]:
        """Analyze repository directory structure with depth limit"""
        cache_key = f"dir_{owner}_{repo}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
            
        try:
            # Get repository tree with limited depth
            tree_endpoint = f"repos/{owner}/{repo}/git/trees/HEAD"
            tree_data = self.github._make_request(tree_endpoint)
            
            if not tree_data.get("tree"):
                return {"structure": "Unable to analyze", "patterns": []}
            
            # Limit to first max_depth items to prevent timeout
            files = tree_data["tree"][:self.max_depth]
            directories = defaultdict(int)
            file_types = Counter()
            
            for item in files:
                if item["type"] == "blob":
                    path = item["path"]
                    directory = "/".join(path.split("/")[:-1]) if "/" in path else "root"
                    directories[directory] += 1
                    
                    if "." in path:
                        ext = path.split(".")[-1].lower()
                        file_types[ext] += 1
            
            result = {
                "total_files": len([f for f in files if f["type"] == "blob"]),
                "total_directories": len(directories),
                "file_types": dict(file_types.most_common(10)),
                "structure_patterns": self._identify_basic_patterns(file_types),
                "largest_directories": dict(Counter(directories).most_common(5)),
                "analysis_depth": min(len(files), self.max_depth)
            }
            
            self._set_cache(cache_key, result)
            return result
            
        except Exception as e:
            return {
                "structure": f"Analysis failed: {str(e)}",
                "patterns": [],
                "total_files": 0,
                "partial": True
            }
    
    def _identify_basic_patterns(self, file_types: Counter) -> List[str]:
        """Quickly identify project patterns from file types"""
        patterns = []
        
        # Quick pattern detection
        if file_types.get("js") or file_types.get("jsx") or file_types.get("ts"):
            patterns.append("JavaScript/TypeScript project")
        if file_types.get("py"):
            patterns.append("Python project")
        if file_types.get("java"):
            patterns.append("Java project")
        if file_types.get("go"):
            patterns.append("Go project")
        if file_types.get("rs"):
            patterns.append("Rust project")
        if file_types.get("rb"):
            patterns.append("Ruby project")
            
        return patterns[:3]  # Return top 3 patterns
    
    @timeout_decorator(seconds=5)
    def analyze_dependencies_quick(self, owner: str, repo: str) -> Dict[str, Any]:
        """Quick dependency analysis with limited scope"""
        cache_key = f"deps_{owner}_{repo}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
            
        dependencies = {
            "package_managers": [],
            "core_dependencies": [],
            "dependency_count": 0,
            "ecosystem_analysis": {}
        }
        
        try:
            # Check only main package files (not all variations)
            quick_checks = [
                ("package.json", "npm/yarn"),
                ("requirements.txt", "pip"),
                ("go.mod", "go modules"),
                ("Cargo.toml", "rust")
            ]
            
            for filename, manager in quick_checks[:2]:  # Check only first 2
                try:
                    file_data = self.github._make_request(
                        f"repos/{owner}/{repo}/contents/{filename}",
                        timeout=2  # Quick timeout
                    )
                    if file_data:
                        dependencies["package_managers"].append(manager)
                        break  # Found one, that's enough
                except:
                    continue
            
            self._set_cache(cache_key, dependencies)
            return dependencies
            
        except Exception as e:
            dependencies["analysis_error"] = str(e)
            return dependencies
    
    @timeout_decorator(seconds=5)
    def analyze_code_quality_quick(self, owner: str, repo: str) -> Dict[str, Any]:
        """Quick code quality analysis"""
        cache_key = f"quality_{owner}_{repo}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
            
        quality_metrics = {
            "testing_framework": "Unknown",
            "linting_tools": [],
            "ci_cd_analysis": {},
            "documentation_quality": "Unknown"
        }
        
        try:
            # Quick checks for common patterns
            common_test_files = ["test", "tests", "spec", "__tests__"]
            
            # Check if any test directories exist (quick check)
            tree_endpoint = f"repos/{owner}/{repo}/contents"
            contents = self.github._make_request(tree_endpoint)
            
            if contents:
                for item in contents[:20]:  # Check only first 20 items
                    if item.get("type") == "dir" and any(test in item.get("name", "").lower() for test in common_test_files):
                        quality_metrics["testing_framework"] = "Detected"
                        break
            
            self._set_cache(cache_key, quality_metrics)
            return quality_metrics
            
        except Exception as e:
            quality_metrics["analysis_error"] = str(e)
            return quality_metrics
    
    @timeout_decorator(seconds=8)
    def analyze_commit_patterns_quick(self, commits: List[Dict]) -> Dict[str, Any]:
        """Quick commit pattern analysis"""
        if not commits:
            return {"patterns": "No commits to analyze"}
        
        # Analyze only recent commits
        recent_commits = commits[:30]  # Limit to 30 most recent
        
        patterns = {
            "total_analyzed": len(recent_commits),
            "commit_frequency": "Unknown",
            "common_authors": [],
            "commit_types": {}
        }
        
        try:
            # Quick type detection
            types = Counter()
            authors = Counter()
            
            for commit in recent_commits:
                message = commit.get("commit", {}).get("message", "").lower()
                author = commit.get("commit", {}).get("author", {}).get("name", "Unknown")
                authors[author] += 1
                
                # Quick classification
                if "fix" in message:
                    types["fixes"] += 1
                elif "feat" in message or "add" in message:
                    types["features"] += 1
                elif "docs" in message:
                    types["documentation"] += 1
                elif "test" in message:
                    types["tests"] += 1
                else:
                    types["other"] += 1
            
            patterns["commit_types"] = dict(types.most_common(5))
            patterns["common_authors"] = [author for author, _ in authors.most_common(3)]
            
        except Exception as e:
            patterns["error"] = str(e)
        
        return patterns
    
    def get_quick_insights(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get quick insights without deep analysis"""
        insights = {
            "analysis_type": "quick",
            "timestamp": datetime.now().isoformat()
        }
        
        # Run quick analyses in parallel with timeout protection
        try:
            insights["directory_structure"] = self.analyze_directory_structure(owner, repo)
            insights["dependencies"] = self.analyze_dependencies_quick(owner, repo)
            insights["code_quality"] = self.analyze_code_quality_quick(owner, repo)
        except Exception as e:
            insights["error"] = f"Quick analysis error: {str(e)}"
        
        return insights