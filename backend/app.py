"""
GitHub Repository Analyzer - FastAPI Backend
Main application server with health check and CORS configuration
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import uvicorn
from datetime import datetime
from github_analyzer import GitHubAnalyzer
from repo_processor import RepoProcessor
from gemini_client import GeminiClient
from cache import get_cache_stats, invalidate_repository_cache
from export_handler import export_handler

# Load environment variables
load_dotenv()

# Create rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour"]  # Default rate limit
)

# Create FastAPI app
app = FastAPI(
    title="GitHub Repository Analyzer",
    description="Analyze GitHub repositories and provide structured intelligence with chat capabilities",
    version="1.0.0"
)

# Add rate limit error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize GitHub analyzer and processor
github_analyzer = GitHubAnalyzer()
repo_processor = RepoProcessor(github_analyzer)

# Pydantic models
class AnalyzeRequest(BaseModel):
    repo_url: str

class ChatRequest(BaseModel):
    question: str
    analysis_data: dict
    gemini_api_key: str = None

class SuggestionsRequest(BaseModel):
    analysis_data: dict
    gemini_api_key: str = None

class ExportRequest(BaseModel):
    analysis_data: dict
    format: str = "json"  # json, csv, or pdf

# Serve static files (frontend) - Fix path resolution
frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")
if os.path.exists(frontend_dir):
    # Mount CSS and JS files
    app.mount("/styles.css", StaticFiles(directory=frontend_dir), name="styles")
    app.mount("/app.js", StaticFiles(directory=frontend_dir), name="app")

@app.get("/")
async def serve_frontend():
    """Serve the main frontend application"""
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "GitHub Repository Analyzer API", "status": "running"}

@app.get("/styles.css")
async def serve_styles():
    """Serve CSS file"""
    css_path = os.path.join(os.path.dirname(__file__), "../frontend/styles.css")
    return FileResponse(css_path, media_type="text/css")

@app.get("/app.js")
async def serve_javascript():
    """Serve JavaScript file"""
    js_path = os.path.join(os.path.dirname(__file__), "../frontend/app.js")
    return FileResponse(js_path, media_type="application/javascript")

@app.get("/visualizations.js")
async def serve_visualizations():
    """Serve Visualizations JavaScript file"""
    js_path = os.path.join(os.path.dirname(__file__), "../frontend/visualizations.js")
    return FileResponse(js_path, media_type="application/javascript")

@app.get("/favicon.ico")
async def serve_favicon():
    """Serve favicon or return empty response"""
    return {"detail": "No favicon"}

@app.get("/health")
async def health_check():
    """Health check endpoint to verify server is running"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "GitHub Repository Analyzer",
        "version": "1.0.0",
        "environment": {
            "github_token_configured": bool(os.getenv("GITHUB_TOKEN")),
            "gemini_api_configured": bool(os.getenv("GEMINI_API_KEY")),
            "port": os.getenv("PORT", 3023),
            "debug": os.getenv("DEBUG", "false").lower() == "true"
        }
    }

@app.get("/api/status")
async def api_status():
    """API status endpoint with configuration details"""
    return {
        "api_version": "v1",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "analyze": "/api/analyze [POST] - Available",
            "chat": "/api/chat [POST] - Available",
            "suggestions": "/api/suggestions [POST] - Available",
            "cache_stats": "/api/cache/stats [GET] - Available",
            "cache_clear": "/api/cache/clear [POST] - Available",
            "export": "/api/export [POST] - Available (json/csv/pdf)"
        },
        "milestone": "6 - Performance Optimization & Caching"
    }

