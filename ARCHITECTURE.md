# Architecture Documentation

## System Overview

The GitHub Repository Analyzer is a full-stack web application that provides comprehensive analysis of GitHub repositories. It follows a modular, layered architecture with clear separation of concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (UI Layer)                   │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  index.html │  │    app.js    │  │   styles.css     │  │
│  │  (UI Shell) │  │ (Controller) │  │  (Presentation)  │  │
│  │   Tabbed UI │  │ Tab Manager  │  │  Glassmorphism   │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           visualizations.js (Visualization Suite)      │ │
│  │  Chart.js & D3.js powered interactive visualizations   │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (API Layer)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    FastAPI (app.py)                   │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │  │
│  │  │ Routing  │  │   CORS   │  │  Rate Limiting   │  │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Processing Layer (Core Logic)                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              RepoProcessor (Orchestrator)             │  │
│  └──────────────────────────────────────────────────────┘  │
│         │              │              │            │         │
│         ▼              ▼              ▼            ▼         │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌─────────┐ │
│  │DeepAnalyzer│ │  Enhanced  │ │ Optimized  │ │  Export │ │
│  │            │ │  Analyzer  │ │  Analyzer  │ │ Handler │ │
│  └────────────┘ └────────────┘ └────────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Integration Layer                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────┐  │
│  │ GitHubAnalyzer   │  │  GeminiClient    │  │  Cache   │  │
│  │ (GitHub API)     │  │  (AI Chat)       │  │  System  │  │
│  └──────────────────┘  └──────────────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Services                         │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │   GitHub API     │  │   Gemini API     │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Layer

#### index.html
- **Purpose**: Main UI shell with tabbed interface
- **Responsibilities**: 
  - Tabbed layout (Analysis, Visualizations, AI Assistant)
  - Component containers
  - User input forms
  - Tab navigation structure

#### app.js
- **Purpose**: Frontend controller with tab management
- **Responsibilities**:
  - API communication
  - DOM manipulation
  - Tab switching logic
  - Event handling
  - State management
  - Export functionality
  - Lazy loading visualizations

#### styles.css
- **Purpose**: Visual presentation with glassmorphism
- **Responsibilities**:
  - Dark theme (#211D49 background)
  - Glassmorphism effects
  - Tab navigation styling
  - Responsive design
  - Smooth transitions
  - Component styling

#### visualizations.js (New in v3.2)
- **Purpose**: Advanced data visualization suite
- **Responsibilities**:
  - Dependency graph (D3.js force-directed)
  - Code complexity heatmap
  - Contribution timeline (Chart.js line)
  - Language distribution (Chart.js donut)
  - File size treemap (D3.js)
  - Activity calendar heatmap
  - Issue/PR trends
  - Commit hour distribution
- **Key Features**:
  - Lazy loading on tab activation
  - Responsive chart sizing
  - Interactive tooltips
  - Dark theme optimized colors

### Backend Layer

#### app.py (FastAPI Application)
- **Purpose**: API server and request handling
- **Key Features**:
  - RESTful endpoints
  - CORS configuration
  - Rate limiting (100/hour default, 10/hour for analysis)
  - Static file serving
  - Request validation

**Endpoints**:
- `GET /` - Serve frontend
- `GET /health` - Health check
- `POST /api/analyze` - Repository analysis
- `POST /api/chat` - AI chat
- `POST /api/suggestions` - AI suggestions
- `POST /api/export` - Export data
- `GET /api/cache/stats` - Cache statistics
- `POST /api/cache/clear` - Clear cache

### Processing Layer

#### RepoProcessor
- **Purpose**: Orchestrate analysis workflow
- **Responsibilities**:
  - Coordinate analyzers
  - Aggregate results
  - Structure output
  - Handle errors

#### DeepAnalyzer
- **Purpose**: Comprehensive repository analysis
- **Key Features**:
  - Recursive file tree traversal
  - Architecture pattern detection
  - Dependency analysis
  - Activity pattern analysis
  - Security assessment
  - Technical debt identification

#### EnhancedAnalyzer
- **Purpose**: Enhanced analysis features
- **Features**:
  - Advanced metrics
  - Pattern recognition
  - Code quality assessment

#### OptimizedAnalyzer
- **Purpose**: Performance-optimized analysis
- **Features**:
  - Parallel processing
  - Smart sampling
  - Quick insights

### Integration Layer

#### GitHubAnalyzer
- **Purpose**: GitHub API client
- **Features**:
  - Rate limit handling
  - Token authentication
  - Retry logic
  - Request caching

#### GeminiClient
- **Purpose**: AI integration
- **Features**:
  - Context-aware responses
  - Question generation
  - Repository insights

#### Cache System
- **Purpose**: Performance optimization
- **Features**:
  - In-memory caching
  - TTL management (1 hour default)
  - Statistics tracking
  - Invalidation control

## Data Flow

1. **User Input**: Repository URL entered in frontend
2. **API Request**: Frontend sends POST to `/api/analyze`
3. **Validation**: Backend validates URL format
4. **Cache Check**: System checks for cached results
5. **GitHub API**: Fetch repository data if not cached
6. **Analysis Pipeline**:
   - Basic metadata extraction
   - Deep file tree analysis
   - Architecture detection
   - Dependency scanning
   - Activity analysis
   - Quality metrics
7. **Result Aggregation**: Combine all analysis results
8. **Cache Storage**: Store results with TTL
9. **Response**: Return structured JSON to frontend
10. **Display**: Frontend renders analysis results

## Security Architecture

### API Security
- **Rate Limiting**: Prevents abuse
- **Input Validation**: URL format checking
- **CORS Configuration**: Controlled cross-origin access
- **Token Management**: Secure GitHub token handling

### Sensitive Data Protection
- **Environment Variables**: Tokens in `.env` file
- **Gitignore**: Prevents credential commits
- **No Logging**: Sensitive data never logged
- **HTTPS Only**: Secure API communication

## Performance Optimization

### Caching Strategy
- **In-Memory Cache**: Fast access
- **TTL-Based**: 1-hour default expiration
- **Key-Based**: Repository-specific caching
- **Statistics**: Track hit/miss rates

### Parallel Processing
- **Concurrent API Calls**: Multiple GitHub endpoints
- **Async Operations**: Non-blocking I/O
- **Smart Sampling**: Analyze representative data

## Scalability Considerations

### Horizontal Scaling
- **Stateless Design**: No server-side sessions
- **External Cache**: Can use Redis/Memcached
- **Load Balancing**: Multiple instances supported

### Vertical Scaling
- **Async Processing**: Efficient resource usage
- **Memory Management**: Controlled cache size
- **Connection Pooling**: Reuse HTTP connections

## Technology Stack

### Backend
- **Python 3.8+**: Core language
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **httpx**: HTTP client
- **google-generativeai**: Gemini integration

### Frontend
- **HTML5**: Structure with semantic tabs
- **CSS3**: Glassmorphism styling
- **JavaScript (ES6+)**: Logic & tab controller
- **Fetch API**: HTTP requests
- **Chart.js v4.4.0**: Standard visualizations
- **D3.js v7**: Advanced visualizations

### Development Tools
- **Git**: Version control
- **pip**: Package management
- **venv**: Virtual environments
- **pytest**: Testing framework

## Deployment Architecture

### Local Development
```
localhost:3023
    │
    ├── Frontend (Static Files)
    └── Backend (FastAPI + Uvicorn)
```

### Production Deployment (Recommended)
```
Load Balancer
    │
    ├── Web Server (Nginx)
    │   └── Static Files
    │
    └── Application Servers
        ├── Instance 1 (FastAPI)
        ├── Instance 2 (FastAPI)
        └── Instance N (FastAPI)
            │
            └── Shared Cache (Redis)
```

## Error Handling

### Frontend
- User-friendly error messages
- Retry mechanisms
- Loading states
- Fallback UI

### Backend
- Structured error responses
- HTTP status codes
- Exception logging
- Graceful degradation

## Monitoring & Observability

### Metrics
- API response times
- Cache hit rates
- Error rates
- GitHub API usage

### Logging
- Request/response logging
- Error tracking
- Performance metrics
- User activity

## Future Enhancements

### Planned Features
- WebSocket support for real-time updates
- Background job processing
- Advanced visualizations
- Multi-repository comparison
- Historical analysis tracking
- Custom analysis plugins

### Architecture Evolution
- Microservices separation
- Message queue integration
- GraphQL API option
- Kubernetes deployment
- Multi-region support

---

*Last Updated: Version 3.2.0*
