"""
Deep Repository Analyzer
Performs comprehensive analysis to fill all TBD fields with real data
"""

import re
import base64
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import statistics

class DeepAnalyzer:
    """Performs deep analysis of repository to extract all insights"""
    
    def __init__(self, github_client):
        self.github = github_client
    
    def analyze_file_tree(self, owner: str, repo: str) -> Dict[str, Any]:
        """Deep analysis of repository file structure"""
        try:
            # Get full tree recursively
            default_branch = self.github.get_repository_info(owner, repo).get("default_branch", "main")
            tree_url = f"repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
            tree_data = self.github._make_request(tree_url)
            
            if not tree_data or "tree" not in tree_data:
                return self._default_tree_analysis()
            
            files = tree_data["tree"]
            
            # Analyze structure
            analysis = {
                "total_files": 0,
                "total_dirs": 0,
                "file_types": Counter(),
                "directory_structure": defaultdict(list),
                "config_files": [],
                "test_files": [],
                "doc_files": [],
                "max_depth": 0
            }
            
            for item in files:
                path = item["path"]
                item_type = item["type"]
                
                if item_type == "blob":
                    analysis["total_files"] += 1
                    
                    # Extract file extension
                    if "." in path:
                        ext = path.split(".")[-1].lower()
                        analysis["file_types"][ext] += 1
                    
                    # Categorize files
                    if any(test in path.lower() for test in ["test", "spec", "__test__"]):
                        analysis["test_files"].append(path)
                    if any(doc in path.lower() for doc in ["readme", "doc", "license", "contributing"]):
                        analysis["doc_files"].append(path)
                    if path.split("/")[-1] in ["package.json", "requirements.txt", "Gemfile", 
                                               "Cargo.toml", "go.mod", "pom.xml", ".env.example",
                                               "Dockerfile", "docker-compose.yml", ".github/workflows"]:
                        analysis["config_files"].append(path)
                    
                    # Track directory structure
                    parts = path.split("/")
                    depth = len(parts) - 1
                    analysis["max_depth"] = max(analysis["max_depth"], depth)
                    
                    if depth > 0:
                        dir_path = "/".join(parts[:-1])
                        analysis["directory_structure"][dir_path].append(parts[-1])
                
                elif item_type == "tree":
                    analysis["total_dirs"] += 1
            
            return analysis
            
        except Exception as e:
            print(f"⚠️ File tree analysis failed: {e}")
            return self._default_tree_analysis()
    
    def _default_tree_analysis(self) -> Dict[str, Any]:
        """Default tree analysis when full analysis fails"""
        return {
            "total_files": 0,
            "total_dirs": 0,
            "file_types": {},
            "directory_structure": {},
            "config_files": [],
            "test_files": [],
            "doc_files": [],
            "max_depth": 0
        }
    
    def detect_architecture_pattern(self, tree_analysis: Dict[str, Any]) -> str:
        """Detect architecture pattern from file structure"""
        dirs = list(tree_analysis["directory_structure"].keys())
        
        # MVC Pattern
        if any("controller" in d.lower() for d in dirs) and \
           any("model" in d.lower() for d in dirs) and \
           any("view" in d.lower() for d in dirs):
            return "MVC (Model-View-Controller)"
        
        # Microservices
        if any("services" in d.lower() for d in dirs) or \
           len([d for d in dirs if "service" in d.lower()]) > 2:
            return "Microservices Architecture"
        
        # Layered Architecture
        if any("domain" in d.lower() for d in dirs) and \
           any("infrastructure" in d.lower() for d in dirs):
            return "Domain-Driven Design (DDD)"
        
        # Component-based (React/Vue/Angular)
        if any("components" in d.lower() for d in dirs) or \
           any("src/components" in d for d in dirs):
            return "Component-Based Architecture"
        
        # API-First
        if any("api" in d.lower() for d in dirs) and \
           any(f for f in tree_analysis.get("config_files", []) if "swagger" in f.lower() or "openapi" in f.lower()):
            return "API-First Architecture"
        
        # Monolithic
        if tree_analysis["max_depth"] < 3 and tree_analysis["total_dirs"] < 10:
            return "Monolithic Architecture"
        
        # Modular
        if any("modules" in d.lower() for d in dirs) or \
           any("packages" in d.lower() for d in dirs):
            return "Modular Architecture"
        
        return "Standard Project Structure"
    
    def analyze_dependencies_detailed(self, owner: str, repo: str) -> Dict[str, Any]:
        """Detailed dependency analysis including versions"""
        deps = {
            "total_count": 0,
            "direct_dependencies": {},
            "dev_dependencies": {},
            "outdated_check": [],
            "security_warnings": [],
            "package_managers": []
        }
        
        # Check package.json for Node.js
        package_json = self.github.get_package_json(owner, repo)
        if package_json:
            deps["package_managers"].append("npm/yarn")
            if "dependencies" in package_json:
                deps["direct_dependencies"]["npm"] = package_json["dependencies"]
                deps["total_count"] += len(package_json["dependencies"])
            if "devDependencies" in package_json:
                deps["dev_dependencies"]["npm"] = package_json["devDependencies"]
                deps["total_count"] += len(package_json["devDependencies"])
            
            # Check for outdated patterns
            for dep, version in deps["direct_dependencies"].get("npm", {}).items():
                if version.startswith("^") or version.startswith("~"):
                    deps["outdated_check"].append(f"{dep}: using flexible versioning ({version})")
        
        # Check requirements.txt for Python
        requirements = self.github.get_requirements_txt(owner, repo)
        if requirements:
            deps["package_managers"].append("pip")
            python_deps = {}
            for line in requirements.split("\n"):
                line = line.strip()
                if line and not line.startswith("#"):
                    if "==" in line:
                        name, version = line.split("==", 1)
                        python_deps[name.strip()] = version.strip()
                    elif ">=" in line or "<=" in line:
                        deps["outdated_check"].append(f"{line}: using flexible versioning")
                    else:
                        python_deps[line] = "*"
            
            deps["direct_dependencies"]["pip"] = python_deps
            deps["total_count"] += len(python_deps)
        
        # Check for other package managers
        files_to_check = [
            ("Gemfile", "bundler"),
            ("Cargo.toml", "cargo"),
            ("go.mod", "go modules"),
            ("pom.xml", "maven"),
            ("build.gradle", "gradle")
        ]
        
        for filename, manager in files_to_check:
            try:
                file_exists = self.github._make_request(f"repos/{owner}/{repo}/contents/{filename}")
                if file_exists and not file_exists.get("error"):
                    deps["package_managers"].append(manager)
            except:
                pass
        
        return deps
    
    def analyze_code_quality_detailed(self, owner: str, repo: str, tree_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Detailed code quality analysis"""
        quality = {
            "test_coverage": "Unknown",
            "test_file_ratio": 0,
            "documentation_coverage": 0,
            "linting_config": [],
            "ci_cd_tools": [],
            "code_review_process": "Unknown",
            "branch_protection": False
        }
        
        # Calculate test coverage estimate
        total_files = tree_analysis["total_files"]
        test_files = len(tree_analysis["test_files"])
        
        if total_files > 0:
            quality["test_file_ratio"] = round((test_files / total_files) * 100, 1)
            if quality["test_file_ratio"] > 30:
                quality["test_coverage"] = "High (>30% test files)"
            elif quality["test_file_ratio"] > 15:
                quality["test_coverage"] = "Medium (15-30% test files)"
            elif quality["test_file_ratio"] > 5:
                quality["test_coverage"] = "Low (5-15% test files)"
            else:
                quality["test_coverage"] = "Minimal (<5% test files)"
        
        # Check for linting configs
        linting_files = [
            ".eslintrc", ".eslintrc.json", ".eslintrc.js",
            ".prettierrc", ".prettierrc.json",
            ".flake8", ".pylintrc", "pyproject.toml",
            ".rubocop.yml", "rustfmt.toml"
        ]
        
        for lint_file in linting_files:
            if any(lint_file in f for f in tree_analysis.get("config_files", [])):
                quality["linting_config"].append(lint_file.replace(".", "").split("rc")[0])
        
        # Check CI/CD
        if any(".github/workflows" in f for f in tree_analysis.get("config_files", [])):
            quality["ci_cd_tools"].append("GitHub Actions")
        if any(".gitlab-ci" in f for f in tree_analysis.get("config_files", [])):
            quality["ci_cd_tools"].append("GitLab CI")
        if any("Jenkinsfile" in f for f in tree_analysis.get("config_files", [])):
            quality["ci_cd_tools"].append("Jenkins")
        if any(".travis" in f for f in tree_analysis.get("config_files", [])):
            quality["ci_cd_tools"].append("Travis CI")
        
        # Check branch protection
        try:
            branch_protection = self.github._make_request(
                f"repos/{owner}/{repo}/branches/{self.github.get_repository_info(owner, repo).get('default_branch', 'main')}/protection"
            )
            if branch_protection and not branch_protection.get("error"):
                quality["branch_protection"] = True
                quality["code_review_process"] = "Protected branches with review requirements"
        except:
            pass
        
        # Documentation coverage
        doc_files = len(tree_analysis.get("doc_files", []))
        if total_files > 0:
            quality["documentation_coverage"] = round((doc_files / total_files) * 100, 1)
        
        return quality
    
    def analyze_commit_activity(self, commits: List[Dict], issues: List[Dict], prs: List[Dict]) -> Dict[str, Any]:
        """Analyze development activity patterns"""
        activity = {
            "commit_frequency": {},
            "peak_hours": [],
            "peak_days": [],
            "avg_pr_merge_time": "Unknown",
            "issue_resolution_time": "Unknown",
            "contributor_distribution": {},
            "commit_message_quality": "Unknown"
        }
        
        if commits:
            # Analyze commit times
            commit_times = []
            commit_days = []
            commit_authors = Counter()
            
            for commit in commits[:100]:  # Analyze last 100 commits
                if commit.get("commit"):
                    date_str = commit["commit"].get("author", {}).get("date")
                    if date_str:
                        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                        commit_times.append(dt.hour)
                        commit_days.append(dt.weekday())
                    
                    author = commit["commit"].get("author", {}).get("name", "Unknown")
                    commit_authors[author] += 1
            
            # Find peak hours
            if commit_times:
                hour_counts = Counter(commit_times)
                peak_hours = hour_counts.most_common(3)
                activity["peak_hours"] = [f"{h}:00-{h+1}:00 UTC ({c} commits)" for h, c in peak_hours]
            
            # Find peak days
            if commit_days:
                day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                day_counts = Counter(commit_days)
                peak_days = day_counts.most_common(3)
                activity["peak_days"] = [f"{day_names[d]} ({c} commits)" for d, c in peak_days]
            
            # Contributor distribution
            total_commits = sum(commit_authors.values())
            top_contributors = commit_authors.most_common(5)
            activity["contributor_distribution"] = {
                author: f"{count} commits ({round(count/total_commits*100, 1)}%)"
                for author, count in top_contributors
            }
            
            # Analyze commit message quality
            good_messages = 0
            for commit in commits[:50]:
                message = commit.get("commit", {}).get("message", "")
                # Good messages have proper length and structure
                if 10 < len(message) < 200 and (
                    any(prefix in message.lower() for prefix in ["fix:", "feat:", "docs:", "refactor:", "test:"]) or
                    len(message.split("\n")[0]) < 72
                ):
                    good_messages += 1
            
            if good_messages > 35:
                activity["commit_message_quality"] = "Excellent (follows conventions)"
            elif good_messages > 20:
                activity["commit_message_quality"] = "Good (mostly structured)"
            else:
                activity["commit_message_quality"] = "Needs improvement"
        
        # Analyze PR merge times
        if prs:
            merge_times = []
            for pr in prs[:20]:  # Check last 20 PRs
                if pr.get("merged_at") and pr.get("created_at"):
                    created = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
                    merged = datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00"))
                    merge_times.append((merged - created).total_seconds() / 3600)  # Hours
            
            if merge_times:
                avg_hours = statistics.mean(merge_times)
                if avg_hours < 24:
                    activity["avg_pr_merge_time"] = f"{round(avg_hours, 1)} hours"
                else:
                    activity["avg_pr_merge_time"] = f"{round(avg_hours/24, 1)} days"
        
        # Analyze issue resolution
        if issues:
            resolution_times = []
            for issue in issues[:20]:
                if issue.get("closed_at") and issue.get("created_at") and not issue.get("pull_request"):
                    created = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
                    closed = datetime.fromisoformat(issue["closed_at"].replace("Z", "+00:00"))
                    resolution_times.append((closed - created).total_seconds() / 3600)
            
            if resolution_times:
                avg_hours = statistics.mean(resolution_times)
                if avg_hours < 24:
                    activity["issue_resolution_time"] = f"{round(avg_hours, 1)} hours"
                elif avg_hours < 168:
                    activity["issue_resolution_time"] = f"{round(avg_hours/24, 1)} days"
                else:
                    activity["issue_resolution_time"] = f"{round(avg_hours/168, 1)} weeks"
        
        return activity
    
    def identify_tech_debt_indicators(self, tree_analysis: Dict, deps: Dict, quality: Dict) -> List[str]:
        """Identify specific technical debt indicators"""
        indicators = []
        
        # File organization debt
        if tree_analysis["max_depth"] > 6:
            indicators.append("Deep nesting (>6 levels) indicates complex organization")
        
        if tree_analysis["total_files"] > 500:
            indicators.append("Large codebase (>500 files) may need modularization")
        
        # Dependency debt
        if deps["total_count"] > 50:
            indicators.append(f"High dependency count ({deps['total_count']}) increases maintenance burden")
        
        if len(deps.get("outdated_check", [])) > 5:
            indicators.append("Multiple dependencies using flexible versioning")
        
        # Testing debt
        if quality["test_file_ratio"] < 10:
            indicators.append("Low test coverage (<10% test files)")
        
        if not quality["ci_cd_tools"]:
            indicators.append("No CI/CD pipeline detected")
        
        if not quality["linting_config"]:
            indicators.append("No code linting configuration found")
        
        # Documentation debt
        if quality["documentation_coverage"] < 5:
            indicators.append("Minimal documentation coverage")
        
        if not indicators:
            indicators.append("No significant technical debt indicators detected")
        
        return indicators
    
    def analyze_security_posture(self, deps: Dict, quality: Dict) -> Dict[str, Any]:
        """Analyze security implications"""
        security = {
            "dependency_risks": [],
            "security_features": [],
            "vulnerabilities": []
        }
        
        # Check for known vulnerable patterns
        vulnerable_packages = {
            "npm": ["minimist<1.2.6", "axios<0.21.1", "lodash<4.17.21"],
            "pip": ["django<3.2", "flask<2.0", "requests<2.25.0"]
        }
        
        for manager, packages in deps.get("direct_dependencies", {}).items():
            if manager in vulnerable_packages:
                for pkg, version in packages.items():
                    # This is simplified - real implementation would check actual versions
                    security["dependency_risks"].append(f"Check {pkg} version for known vulnerabilities")
        
        # Security features
        if quality.get("branch_protection"):
            security["security_features"].append("Branch protection enabled")
        
        if any("dependabot" in str(f).lower() for f in quality.get("ci_cd_tools", [])):
            security["security_features"].append("Automated dependency updates")
        
        if any("security" in str(f).lower() for f in quality.get("ci_cd_tools", [])):
            security["security_features"].append("Security scanning in CI/CD")
        
        if not security["security_features"]:
            security["security_features"].append("Consider enabling security features")
        
        return security