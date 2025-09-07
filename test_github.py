#!/usr/bin/env python3
"""
Quick test script to debug GitHub API integration
"""
import os
import sys
sys.path.append('backend')

from backend.github_analyzer import GitHubAnalyzer
from backend.repo_processor import RepoProcessor

def test_github_integration():
    print("🧪 Testing GitHub Integration")
    print(f"GITHUB_TOKEN configured: {bool(os.getenv('GITHUB_TOKEN'))}")
    
    # Test without token first (should work for public repos with rate limits)
    github = GitHubAnalyzer(token=None)
    processor = RepoProcessor(github)
    
    try:
        print("📡 Testing basic API call...")
        owner, repo = github.parse_repo_url("https://github.com/octocat/Hello-World")
        print(f"Parsed URL: {owner}/{repo}")
        
        repo_info = github.get_repository_info(owner, repo)
        print(f"✅ Repository info fetched: {repo_info['name']}")
        print(f"Stars: {repo_info['stargazers_count']}")
        
        print("🔍 Testing full analysis...")
        analysis = processor.analyze_repository("https://github.com/octocat/Hello-World")
        print("✅ Full analysis completed!")
        print(f"Primary language: {analysis['repository_metadata']['primary_stack']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_github_integration()
    sys.exit(0 if success else 1)