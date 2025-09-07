"""
Gemini AI client for repository analysis chat functionality.
Integrates with Google's Generative AI API to provide conversational Q&A about repositories.
"""

import google.generativeai as genai
from typing import Dict, Any, List, Optional
import json
import logging

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, api_key: str):
        """Initialize Gemini client with API key."""
        if not api_key:
            raise ValueError("Gemini API key is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def analyze_with_context(self, repository_data: Dict[str, Any], user_question: str) -> str:
        """
        Generate AI response about repository using Gemini with full repository context.
        
        Args:
            repository_data: Complete repository analysis data
            user_question: User's question about the repository
            
        Returns:
            AI-generated response about the repository
        """
        try:
            # Create comprehensive context from repository data
            context = self._build_repository_context(repository_data)
            
            # Construct the prompt
            prompt = f"""You are an expert software engineer and repository analyst. You have access to comprehensive analysis data about a GitHub repository. Answer the user's question based on this data.

REPOSITORY ANALYSIS DATA:
{context}

USER QUESTION: {user_question}

Please provide a detailed, accurate answer based on the repository data. Be specific and cite relevant information from the analysis. If the question cannot be answered from the available data, explain what additional information would be needed.

RESPONSE:"""

            # Generate response
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating Gemini response: {e}")
            return f"I apologize, but I encountered an error while processing your question: {str(e)}"
    
    def _build_repository_context(self, repo_data: Dict[str, Any]) -> str:
        """Build comprehensive context string from repository analysis data."""
        try:
            context_sections = []
            
            # Repository metadata
            if 'repository_metadata' in repo_data:
                metadata = repo_data['repository_metadata']
                context_sections.append(f"""
REPOSITORY METADATA:
- Repository: {metadata.get('repository_name', 'N/A')} 
- Owner: {metadata.get('repository_owner', 'N/A')}
- Primary Language: {metadata.get('primary_stack', 'N/A')}
- Stars: {metadata.get('stars', 0):,}
- Forks: {metadata.get('forks', 0):,}
- Contributors: {metadata.get('contributors', 0)}
- Size: {metadata.get('repository_size_kb', 0)} KB
- License: {metadata.get('license_type', 'N/A')}
- Created: {metadata.get('created_at', 'N/A')}
- Last Updated: {metadata.get('updated_at', 'N/A')}
- Description: {metadata.get('description', 'N/A')}
""")
            
            # Languages breakdown
            if 'languages' in repo_data:
                languages = repo_data['languages']
                if languages:
                    lang_list = [f"{lang}: {percent}%" for lang, percent in languages.items()]
                    context_sections.append(f"""
PROGRAMMING LANGUAGES:
{chr(10).join([f"- {lang}" for lang in lang_list])}
""")
            
            # Architecture synopsis
            if 'architecture_synopsis' in repo_data:
                arch = repo_data['architecture_synopsis']
                context_sections.append(f"""
ARCHITECTURE SYNOPSIS:
- Build System: {arch.get('build_system', 'N/A')}
- Directory Structure: {arch.get('directory_structure', 'N/A')}
- Dependencies: {arch.get('dependency_count', 0)}
- Core Dependencies: {', '.join(arch.get('core_dependencies', []))}
- Project Patterns: {', '.join(arch.get('project_patterns', []))}
""")
            
            # Code quality metrics
            if 'code_quality_metrics' in repo_data:
                quality = repo_data['code_quality_metrics']
                context_sections.append(f"""
CODE QUALITY METRICS:
- Testing Framework: {quality.get('testing_framework', 'N/A')}
- CI/CD Pipeline: {quality.get('ci_cd_pipeline_status', 'N/A')}
- Linting Standards: {quality.get('linting_standards', 'N/A')}
- Workflow Runs: {quality.get('automation_scope', 'N/A')}
- Recent Workflows: {', '.join(quality.get('recent_workflows', []))}
""")
            
            # Documentation analysis
            if 'documentation_analysis' in repo_data:
                docs = repo_data['documentation_analysis']
                context_sections.append(f"""
DOCUMENTATION ANALYSIS:
- Quality: {docs.get('documentation_quality', 'N/A')}
- Has Documentation Folder: {docs.get('has_documentation_folder', False)}
- README Summary: {docs.get('readme_summary', 'N/A')}
- Installation Instructions: {', '.join(docs.get('installation_instructions', []))}
""")
            
            # Development activity
            if 'development_activity' in repo_data:
                activity = repo_data['development_activity']
                context_sections.append(f"""
DEVELOPMENT ACTIVITY:
- Consistency: {activity.get('development_consistency', 'N/A')}
- Recent Commits: {activity.get('recent_commits', 0)}
- Commit Frequency: {activity.get('commit_frequency', 'N/A')}
- Open Issues: {activity.get('open_issues', 0)}
- Open Pull Requests: {activity.get('open_pull_requests', 0)}
- Active Contributors: {activity.get('contributor_activity', 'N/A')}
- Project Velocity: {activity.get('project_velocity', 'N/A')}
""")
            
            # Technical debt assessment
            if 'technical_debt_assessment' in repo_data:
                debt = repo_data['technical_debt_assessment']
                context_sections.append(f"""
TECHNICAL DEBT ASSESSMENT:
- Maintenance Burden: {debt.get('maintenance_burden', 'N/A')}
- Security Score: {debt.get('security_score', 'N/A')}
- Total Dependencies: {debt.get('total_dependencies', 0)}
- Scalability Score: {debt.get('scalability_score', 'N/A')}
- Maintenance Indicators: {', '.join(debt.get('maintenance_indicators', []))}
- Refactoring Priorities: {', '.join(debt.get('refactoring_priorities', []))}
""")
            
            # Project health score
            if 'project_health_score' in repo_data:
                context_sections.append(f"""
PROJECT HEALTH SCORE: {repo_data['project_health_score']}/100
""")
            
            return "\n".join(context_sections)
            
        except Exception as e:
            logger.error(f"Error building repository context: {e}")
            return f"Repository data available but context building failed: {str(e)}"
    
    def get_suggested_questions(self, repository_data: Dict[str, Any]) -> List[str]:
        """Generate suggested questions based on repository analysis."""
        try:
            context = self._build_repository_context(repository_data)
            
            prompt = f"""Based on this repository analysis data, suggest 5 insightful questions that a developer or stakeholder might ask about this repository. Focus on practical questions about code quality, architecture, maintenance, and development practices.

REPOSITORY DATA:
{context}

Generate exactly 5 questions, each on a new line, without numbering or bullets:"""

            response = self.model.generate_content(prompt)
            questions = [q.strip() for q in response.text.split('\n') if q.strip()]
            return questions[:5]  # Ensure exactly 5 questions
            
        except Exception as e:
            logger.error(f"Error generating suggested questions: {e}")
            return [
                "What is the overall code quality of this repository?",
                "How active is the development on this project?",
                "What are the main dependencies and potential risks?",
                "How well is this repository documented?",
                "What would be the main challenges in maintaining this codebase?"
            ]