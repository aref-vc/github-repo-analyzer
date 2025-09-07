#!/usr/bin/env python3
"""
Test script for enhanced analysis with performance monitoring
"""
import time
import sys
sys.path.append('backend')

from backend.github_analyzer import GitHubAnalyzer
from backend.enhanced_analyzer import EnhancedAnalyzer
from backend.repo_processor import RepoProcessor

def test_enhanced_performance():
    print("🧪 Testing Enhanced Analysis Performance")
    
    github = GitHubAnalyzer(token=None)
    enhanced = EnhancedAnalyzer(github)
    processor = RepoProcessor(github)
    
    repo_url = "https://github.com/octocat/Hello-World"
    owner, repo = github.parse_repo_url(repo_url)
    
    try:
        start_time = time.time()
        
        # Test basic GitHub API calls first
        print("📡 Testing basic API calls...")
        repo_info = github.get_repository_info(owner, repo)
        print(f"✅ Basic repo info: {time.time() - start_time:.2f}s")
        
        languages = github.get_languages(owner, repo)
        print(f"✅ Languages: {time.time() - start_time:.2f}s")
        
        contributors = github.get_contributors(owner, repo)
        print(f"✅ Contributors: {time.time() - start_time:.2f}s")
        
        commits = github.get_commits(owner, repo, limit=10)  # Reduced limit
        print(f"✅ Commits: {time.time() - start_time:.2f}s")
        
        # Test enhanced analysis components one by one
        print("\n🔬 Testing enhanced analysis components...")
        
        print("1. Directory structure analysis...")
        try:
            dir_structure = enhanced.analyze_directory_structure(owner, repo)
            print(f"✅ Directory structure: {time.time() - start_time:.2f}s")
        except Exception as e:
            print(f"❌ Directory structure failed: {e}")
        
        print("2. Dependencies analysis...")
        try:
            deep_deps = enhanced.analyze_dependencies_deep(owner, repo)
            print(f"✅ Dependencies: {time.time() - start_time:.2f}s")
        except Exception as e:
            print(f"❌ Dependencies failed: {e}")
        
        print("3. Code quality analysis...")
        try:
            code_quality = enhanced.analyze_code_quality_deep(owner, repo)
            print(f"✅ Code quality: {time.time() - start_time:.2f}s")
        except Exception as e:
            print(f"❌ Code quality failed: {e}")
        
        print("4. Commit patterns analysis...")
        try:
            commit_patterns = enhanced.analyze_commit_patterns_deep(owner, repo, commits)
            print(f"✅ Commit patterns: {time.time() - start_time:.2f}s")
        except Exception as e:
            print(f"❌ Commit patterns failed: {e}")
        
        print("5. Issue patterns analysis...")
        try:
            issue_analysis = enhanced.analyze_issue_patterns(owner, repo)
            print(f"✅ Issue patterns: {time.time() - start_time:.2f}s")
        except Exception as e:
            print(f"❌ Issue patterns failed: {e}")
        
        total_time = time.time() - start_time
        print(f"\n🎯 Total analysis time: {total_time:.2f}s")
        
        if total_time < 30:
            print("✅ Performance acceptable!")
            return True
        else:
            print("⚠️ Performance needs optimization")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_enhanced_performance()
    sys.exit(0 if success else 1)