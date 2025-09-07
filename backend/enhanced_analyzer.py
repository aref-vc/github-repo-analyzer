"""
Enhanced Repository Analysis Engine
Advanced analysis capabilities for deeper repository intelligence
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import statistics

class EnhancedAnalyzer:
    """Enhanced analysis capabilities for deeper repository insights"""
    
    def __init__(self, github_analyzer):
        self.github = github_analyzer
    
    def analyze_directory_structure(self, owner: str, repo: str) -> Dict[str, Any]:
        """Analyze repository directory structure and patterns"""
        try:
            # Get repository tree
            tree_endpoint = f"repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
            tree_data = self.github._make_request(tree_endpoint)
            
            if not tree_data.get("tree"):
                return {"structure": "Unable to analyze", "patterns": []}
            
            files = tree_data["tree"]
            directories = defaultdict(int)
            file_types = Counter()
            
            # Analyze file patterns
            for item in files:
                if item["type"] == "blob":  # File
                    path = item["path"]
                    directory = "/".join(path.split("/")[:-1]) if "/" in path else "root"
                    directories[directory] += 1
                    
                    # Extract file extension
                    if "." in path:
                        ext = path.split(".")[-1].lower()
                        file_types[ext] += 1
            
            # Identify project structure patterns
            patterns = self._identify_project_patterns(files, directories, file_types)
            
            # Create directory hierarchy
            hierarchy = self._build_directory_hierarchy(directories)
            
            return {
                "total_files": len([f for f in files if f["type"] == "blob"]),
                "total_directories": len(directories),
                "file_types": dict(file_types.most_common(10)),
                "structure_patterns": patterns,
                "directory_hierarchy": hierarchy,
                "largest_directories": dict(Counter(directories).most_common(5))
            }
        except Exception as e:
            return {
                "structure": f"Analysis failed: {str(e)}",
                "patterns": [],
                "total_files": 0
            }
    
    def analyze_dependencies_deep(self, owner: str, repo: str) -> Dict[str, Any]:
        """Deep analysis of project dependencies and ecosystem"""
        dependencies = {
            "package_managers": [],
            "core_dependencies": [],
            "dev_dependencies": [],
            "dependency_count": 0,
            "security_concerns": [],
            "ecosystem_analysis": {}
        }
        
        try:
            # Check for various package manager files
            package_files = [
                ("package.json", "npm/yarn"),
                ("requirements.txt", "pip"),
                ("Pipfile", "pipenv"), 
                ("poetry.lock", "poetry"),
                ("Cargo.toml", "rust"),
                ("go.mod", "go modules"),
                ("composer.json", "composer"),
                ("Gemfile", "bundler"),
                ("pom.xml", "maven"),
                ("build.gradle", "gradle")
            ]
            
            for filename, manager in package_files:
                try:
                    file_data = self.github._make_request(f"repos/{owner}/{repo}/contents/{filename}")
                    if file_data:
                        dependencies["package_managers"].append(manager)
                        
                        # Parse specific file types
                        if filename == "package.json":
                            deps = self._parse_package_json(file_data)
                            dependencies.update(deps)
                        elif filename == "requirements.txt":
                            deps = self._parse_requirements_txt(file_data)
                            dependencies["core_dependencies"].extend(deps)
                            
                except:
                    continue
            
            dependencies["dependency_count"] = len(dependencies["core_dependencies"]) + len(dependencies["dev_dependencies"])
            
            return dependencies
            
        except Exception as e:
            dependencies["analysis_error"] = str(e)
            return dependencies
    
    def analyze_code_quality_deep(self, owner: str, repo: str) -> Dict[str, Any]:
        """Deep code quality analysis"""
        quality_metrics = {
            "testing_framework": "Unknown",
            "test_coverage": "Unknown",
            "linting_tools": [],
            "ci_cd_analysis": {},
            "code_standards": {},
            "documentation_quality": "Unknown"
        }
        
        try:
            # Check for testing frameworks
            test_patterns = {
                "pytest": ["pytest.ini", "conftest.py"],
                "jest": ["jest.config.js", "__tests__"],
                "mocha": ["mocha.opts", "test/"],
                "rspec": [".rspec", "spec/"],
                "unittest": ["test_*.py", "*_test.py"]
            }
            
            for framework, patterns in test_patterns.items():
                for pattern in patterns:
                    try:
                        search_result = self.github.search_files(owner, repo, pattern, limit=1)
                        if search_result:
                            quality_metrics["testing_framework"] = framework
                            break
                    except:
                        continue
                if quality_metrics["testing_framework"] != "Unknown":
                    break
            
            # Check for linting configurations
            linting_configs = [
                (".eslintrc", "ESLint"),
                (".pylintrc", "Pylint"), 
                ("pyproject.toml", "Modern Python tools"),
                ("tslint.json", "TSLint"),
                (".rubocop.yml", "RuboCop")
            ]
            
            for config_file, tool in linting_configs:
                try:
                    file_data = self.github._make_request(f"repos/{owner}/{repo}/contents/{config_file}")
                    if file_data:
                        quality_metrics["linting_tools"].append(tool)
                except:
                    continue
            
            # Analyze GitHub Actions
            workflows = self.github.get_workflow_runs(owner, repo, limit=20)
            if workflows:
                quality_metrics["ci_cd_analysis"] = self._analyze_workflows(workflows)
            
            return quality_metrics
            
        except Exception as e:
            quality_metrics["analysis_error"] = str(e)
            return quality_metrics
    
    def analyze_commit_patterns_deep(self, owner: str, repo: str, commits: List[Dict]) -> Dict[str, Any]:
        """Deep analysis of commit patterns and development activity"""
        if not commits:
            return {"analysis": "No commits available"}
        
        # Parse commit data
        commit_data = []
        for commit in commits:
            try:
                commit_info = {
                    "date": datetime.fromisoformat(commit["commit"]["author"]["date"].replace('Z', '+00:00')),
                    "author": commit["commit"]["author"]["name"],
                    "message": commit["commit"]["message"],
                    "additions": commit.get("stats", {}).get("additions", 0),
                    "deletions": commit.get("stats", {}).get("deletions", 0)
                }
                commit_data.append(commit_info)
            except:
                continue
        
        if not commit_data:
            return {"analysis": "Unable to parse commit data"}
        
        # Analyze patterns
        analysis = {}
        
        # Time patterns
        commit_dates = [c["date"] for c in commit_data]
        if commit_dates:
            date_range = max(commit_dates) - min(commit_dates)
            analysis["active_period_days"] = date_range.days
            analysis["average_commits_per_day"] = len(commit_dates) / max(date_range.days, 1)
        
        # Author patterns
        authors = [c["author"] for c in commit_data]
        author_counts = Counter(authors)
        analysis["unique_authors"] = len(author_counts)
        analysis["top_contributors"] = dict(author_counts.most_common(5))
        
        # Commit message patterns
        messages = [c["message"] for c in commit_data]
        analysis["commit_types"] = self._analyze_commit_types(messages)
        
        # Code churn analysis
        if any(c["additions"] > 0 or c["deletions"] > 0 for c in commit_data):
            additions = [c["additions"] for c in commit_data if c["additions"] > 0]
            deletions = [c["deletions"] for c in commit_data if c["deletions"] > 0]
            
            if additions:
                analysis["average_additions"] = round(statistics.mean(additions), 1)
            if deletions:
                analysis["average_deletions"] = round(statistics.mean(deletions), 1)
        
        return analysis
    
    def analyze_issue_patterns(self, owner: str, repo: str) -> Dict[str, Any]:
        """Analyze issue and PR patterns for project health"""
        try:
            issues = self.github.get_issues(owner, repo, limit=100)
            prs = self.github.get_pull_requests(owner, repo, limit=50)
            
            analysis = {
                "issue_analysis": self._analyze_issues(issues),
                "pr_analysis": self._analyze_pull_requests(prs),
                "project_health_score": 0
            }
            
            # Calculate project health score (0-100)
            health_score = self._calculate_health_score(issues, prs)
            analysis["project_health_score"] = health_score
            
            return analysis
            
        except Exception as e:
            return {"analysis_error": str(e)}
    
    def _identify_project_patterns(self, files: List[Dict], directories: Dict, file_types: Counter) -> List[str]:
        """Identify common project structure patterns"""
        patterns = []
        
        file_paths = [f["path"] for f in files if f["type"] == "blob"]
        
        # Web development patterns
        if any("package.json" in path for path in file_paths):
            patterns.append("Node.js/NPM project")
        
        if "src/" in directories and "public/" in directories:
            patterns.append("Modern web application structure")
        
        # Python patterns
        if "requirements.txt" in [f.split("/")[-1] for f in file_paths]:
            patterns.append("Python project with pip dependencies")
        
        if "setup.py" in [f.split("/")[-1] for f in file_paths]:
            patterns.append("Python package structure")
        
        # Documentation patterns
        if any("docs/" in path for path in file_paths):
            patterns.append("Documented project")
        
        if any(path.lower().startswith("readme") for path in file_paths):
            patterns.append("Well-documented project")
        
        # Testing patterns
        if any("test" in path.lower() for path in file_paths):
            patterns.append("Includes automated tests")
        
        # CI/CD patterns
        if any(".github/workflows" in path for path in file_paths):
            patterns.append("GitHub Actions CI/CD")
        
        return patterns
    
    def _build_directory_hierarchy(self, directories: Dict) -> Dict[str, Any]:
        """Build a hierarchical view of directories"""
        hierarchy = {"root": {"subdirs": {}, "file_count": directories.get("root", 0)}}
        
        for dir_path, file_count in directories.items():
            if dir_path == "root":
                continue
                
            parts = dir_path.split("/")
            current = hierarchy["root"]
            
            for part in parts:
                if part not in current["subdirs"]:
                    current["subdirs"][part] = {"subdirs": {}, "file_count": 0}
                current = current["subdirs"][part]
            
            current["file_count"] = file_count
        
        return hierarchy
    
    def _parse_package_json(self, file_data: Dict) -> Dict[str, List]:
        """Parse package.json dependencies"""
        try:
            import base64
            content = base64.b64decode(file_data["content"]).decode("utf-8")
            package_data = json.loads(content)
            
            return {
                "core_dependencies": list(package_data.get("dependencies", {}).keys()),
                "dev_dependencies": list(package_data.get("devDependencies", {}).keys())
            }
        except:
            return {"core_dependencies": [], "dev_dependencies": []}
    
    def _parse_requirements_txt(self, file_data: Dict) -> List[str]:
        """Parse requirements.txt dependencies"""
        try:
            import base64
            content = base64.b64decode(file_data["content"]).decode("utf-8")
            lines = content.strip().split('\n')
            deps = []
            
            for line in lines:
                if line and not line.startswith('#'):
                    # Extract package name (before ==, >=, etc.)
                    dep = re.split(r'[><=!]', line)[0].strip()
                    if dep:
                        deps.append(dep)
            
            return deps
        except:
            return []
    
    def _analyze_workflows(self, workflows: List[Dict]) -> Dict[str, Any]:
        """Analyze GitHub Actions workflows"""
        if not workflows:
            return {"status": "No workflows found"}
        
        successful = len([w for w in workflows if w.get("conclusion") == "success"])
        failed = len([w for w in workflows if w.get("conclusion") == "failure"])
        total = len(workflows)
        
        return {
            "total_runs": total,
            "success_rate": round((successful / total) * 100, 1) if total > 0 else 0,
            "recent_failures": failed,
            "workflow_health": "Healthy" if (successful / total) > 0.8 else "Needs attention"
        }
    
    def _analyze_commit_types(self, messages: List[str]) -> Dict[str, int]:
        """Analyze commit message types using conventional commits"""
        types = Counter()
        
        for message in messages:
            # Check for conventional commit patterns
            conventional_match = re.match(r'^(\w+)(\(.+\))?\s*:\s*', message.lower())
            if conventional_match:
                commit_type = conventional_match.group(1)
                types[commit_type] += 1
            else:
                # Fallback to keyword analysis
                if any(word in message.lower() for word in ["fix", "bug"]):
                    types["fix"] += 1
                elif any(word in message.lower() for word in ["feat", "add", "new"]):
                    types["feat"] += 1
                elif any(word in message.lower() for word in ["doc", "readme"]):
                    types["docs"] += 1
                else:
                    types["other"] += 1
        
        return dict(types)
    
    def _analyze_issues(self, issues: List[Dict]) -> Dict[str, Any]:
        """Analyze issue patterns"""
        if not issues:
            return {"status": "No issues found"}
        
        open_issues = [i for i in issues if i["state"] == "open"]
        closed_issues = [i for i in issues if i["state"] == "closed"]
        
        # Analyze labels
        all_labels = []
        for issue in issues:
            all_labels.extend([label["name"] for label in issue.get("labels", [])])
        
        label_counts = Counter(all_labels)
        
        return {
            "total_issues": len(issues),
            "open_issues": len(open_issues),
            "closed_issues": len(closed_issues),
            "common_labels": dict(label_counts.most_common(5)),
            "issue_resolution_rate": round((len(closed_issues) / len(issues)) * 100, 1) if issues else 0
        }
    
    def _analyze_pull_requests(self, prs: List[Dict]) -> Dict[str, Any]:
        """Analyze pull request patterns"""
        if not prs:
            return {"status": "No pull requests found"}
        
        merged = len([pr for pr in prs if pr.get("merged_at")])
        open_prs = len([pr for pr in prs if pr["state"] == "open"])
        closed = len([pr for pr in prs if pr["state"] == "closed"])
        
        return {
            "total_prs": len(prs),
            "merged_prs": merged,
            "open_prs": open_prs,
            "closed_prs": closed,
            "merge_rate": round((merged / len(prs)) * 100, 1) if prs else 0
        }
    
    def _calculate_health_score(self, issues: List[Dict], prs: List[Dict]) -> int:
        """Calculate overall project health score (0-100)"""
        score = 50  # Base score
        
        # Issue health
        if issues:
            open_ratio = len([i for i in issues if i["state"] == "open"]) / len(issues)
            if open_ratio < 0.3:  # Less than 30% open issues is good
                score += 20
            elif open_ratio > 0.7:  # More than 70% open issues is concerning
                score -= 20
        
        # PR health
        if prs:
            merged_ratio = len([pr for pr in prs if pr.get("merged_at")]) / len(prs)
            if merged_ratio > 0.7:  # High merge rate is good
                score += 15
            elif merged_ratio < 0.3:  # Low merge rate might indicate problems
                score -= 15
        
        # Activity bonus
        recent_activity = len([i for i in issues if 
                             datetime.fromisoformat(i["updated_at"].replace('Z', '+00:00')) > 
                             datetime.now().replace(tzinfo=datetime.now().astimezone().tzinfo) - timedelta(days=30)])
        if recent_activity > 5:
            score += 15
        
        return max(0, min(100, score))