# GitHub Repository Analyzer - Claude Configuration

## Project Overview
A comprehensive GitHub repository analysis tool that provides deep insights into repository structure, codebase metrics, architecture patterns, and AI-powered chat interface for exploring repository details.

## Project Status
- **Version**: 3.0
- **Status**: Production Ready
- **Repository**: https://github.com/aref-vc/github-repo-analyzer
- **Port**: 3023

## Key Features
- 🔍 Deep repository analysis with GitHub API integration
- 🏗️ Architecture pattern detection
- 📊 Comprehensive metrics and visualizations
- 💬 AI-powered chat with Gemini integration
- 🎨 Dark glassmorphism UI design
- 📝 Full markdown rendering support
- ⚡ Performance optimized with caching

## Technology Stack

### Backend
- **Python 3.8+** with FastAPI framework
- **Uvicorn** ASGI server
- **httpx** for async HTTP requests
- **google-generativeai** for Gemini chat
- **Pydantic** for data validation
- **python-dotenv** for environment management

### Frontend
- **Vanilla JavaScript** (ES6+)
- **HTML5** with semantic structure
- **CSS3** with CSS variables and glassmorphism
- **Chart.js** for data visualizations
- **Fetch API** for backend communication

## Critical Files

### Configuration
- `.env` - Contains sensitive tokens (GITHUB_TOKEN, GEMINI_API_KEY)
- `.gitignore` - Security-focused ignore patterns
- `requirements.txt` - Python dependencies

### Backend Components
- `backend/app.py` - FastAPI server with CORS, rate limiting
- `backend/repo_processor.py` - Main analysis orchestrator
- `backend/deep_analyzer.py` - Deep GitHub API integration
- `backend/enhanced_analyzer.py` - Enhanced metrics analysis
- `backend/optimized_analyzer.py` - Performance optimized analyzer
- `backend/github_analyzer.py` - GitHub API client wrapper
- `backend/gemini_client.py` - AI chat integration
- `backend/export_handler.py` - Data export functionality

### Frontend Components
- `frontend/index.html` - Main UI structure
- `frontend/app.js` - Controller with markdown parser
- `frontend/styles.css` - Dark theme with glassmorphism

## Environment Variables
```bash
# Required in .env file
GITHUB_TOKEN=ghp_... # GitHub personal access token
GEMINI_API_KEY=AIza... # Google Gemini API key
```

## Common Commands

### Start Server
```bash
cd "/Users/aref/Documents/Claude Code/GitHub-Repo-Analyzer/backend"
source ../venv/bin/activate
python app.py
```

### Install Dependencies
```bash
cd "/Users/aref/Documents/Claude Code/GitHub-Repo-Analyzer"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Git Operations
```bash
# Create new version tag
git tag -a vX.X -m "Version X.X: Description"
git push origin vX.X

# Push changes
git add .
git commit -m "feat: description"
git push origin main
```

## API Endpoints
- `GET /` - Serve frontend
- `GET /health` - Health check
- `POST /api/analyze` - Analyze repository
- `POST /api/chat` - AI chat interface
- `POST /api/suggestions` - Get AI suggestions
- `POST /api/export` - Export analysis data
- `GET /api/cache/stats` - Cache statistics
- `POST /api/cache/clear` - Clear cache

## Rate Limits
- General API: 100 requests/hour
- Analysis endpoint: 10 requests/hour
- GitHub API: 5000 requests/hour (authenticated)

## Version History

### v3.0 (Current)
- ✅ Comprehensive markdown parser for chat interface
- ✅ Support for all markdown formatting (bold, italic, code, lists, headers, links)
- ✅ XSS prevention with HTML escaping
- ✅ Proper paragraph and line break handling

### v2.0
- ✅ Dark theme UI with solid background (#211D49)
- ✅ Improved readability with orange category labels
- ✅ Fixed visibility issues on dark background
- ✅ Enhanced glassmorphism effects

### v1.0
- ✅ Initial release with deep repository analysis
- ✅ Fixed TBD placeholders with actual GitHub data
- ✅ Fixed Counter object handling bug
- ✅ Complete GitHub integration with token authentication

## Known Issues & Solutions

### Issue: "unhashable type: 'slice'" error
**Solution**: Fixed in v1.0 - Added isinstance check for Counter objects in repo_processor.py:311

### Issue: 401 Unauthorized GitHub API
**Solution**: Ensure full GitHub token is in .env file (not truncated)

### Issue: Markdown not rendering in chat
**Solution**: Fixed in v3.0 - Comprehensive markdown parser in app.js

### Issue: Dark theme visibility
**Solution**: Fixed in v2.0 - Adjusted color scheme for proper contrast

## Development Notes

### Markdown Parser Features
The chat interface supports:
- **Bold text**: `**text**` or `__text__`
- **Italic text**: `*text*` or `_text_`
- **Code blocks**: ` ```language...``` `
- **Inline code**: `` `code` ``
- **Headers**: `# H1` through `###### H6`
- **Lists**: `- item` or `* item` or `1. item`
- **Links**: `[text](url)`
- **Line breaks**: Proper `<br>` handling
- **Paragraphs**: Double newline separation

### Security Considerations
- GitHub token never exposed in frontend
- All sensitive data in .env (gitignored)
- XSS prevention in markdown parser
- CORS properly configured
- Rate limiting on all endpoints

### Performance Optimizations
- In-memory caching with 1-hour TTL
- Parallel API requests where possible
- Smart sampling for large repositories
- Async operations throughout

## Troubleshooting

### Server won't start
1. Check virtual environment is activated
2. Verify all dependencies installed
3. Ensure .env file has valid tokens
4. Check port 3023 is not in use

### Analysis fails
1. Verify GitHub token has repo scope
2. Check repository URL format
3. Ensure internet connectivity
4. Review rate limit status

### Chat not working
1. Verify Gemini API key is valid
2. Check browser console for errors
3. Ensure markdown parser loaded
4. Test with simple messages first

## Future Enhancements
- [ ] WebSocket support for real-time updates
- [ ] Multi-repository comparison
- [ ] Historical analysis tracking
- [ ] Advanced visualization options
- [ ] Export to multiple formats
- [ ] Custom analysis plugins

## Contact & Support
- Repository: https://github.com/aref-vc/github-repo-analyzer
- Issues: Report at GitHub Issues
- Version: 3.0
- Last Updated: 2025-09-07