@app.get("/api/cache/stats")
async def cache_statistics():
    """Get cache statistics"""
    return {
        "success": True,
        "cache_stats": get_cache_stats(),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/cache/clear")
async def clear_cache():
    """Clear the cache"""
    invalidate_repository_cache("", "")  # Clear all
    return {
        "success": True,
        "message": "Cache cleared successfully",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/analyze")
@limiter.limit("10 per hour")  # Limit analysis to 10 per hour per IP
async def analyze_repository(request: Request, analyze_request: AnalyzeRequest):
    """Analyze a GitHub repository and return structured intelligence"""
    try:
        # Note: We can analyze public repositories without a token (with rate limits)
        # But having a token provides much higher rate limits
        if not github_analyzer.token:
            print("⚠️ No GitHub token configured - using anonymous access (rate limited)")
        
        # Analyze repository
        print(f"🔍 Starting analysis of: {analyze_request.repo_url}")
        analysis = repo_processor.analyze_repository(analyze_request.repo_url)
        print(f"✅ Analysis complete for: {analyze_request.repo_url}")
        
        return {
            "success": True,
            "repo_url": analyze_request.repo_url,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        error_msg = str(e) if str(e) else f"Analysis failed for unknown reason: {type(e).__name__}"
        print(f"❌ Analysis failed: {error_msg}")
        raise HTTPException(status_code=400, detail=error_msg)

@app.post("/api/chat")
@limiter.limit("30 per hour")  # Chat is less resource-intensive
async def chat_about_repository(request: Request, chat_request: ChatRequest):
    """Chat with AI about repository analysis results using Gemini"""
    try:
        # Get API key from request or environment
        api_key = chat_request.gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=400, 
                detail="Gemini API key is required. Provide it in the request or set GEMINI_API_KEY environment variable."
            )
        
        # Initialize Gemini client
        gemini_client = GeminiClient(api_key)
        
        # Generate response
        print(f"🤖 Processing chat question: {chat_request.question[:100]}...")
        response = gemini_client.analyze_with_context(chat_request.analysis_data, chat_request.question)
        print(f"✅ Chat response generated successfully")
        
        return {
            "success": True,
            "question": chat_request.question,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        error_msg = str(e) if str(e) else f"Chat failed for unknown reason: {type(e).__name__}"
        print(f"❌ Chat failed: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/api/suggestions")
@limiter.limit("20 per hour")
async def get_suggested_questions(request: Request, suggestions_request: SuggestionsRequest):
    """Get AI-suggested questions based on repository analysis"""
    try:
        # Get API key from request or environment
        api_key = suggestions_request.gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=400, 
                detail="Gemini API key is required. Provide it in the request or set GEMINI_API_KEY environment variable."
            )
        
        # Initialize Gemini client
        gemini_client = GeminiClient(api_key)
        
        # Generate suggested questions
        print("🤖 Generating suggested questions...")
        suggestions = gemini_client.get_suggested_questions(suggestions_request.analysis_data)
        print(f"✅ Generated {len(suggestions)} suggested questions")
        
        return {
            "success": True,
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        error_msg = str(e) if str(e) else f"Suggestions generation failed for unknown reason: {type(e).__name__}"
        print(f"❌ Suggestions failed: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/api/export")
@limiter.limit("20 per hour")
async def export_analysis(request: Request, export_request: ExportRequest):
    """Export analysis data in various formats"""
    try:
        format_type = export_request.format.lower()
        
        if format_type == "json":
            # Export as JSON
            json_data = export_handler.export_json(export_request.analysis_data)
            return Response(
                content=json_data,
                media_type="application/json",
                headers={
                    "Content-Disposition": f"attachment; filename=repo_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                }
            )
        
        elif format_type == "csv":
            # Export as CSV
            csv_data = export_handler.export_csv(export_request.analysis_data)
            return Response(
                content=csv_data,
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename=repo_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                }
            )
        
        elif format_type == "pdf":
            # Export as PDF
            pdf_data = export_handler.export_pdf(export_request.analysis_data)
            return Response(
                content=pdf_data,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename=repo_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                }
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported export format: {format_type}. Use json, csv, or pdf")
        
    except HTTPException as he:
        raise he
    except Exception as e:
        error_msg = str(e) if str(e) else f"Export failed for unknown reason: {type(e).__name__}"
        print(f"❌ Export failed: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3023))
    host = os.getenv("HOST", "localhost")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🚀 Starting GitHub Repository Analyzer on http://{host}:{port}")
    print(f"📋 Health Check: http://{host}:{port}/health")
    print(f"🔧 API Status: http://{host}:{port}/api/status")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )