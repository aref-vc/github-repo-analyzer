# GitHub Repository Analyzer 🔍

A powerful web application that provides deep, structured intelligence analysis of GitHub repositories. Transform any GitHub repository URL into comprehensive insights with AI-powered chat capabilities.

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-red)
![License](https://img.shields.io/badge/license-MIT-purple)

## ✨ Features

### 🔬 Deep Repository Analysis
- **Complete File Tree Analysis**: Recursive traversal with file type distribution
- **Architecture Pattern Detection**: Identifies MVC, Microservices, DDD, Component-Based patterns
- **Multi-Package Manager Support**: npm, pip, cargo, maven, gradle, and more
- **Code Quality Metrics**: Test coverage estimation, linting configuration detection
- **Temporal Activity Analysis**: Peak development hours, commit patterns, contributor distribution
- **Security Assessment**: Vulnerability scanning, dependency risks, security features
- **Technical Debt Indicators**: Code organization issues, maintenance burden analysis

### 🤖 AI-Powered Features
- **Gemini Chat Integration**: Ask questions about the analyzed repository
- **Smart Suggestions**: AI-generated questions based on analysis
- **Context-Aware Responses**: Leverages repository data for accurate answers

### 📊 Export Capabilities
- **JSON Export**: Complete structured data
- **CSV Export**: Tabular format for spreadsheets
- **PDF Export**: Professional reports with visualizations

### ⚡ Performance & Optimization
- **Smart Caching**: Reduces API calls and improves response time
- **Rate Limiting**: Protects against abuse
- **Optimized Analysis**: Parallel processing for faster results

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- GitHub Personal Access Token (optional but recommended)
- Gemini API Key (optional, for AI features)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/github-repo-analyzer.git
cd github-repo-analyzer
```

2. **Set up Python virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r backend/requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your tokens:
# - GITHUB_TOKEN: Your GitHub personal access token
# - GEMINI_API_KEY: Your Gemini API key (optional)
```

5. **Start the application**
```bash
cd backend
python app.py
```

6. **Open in browser**
Navigate to `http://localhost:3023`

## 🔑 Configuration

### GitHub Token (Recommended)
While the analyzer works with public repositories without authentication, a GitHub token provides:
- Higher API rate limits (5,000 vs 60 requests/hour)
- Access to private repositories
- More detailed analysis data

**To create a token:**
1. Go to [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Generate new token (classic)
3. Select `repo` scope
4. Add to `.env` file

### Gemini API Key (Optional)
Enables AI chat features:
1. Get key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env` file

## 📖 Usage

1. **Enter Repository URL**: Paste any GitHub repository URL
2. **Analyze**: Click "Analyze Repository" 
3. **Explore Results**: Navigate through structured insights
4. **Ask Questions**: Use AI chat for specific queries
5. **Export Data**: Download analysis in your preferred format

### Example Repositories to Try
- `https://github.com/facebook/react` - Large JavaScript project
- `https://github.com/python/cpython` - Python source code
- `https://github.com/microsoft/vscode` - TypeScript/Electron app
- `https://github.com/rust-lang/rust` - Systems programming language

## 🏗️ Architecture

```
github-repo-analyzer/
├── backend/
│   ├── app.py                 # FastAPI main application
│   ├── repo_processor.py      # Core analysis orchestrator
│   ├── deep_analyzer.py       # Deep analysis engine
│   ├── github_analyzer.py     # GitHub API client
│   ├── gemini_client.py       # AI integration
│   ├── cache.py              # Caching system
│   └── export_handler.py     # Export functionality
├── frontend/
│   ├── index.html            # Main UI
│   ├── app.js                # Frontend logic
│   └── styles.css            # Styling
└── tests/
    └── test_*.py             # Test suites
```

## 🔍 Analysis Capabilities

### Repository Metadata
- Basic info (stars, forks, issues, size)
- Language distribution
- License and topics
- Creation and update dates

### Code Structure
- File tree with type distribution
- Directory organization patterns
- Configuration file detection
- Test file identification

### Dependencies
- Direct and dev dependencies
- Version analysis
- Outdated package detection
- Security vulnerability warnings

### Development Activity
- Commit frequency patterns
- Peak development hours/days
- Contributor distribution
- PR merge velocity
- Issue resolution time

### Quality Metrics
- Test coverage estimation
- Documentation coverage
- CI/CD tool detection
- Code review processes
- Branch protection status

## 🛡️ Security

- **No sensitive data storage**: Tokens are never logged or cached
- **Secure API calls**: All GitHub API calls use HTTPS
- **Input validation**: Repository URLs are validated
- **Rate limiting**: Prevents abuse and ensures fair usage
- **Gitignore configured**: Prevents accidental token commits

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI powered by modern web technologies
- AI features via [Google Gemini](https://deepmind.google/technologies/gemini/)
- Data from [GitHub API](https://docs.github.com/en/rest)

## 📧 Contact

For questions or support, please open an issue on GitHub.

---
Made with ❤️ using Claude Code
