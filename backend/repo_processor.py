"""
Repository Data Processor
Transforms raw GitHub API data into structured analysis following the template
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from github_analyzer import GitHubAnalyzer
from optimized_analyzer import OptimizedAnalyzer
from deep_analyzer import DeepAnalyzer
from cache import cache_repository_analysis, get_cached_analysis, cache_result
import re
from collections import Counter

class RepoProcessor:
    def __init__(self, github_analyzer: GitHubAnalyzer):
        self.github = github_analyzer
        self.enhanced = OptimizedAnalyzer(github_analyzer)
        self.deep = DeepAnalyzer(github_analyzer)
    
    def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
        """
        Complete repository analysis following the structured template
        """
        try:
            # Parse repository URL
            owner, repo = self.github.parse_repo_url(repo_url)
            
            # Check cache first
            cached_analysis = get_cached_analysis(owner, repo)
            if cached_analysis:
                print(f"✅ Using cached analysis for {owner}/{repo}")
                return cached_analysis
            
            # Gather all necessary data
            print(f"🔍 Analyzing {owner}/{repo}...")
            
            # Basic repo info
            repo_info = self.github.get_repository_info(owner, repo)
            languages = self.github.get_languages(owner, repo)
            contributors = self.github.get_contributors(owner, repo)
            commits = self.github.get_commits(owner, repo)
            releases = self.github.get_releases(owner, repo)
            issues = self.github.get_issues(owner, repo)
            pull_requests = self.github.get_pull_requests(owner, repo)
            readme = self.github.get_readme(owner, repo)
            package_json = self.github.get_package_json(owner, repo)
            requirements_txt = self.github.get_requirements_txt(owner, repo)
            workflows = self.github.get_workflow_runs(owner, repo)
            
            # Try to get enhanced insights (with timeout protection)
            enhanced_insights = None
            try:
                enhanced_insights = self.enhanced.get_quick_insights(owner, repo)
            except Exception as e:
                print(f"⚠️ Enhanced analysis skipped: {e}")
            
            # Perform deep analysis for complete data
            print(f"🔬 Performing deep analysis...")
            tree_analysis = self.deep.analyze_file_tree(owner, repo)
            deep_deps = self.deep.analyze_dependencies_detailed(owner, repo)
            deep_quality = self.deep.analyze_code_quality_detailed(owner, repo, tree_analysis)
            deep_activity = self.deep.analyze_commit_activity(commits, issues, pull_requests)
            security_analysis = self.deep.analyze_security_posture(deep_deps, deep_quality)
            
            # Process data into structured analysis with deep insights
            analysis = {
                "repository_metadata": self._process_metadata(repo_info, languages, contributors),
                "architecture_synopsis": self._process_architecture_deep(repo_info, package_json, requirements_txt, tree_analysis, deep_deps),
                "code_quality_metrics": self._process_quality_metrics_deep(repo_info, workflows, deep_quality, tree_analysis),
                "documentation_extraction": self._process_documentation(readme, repo_info),
                "development_activity": self._process_activity_deep(commits, issues, pull_requests, releases, deep_activity),
                "technical_debt_assessment": self._process_technical_debt_deep(repo_info, languages, tree_analysis, deep_deps, deep_quality, security_analysis),
                "raw_data": {
                    "fetched_at": datetime.now().isoformat(),
                    "repo_url": f"https://github.com/{owner}/{repo}",
                    "api_calls_made": 8,  # Basic analysis API calls
                    "enhanced_analysis": enhanced_insights is not None
                }
            }
            
            # Merge enhanced insights if available
            if enhanced_insights:
                analysis["enhanced_insights"] = enhanced_insights
            
            # Cache the successful analysis
            cache_repository_analysis(owner, repo, analysis)
            print(f"💾 Analysis cached for {owner}/{repo}")
            
            return analysis
            
        except Exception as e:
            raise Exception(f"Repository analysis failed: {str(e)}")
    
    def _process_metadata(self, repo_info: Dict, languages: Dict, contributors: List) -> Dict[str, Any]:
        """Process Repository Metadata Block"""
        total_bytes = sum(languages.values()) if languages else 1
        language_percentages = {
            lang: round((bytes_count / total_bytes) * 100, 1) 
            for lang, bytes_count in languages.items()
        } if languages else {}
        
        primary_language = max(language_percentages.items(), key=lambda x: x[1])[0] if language_percentages else "Unknown"
        
        return {
            "language_composition": language_percentages,
            "primary_stack": primary_language,
            "repository_size_kb": repo_info.get("size", 0),
            "commit_frequency": self._calculate_commit_frequency(repo_info),
            "contributor_count": len(contributors),
            "license_type": repo_info.get("license", {}).get("name") if repo_info.get("license") else "No License",
            "dependency_count": "Analyzed in Architecture Synopsis",
            "latest_release": repo_info.get("default_branch", "main"),
            "created_date": repo_info.get("created_at"),
            "last_updated": repo_info.get("updated_at"),
            "stars": repo_info.get("stargazers_count", 0),
            "forks": repo_info.get("forks_count", 0),
            "watchers": repo_info.get("watchers_count", 0)
        }
    
    def _process_architecture(self, repo_info: Dict, package_json: Dict, requirements_txt: str) -> Dict[str, Any]:
        """Process Architecture Synopsis"""
        entry_points = []
        dependencies = {"core": [], "dev": []}
        
        # Analyze package.json for Node.js projects
        if package_json:
            scripts = package_json.get("scripts", {})
            entry_points.extend([f"{script}: {command}" for script, command in scripts.items()])
            
            deps = package_json.get("dependencies", {})
            dev_deps = package_json.get("devDependencies", {})
            dependencies["core"] = list(deps.keys())
            dependencies["dev"] = list(dev_deps.keys())
        
        # Analyze requirements.txt for Python projects
        if requirements_txt:
            lines = requirements_txt.strip().split('\n')
            python_deps = [line.split('==')[0].split('>=')[0].split('<=')[0] for line in lines if line and not line.startswith('#')]
            dependencies["core"].extend(python_deps)
        
        return {
            "entry_points": entry_points or ["No explicit entry points found"],
            "directory_structure": "TBD - Requires tree analysis",
            "core_dependencies": dependencies["core"][:20],  # Limit to top 20
            "dev_dependencies": dependencies["dev"][:20],
            "build_system": self._detect_build_system(package_json, requirements_txt),
            "deployment_pipeline": "TBD - Requires CI/CD analysis"
        }
    
    def _process_quality_metrics(self, repo_info: Dict, workflows: List) -> Dict[str, Any]:
        """Process Code Quality Metrics"""
        has_actions = len(workflows) > 0
        recent_workflows = [w for w in workflows if w.get("status") == "completed"][:5]
        
        return {
            "test_coverage_percentage": "TBD - Requires code analysis",
            "testing_framework": "TBD - Requires file analysis",
            "linting_standards": "TBD - Requires config file analysis",
            "ci_cd_pipeline_status": "Active" if has_actions else "Not detected",
            "automation_scope": f"{len(workflows)} workflow runs found" if workflows else "No automation detected",
            "security_vulnerabilities": "TBD - Requires security scan",
            "recent_workflow_results": [
                {
                    "name": w.get("name", "Unknown"),
                    "status": w.get("conclusion", "unknown"),
                    "date": w.get("updated_at")
                } for w in recent_workflows
            ]
        }
    
    def _process_documentation(self, readme: str, repo_info: Dict) -> Dict[str, Any]:
        """Process Documentation Extraction"""
        readme_summary = "No README found"
        installation_steps = []
        usage_examples = []
        
        if readme:
            # Extract README summary (first few paragraphs)
            lines = readme.split('\n')
            summary_lines = []
            for line in lines[:20]:  # First 20 lines
                if line.strip() and not line.startswith('#'):
                    summary_lines.append(line.strip())
                if len(summary_lines) >= 3:  # Get first 3 non-header lines
                    break
            readme_summary = ' '.join(summary_lines) if summary_lines else "README exists but no summary found"
            
            # Look for installation instructions
            readme_lower = readme.lower()
            if 'install' in readme_lower:
                install_section = re.search(r'## installation.*?\n(.*?)(?=##|\Z)', readme, re.IGNORECASE | re.DOTALL)
                if install_section:
                    installation_steps = [line.strip() for line in install_section.group(1).split('\n')[:5] if line.strip()]
        
        return {
            "readme_summary": readme_summary[:500] + "..." if len(readme_summary) > 500 else readme_summary,
            "api_documentation": "TBD - Requires API endpoint analysis",
            "installation_requirements": installation_steps or ["Check README for installation instructions"],
            "configuration_variables": "TBD - Requires env file analysis",
            "known_limitations": "TBD - Requires issue analysis",
            "compatibility_constraints": f"Language: {repo_info.get('language', 'Unknown')}"
        }
    
    def _process_activity(self, commits: List, issues: List, pull_requests: List, releases: List) -> Dict[str, Any]:
        """Process Development Activity Indicators"""
        # Analyze commit patterns
        recent_commits = [c for c in commits[:30]]  # Last 30 commits
        commit_dates = [datetime.fromisoformat(c["commit"]["author"]["date"].replace('Z', '+00:00')) for c in recent_commits]
        
        # Calculate commit frequency
        if commit_dates:
            days_diff = (datetime.now().replace(tzinfo=commit_dates[0].tzinfo) - min(commit_dates)).days
            commit_frequency = len(commit_dates) / max(days_diff, 1) if days_diff > 0 else len(commit_dates)
        else:
            commit_frequency = 0
        
        # Analyze issues and PRs
        open_issues = [i for i in issues if i.get("state") == "open" and not i.get("pull_request")]
        open_prs = [pr for pr in pull_requests if pr.get("state") == "open"]
        
        return {
            "recent_commit_patterns": f"{len(recent_commits)} commits in last 30",
            "commit_frequency_per_day": round(commit_frequency, 2),
            "release_cadence": f"{len(releases)} releases total" if releases else "No releases",
            "open_issues_count": len(open_issues),
            "open_pull_requests": len(open_prs),
            "pull_request_velocity": "TBD - Requires temporal analysis",
            "contributor_activity": f"{len(set([c['author']['login'] for c in recent_commits if c.get('author')]))} active contributors",
            "breaking_changes": "TBD - Requires changelog analysis",
            "latest_release": releases[0] if releases else None
        }
    
    def _process_technical_debt(self, repo_info: Dict, languages: Dict, dependencies: Dict) -> Dict[str, Any]:
        """Process Technical Debt Assessment"""
        age_years = self._calculate_repo_age(repo_info.get("created_at"))
        
        debt_indicators = []
        if age_years > 3:
            debt_indicators.append("Repository is over 3 years old - check for outdated dependencies")
        
        if repo_info.get("size", 0) > 100000:  # > 100MB
            debt_indicators.append("Large repository size may indicate accumulated technical debt")
        
        return {
            "outdated_dependencies": "TBD - Requires dependency version analysis",
            "security_implications": "TBD - Requires vulnerability scan",
            "code_complexity_hotspots": "TBD - Requires static analysis",
            "performance_bottlenecks": "TBD - Requires performance profiling",
            "scalability_concerns": "TBD - Requires architecture analysis",
            "maintenance_burden": f"Repository age: {age_years:.1f} years",
            "debt_indicators": debt_indicators or ["No immediate debt indicators detected"],
            "refactoring_opportunities": "TBD - Requires code analysis"
        }
    
    def _calculate_commit_frequency(self, repo_info: Dict) -> str:
        """Calculate approximate commit frequency"""
        created = repo_info.get("created_at")
        updated = repo_info.get("updated_at")
        
        if created and updated:
            created_date = datetime.fromisoformat(created.replace('Z', '+00:00'))
            updated_date = datetime.fromisoformat(updated.replace('Z', '+00:00'))
            days_active = (updated_date - created_date).days
            
            if days_active > 0:
                return f"Active for {days_active} days"
        
        return "Unable to calculate"
    
    def _detect_build_system(self, package_json: Dict, requirements_txt: str) -> str:
        """Detect build system based on available files"""
        if package_json:
            if "webpack" in str(package_json.get("devDependencies", {})):
                return "Webpack"
            elif "vite" in str(package_json.get("devDependencies", {})):
                return "Vite"
            elif package_json.get("scripts", {}).get("build"):
                return "NPM Scripts"
            else:
                return "Node.js"
        elif requirements_txt:
            return "Python/pip"
        else:
            return "Unknown"
    
    def _calculate_repo_age(self, created_at: str) -> float:
        """Calculate repository age in years"""
        if not created_at:
            return 0
        
        created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        age = datetime.now().replace(tzinfo=created_date.tzinfo) - created_date
        return age.days / 365.25
    
    def _process_architecture_deep(self, repo_info: Dict, package_json: Dict, requirements_txt: str, 
                                  tree_analysis: Dict, deep_deps: Dict) -> Dict[str, Any]:
        """Process architecture with deep analysis data"""
        # Get base architecture
        base = self._process_architecture(repo_info, package_json, requirements_txt)
        
        # Replace TBD fields with real data
        base["architecture_pattern"] = self.deep.detect_architecture_pattern(tree_analysis)
        base["data_flow_analysis"] = f"Repository structure: {tree_analysis.get('total_dirs', 0)} directories, {tree_analysis.get('total_files', 0)} files, max depth: {tree_analysis.get('max_depth', 0)}"
        base["scalability_assessment"] = f"Modular structure with {len(tree_analysis.get('directory_structure', {}))} modules"
        base["performance_considerations"] = f"Dependencies: {deep_deps.get('total_count', 0)} total packages across {len(deep_deps.get('package_managers', []))} package managers"
        
        # Replace the TBD directory_structure with actual data
        dir_struct = tree_analysis.get('directory_structure', {})
        if dir_struct:
            # Get top-level directories
            top_dirs = set()
            for path in dir_struct.keys():
                parts = path.split('/')
                if parts[0]:
                    top_dirs.add(parts[0])
            
            # Build directory summary
            dir_summary = f"{tree_analysis.get('total_files', 0)} files in {tree_analysis.get('total_dirs', 0)} directories"
            if top_dirs:
                dir_summary += f" | Main folders: {', '.join(sorted(list(top_dirs)[:10]))}"
            
            base["directory_structure"] = dir_summary
        else:
            base["directory_structure"] = f"{tree_analysis.get('total_files', 0)} files, {tree_analysis.get('total_dirs', 0)} directories"
        
        # Replace the deployment_pipeline TBD if we have CI/CD info
        if deep_deps.get('package_managers'):
            base["deployment_pipeline"] = f"Detected: {', '.join(deep_deps['package_managers'])}"
        
        # Add file type distribution
        file_types = tree_analysis.get("file_types", {})
        if file_types:
            # file_types is already a Counter object from deep_analyzer
            if isinstance(file_types, Counter):
                top_types = dict(file_types.most_common(5))
            else:
                top_types = dict(Counter(file_types).most_common(5))
            base["primary_technologies"] = ", ".join([f"{ext}: {count} files" for ext, count in top_types.items()])
        
        return base
    
    def _process_quality_metrics_deep(self, repo_info: Dict, workflows: List, deep_quality: Dict, tree_analysis: Dict) -> Dict[str, Any]:
        """Process quality metrics with deep analysis data"""
        base = self._process_quality_metrics(repo_info, workflows)
        
        # Replace TBD fields with real data
        base["testing_framework"] = deep_quality.get("test_coverage", "Unknown")
        base["code_coverage"] = f"{deep_quality.get('test_file_ratio', 0)}% test files"
        base["linting_standards"] = ", ".join(deep_quality.get("linting_config", [])) if deep_quality.get("linting_config") else "No linting config detected"
        base["documentation_quality"] = f"{deep_quality.get('documentation_coverage', 0)}% documentation coverage"
        base["automation_scope"] = ", ".join(deep_quality.get("ci_cd_tools", [])) if deep_quality.get("ci_cd_tools") else "No CI/CD detected"
        base["branch_protection"] = "Enabled" if deep_quality.get("branch_protection") else "Not enabled"
        base["code_review_process"] = deep_quality.get("code_review_process", "Unknown")
        
        return base
    
    def _process_activity_deep(self, commits: List, issues: List, prs: List, releases: List, deep_activity: Dict) -> Dict[str, Any]:
        """Process development activity with deep analysis data"""
        base = self._process_activity(commits, issues, prs, releases)
        
        # Replace TBD fields with real data
        base["pull_request_velocity"] = deep_activity.get("avg_pr_merge_time", "Unknown")
        base["issue_resolution_time"] = deep_activity.get("issue_resolution_time", "Unknown")
        base["commit_message_quality"] = deep_activity.get("commit_message_quality", "Unknown")
        
        # Add peak activity times
        if deep_activity.get("peak_hours"):
            base["peak_development_hours"] = ", ".join(deep_activity["peak_hours"][:2])
        
        if deep_activity.get("peak_days"):
            base["peak_development_days"] = ", ".join(deep_activity["peak_days"][:2])
        
        # Add contributor insights
        if deep_activity.get("contributor_distribution"):
            base["top_contributors"] = deep_activity["contributor_distribution"]
        
        # Analyze breaking changes from commit messages
        breaking_changes = []
        for commit in commits[:30]:
            message = commit.get("commit", {}).get("message", "").lower()
            if "breaking" in message or "major" in message or "incompatible" in message:
                breaking_changes.append(message.split("\n")[0][:100])
        
        base["breaking_changes"] = breaking_changes[:3] if breaking_changes else ["No breaking changes detected in recent commits"]
        
        return base
    
    def _process_technical_debt_deep(self, repo_info: Dict, languages: Dict, tree_analysis: Dict, 
                                    deep_deps: Dict, deep_quality: Dict, security_analysis: Dict) -> Dict[str, Any]:
        """Process technical debt with deep analysis data"""
        base = self._process_technical_debt(repo_info, languages, deep_deps)
        
        # Get specific debt indicators
        debt_indicators = self.deep.identify_tech_debt_indicators(tree_analysis, deep_deps, deep_quality)
        
        # Replace TBD fields with real data
        base["outdated_dependencies"] = ", ".join(deep_deps.get("outdated_check", []))[:200] if deep_deps.get("outdated_check") else "All dependencies use fixed versioning"
        base["security_implications"] = security_analysis.get("dependency_risks", ["No known security risks detected"])
        base["code_complexity_hotspots"] = f"Repository complexity: {tree_analysis.get('max_depth', 0)} levels deep, {tree_analysis.get('total_files', 0)} files"
        base["performance_bottlenecks"] = f"Large repository size: {repo_info.get('size', 0)/1024:.1f}MB" if repo_info.get('size', 0) > 50000 else "Repository size is manageable"
        base["scalability_concerns"] = f"Total dependencies: {deep_deps.get('total_count', 0)}" if deep_deps.get('total_count', 0) > 30 else "Dependency count is reasonable"
        base["debt_indicators"] = debt_indicators
        base["refactoring_opportunities"] = [
            f"Consider breaking down directories with many files" if any(len(files) > 20 for files in tree_analysis.get("directory_structure", {}).values()) else "File organization appears good",
            f"Add more tests to improve coverage" if deep_quality.get("test_file_ratio", 0) < 15 else "Test coverage appears adequate",
            f"Implement linting standards" if not deep_quality.get("linting_config") else "Linting is configured"
        ]
        
        # Add security features
        if security_analysis.get("security_features"):
            base["security_features"] = security_analysis["security_features"]
        
        return base
    
    def _process_architecture_enhanced(self, repo_info: Dict, package_json: Dict, requirements_txt: str, 
                                     dir_structure: Dict, deep_deps: Dict) -> Dict[str, Any]:
        """Enhanced architecture analysis"""
        # Get base analysis
        base_analysis = self._process_architecture(repo_info, package_json, requirements_txt)
        
        # Add enhanced data
        enhanced = base_analysis.copy()
        enhanced.update({
            "directory_structure": f"{dir_structure.get('total_files', 0)} files in {dir_structure.get('total_directories', 0)} directories",
            "project_patterns": dir_structure.get("structure_patterns", []),
            "file_type_distribution": dir_structure.get("file_types", {}),
            "dependency_count": deep_deps.get("dependency_count", 0),
            "package_managers": deep_deps.get("package_managers", []),
            "build_system": self._detect_build_system_enhanced(package_json, requirements_txt, dir_structure),
            "deployment_pipeline": "GitHub Actions detected" if any("actions" in pattern.lower() for pattern in dir_structure.get("structure_patterns", [])) else "No CI/CD detected"
        })
        
        return enhanced
    
    def _process_quality_metrics_enhanced(self, repo_info: Dict, workflows: List, code_quality_deep: Dict) -> Dict[str, Any]:
        """Enhanced code quality analysis"""
        base_quality = self._process_quality_metrics(repo_info, workflows)
        
        enhanced = base_quality.copy()
        enhanced.update({
            "testing_framework": code_quality_deep.get("testing_framework", "Unknown"),
            "linting_standards": ", ".join(code_quality_deep.get("linting_tools", [])) or "Not detected",
            "ci_cd_analysis": code_quality_deep.get("ci_cd_analysis", {}),
            "code_standards": {
                "has_linting": len(code_quality_deep.get("linting_tools", [])) > 0,
                "has_testing": code_quality_deep.get("testing_framework", "Unknown") != "Unknown"
            }
        })
        
        return enhanced
    
    def _process_documentation_enhanced(self, readme: str, repo_info: Dict, dir_structure: Dict) -> Dict[str, Any]:
        """Enhanced documentation analysis"""
        base_docs = self._process_documentation(readme, repo_info)
        
        # Check for documentation patterns from directory structure
        patterns = dir_structure.get("structure_patterns", [])
        has_docs = any("documented" in pattern.lower() for pattern in patterns)
        
        enhanced = base_docs.copy()
        enhanced.update({
            "documentation_quality": "Well documented" if has_docs else "Minimal documentation",
            "has_docs_folder": any("docs/" in str(dir_structure.get("largest_directories", {})).lower()),
            "file_types_detected": list(dir_structure.get("file_types", {}).keys()),
            "documentation_completeness": self._assess_documentation_completeness(readme, dir_structure)
        })
        
        return enhanced
    
    def _process_activity_enhanced(self, commits: List, issues: List, pull_requests: List, releases: List,
                                 commit_patterns: Dict, issue_analysis: Dict) -> Dict[str, Any]:
        """Enhanced development activity analysis"""
        base_activity = self._process_activity(commits, issues, pull_requests, releases)
        
        enhanced = base_activity.copy()
        enhanced.update({
            "commit_analysis": commit_patterns,
            "issue_health": issue_analysis.get("issue_analysis", {}),
            "pr_health": issue_analysis.get("pr_analysis", {}),
            "project_velocity": self._calculate_project_velocity(commits, issues, pull_requests),
            "contributor_diversity": commit_patterns.get("unique_authors", 0),
            "development_consistency": self._assess_development_consistency(commit_patterns)
        })
        
        return enhanced
    
    def _process_technical_debt_enhanced(self, repo_info: Dict, languages: Dict, deep_deps: Dict, issue_analysis: Dict) -> Dict[str, Any]:
        """Enhanced technical debt analysis"""
        base_debt = self._process_technical_debt(repo_info, languages, deep_deps)
        
        # Analyze security concerns from dependencies
        security_score = self._calculate_security_score(deep_deps, issue_analysis)
        
        enhanced = base_debt.copy()
        enhanced.update({
            "dependency_analysis": {
                "total_dependencies": deep_deps.get("dependency_count", 0),
                "package_managers": len(deep_deps.get("package_managers", [])),
                "security_score": security_score
            },
            "maintenance_indicators": self._get_maintenance_indicators(repo_info, issue_analysis),
            "scalability_assessment": self._assess_scalability(deep_deps, repo_info),
            "refactoring_priorities": self._identify_refactoring_priorities(issue_analysis, deep_deps)
        })
        
        return enhanced
    
    # Helper methods for enhanced analysis
    def _detect_build_system_enhanced(self, package_json: Dict, requirements_txt: str, dir_structure: Dict) -> str:
        """Enhanced build system detection"""
        patterns = dir_structure.get("structure_patterns", [])
        file_types = dir_structure.get("file_types", {})
        
        if package_json:
            if "webpack" in str(package_json.get("devDependencies", {})):
                return "Webpack + Node.js"
            elif "vite" in str(package_json.get("devDependencies", {})):
                return "Vite + Node.js"
            elif "next" in str(package_json.get("dependencies", {})):
                return "Next.js"
            elif "react" in str(package_json.get("dependencies", {})):
                return "React application"
            else:
                return "Node.js/NPM"
        elif requirements_txt:
            if "django" in requirements_txt.lower():
                return "Django (Python)"
            elif "flask" in requirements_txt.lower():
                return "Flask (Python)"
            elif "fastapi" in requirements_txt.lower():
                return "FastAPI (Python)"
            else:
                return "Python/pip"
        elif "go" in file_types:
            return "Go modules"
        elif "rs" in file_types:
            return "Rust/Cargo"
        else:
            return "Unknown build system"
    
    def _assess_documentation_completeness(self, readme: str, dir_structure: Dict) -> str:
        """Assess documentation completeness"""
        score = 0
        
        if readme and len(readme) > 100:
            score += 30
        
        patterns = dir_structure.get("structure_patterns", [])
        if any("documented" in pattern.lower() for pattern in patterns):
            score += 40
        
        if any("docs/" in str(dir_structure.get("largest_directories", {})).lower()):
            score += 30
        
        if score >= 80:
            return "Comprehensive"
        elif score >= 50:
            return "Good"
        elif score >= 30:
            return "Basic"
        else:
            return "Minimal"
    
    def _calculate_project_velocity(self, commits: List, issues: List, pull_requests: List) -> Dict[str, Any]:
        """Calculate project development velocity"""
        recent_commits = len([c for c in commits[:10]])  # Recent 10 commits
        open_issues = len([i for i in issues if i["state"] == "open"])
        merged_prs = len([pr for pr in pull_requests if pr.get("merged_at")])
        
        velocity_score = min(100, (recent_commits * 10) + (merged_prs * 5) - (open_issues * 2))
        
        return {
            "velocity_score": max(0, velocity_score),
            "recent_commits": recent_commits,
            "merged_prs": merged_prs,
            "velocity_status": "High" if velocity_score > 70 else "Medium" if velocity_score > 40 else "Low"
        }
    
    def _assess_development_consistency(self, commit_patterns: Dict) -> str:
        """Assess development consistency"""
        if not commit_patterns or "average_commits_per_day" not in commit_patterns:
            return "Unknown"
        
        daily_commits = commit_patterns.get("average_commits_per_day", 0)
        if daily_commits > 1:
            return "Very active"
        elif daily_commits > 0.5:
            return "Active"
        elif daily_commits > 0.1:
            return "Moderate"
        else:
            return "Low activity"
    
    def _calculate_security_score(self, deep_deps: Dict, issue_analysis: Dict) -> int:
        """Calculate security score based on dependencies and issues"""
        score = 70  # Base score
        
        # Dependency factors
        dep_count = deep_deps.get("dependency_count", 0)
        if dep_count > 100:
            score -= 10
        elif dep_count > 50:
            score -= 5
        
        # Multiple package managers might indicate complexity
        pkg_managers = len(deep_deps.get("package_managers", []))
        if pkg_managers > 2:
            score -= 5
        
        return max(0, min(100, score))
    
    def _get_maintenance_indicators(self, repo_info: Dict, issue_analysis: Dict) -> List[str]:
        """Get maintenance burden indicators"""
        indicators = []
        
        # Age-based indicators
        age_years = self._calculate_repo_age(repo_info.get("created_at"))
        if age_years > 5:
            indicators.append(f"Mature project ({age_years:.1f} years old)")
        
        # Issue-based indicators
        issue_data = issue_analysis.get("issue_analysis", {})
        if issue_data.get("open_issues", 0) > 50:
            indicators.append("High number of open issues")
        
        if issue_data.get("issue_resolution_rate", 0) < 50:
            indicators.append("Low issue resolution rate")
        
        # Size-based indicators
        if repo_info.get("size", 0) > 50000:  # > 50MB
            indicators.append("Large repository size")
        
        return indicators or ["No major maintenance concerns detected"]
    
    def _assess_scalability(self, deep_deps: Dict, repo_info: Dict) -> Dict[str, Any]:
        """Assess project scalability"""
        concerns = []
        opportunities = []
        
        # Dependency analysis
        dep_count = deep_deps.get("dependency_count", 0)
        if dep_count > 100:
            concerns.append("High dependency count may impact maintenance")
        
        pkg_managers = deep_deps.get("package_managers", [])
        if len(pkg_managers) > 1:
            opportunities.append("Multiple package managers enable flexible architecture")
        
        # Size analysis
        size_kb = repo_info.get("size", 0)
        if size_kb > 100000:
            concerns.append("Large repository size may impact clone/build times")
        
        return {
            "scalability_score": max(0, 100 - len(concerns) * 20),
            "concerns": concerns or ["No major scalability concerns"],
            "opportunities": opportunities or ["Standard scalability practices recommended"]
        }
    
    def _identify_refactoring_priorities(self, issue_analysis: Dict, deep_deps: Dict) -> List[str]:
        """Identify refactoring priorities based on analysis"""
        priorities = []
        
        # Issue-based priorities
        issue_data = issue_analysis.get("issue_analysis", {})
        if issue_data.get("open_issues", 0) > 20:
            priorities.append("Address backlog of open issues")
        
        # Dependency-based priorities
        if deep_deps.get("dependency_count", 0) > 50:
            priorities.append("Review and consolidate dependencies")
        
        # PR-based priorities
        pr_data = issue_analysis.get("pr_analysis", {})
        if pr_data.get("merge_rate", 0) < 50:
            priorities.append("Improve PR review and merge process")
        
        return priorities or ["Continue current development practices"]