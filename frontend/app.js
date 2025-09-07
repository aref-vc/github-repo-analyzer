/**
 * GitHub Repository Analyzer - Frontend JavaScript
 * Handles form validation, API communication, and dynamic UI updates
 */

class RepositoryAnalyzer {
    constructor() {
        this.apiBaseUrl = '/api';
        this.currentAnalysis = null;
        this.geminiApiKey = localStorage.getItem('gemini_api_key') || '';
        this.chatHistory = [];
        
        this.initializeEventListeners();
        this.initializeExamples();
        this.initializeChat();
    }

    /**
     * Initialize all event listeners
     */
    initializeEventListeners() {
        // Form submission
        const form = document.getElementById('analyzeForm');
        form.addEventListener('submit', (e) => this.handleFormSubmit(e));

        // Example buttons
        const exampleButtons = document.querySelectorAll('.example-btn');
        exampleButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleExampleClick(e));
        });

        // Control buttons
        document.getElementById('retryBtn').addEventListener('click', () => this.retryAnalysis());
        document.getElementById('newAnalysisBtn').addEventListener('click', () => this.startNewAnalysis());
        document.getElementById('toggleRawData').addEventListener('click', () => this.toggleRawData());

        // Input validation
        const repoInput = document.getElementById('repoUrl');
        repoInput.addEventListener('input', () => this.validateInput());
        repoInput.addEventListener('paste', () => {
            // Allow paste processing then validate
            setTimeout(() => this.validateInput(), 10);
        });
    }

    /**
     * Initialize example repository suggestions
     */
    initializeExamples() {
        const examples = [
            'https://github.com/fastapi/fastapi',
            'https://github.com/microsoft/vscode',
            'https://github.com/facebook/react'
        ];

        // Set random example as placeholder
        const repoInput = document.getElementById('repoUrl');
        const randomExample = examples[Math.floor(Math.random() * examples.length)];
        repoInput.placeholder = randomExample;
    }

    /**
     * Handle form submission
     */
    async handleFormSubmit(event) {
        event.preventDefault();
        
        const repoUrl = document.getElementById('repoUrl').value.trim();
        if (!this.isValidGitHubUrl(repoUrl)) {
            this.showError('Please enter a valid GitHub repository URL');
            return;
        }

        await this.analyzeRepository(repoUrl);
    }

    /**
     * Handle example button clicks
     */
    handleExampleClick(event) {
        const url = event.target.dataset.url;
        document.getElementById('repoUrl').value = url;
        this.validateInput();
    }

    /**
     * Validate GitHub URL input
     */
    validateInput() {
        const repoInput = document.getElementById('repoUrl');
        const submitBtn = document.getElementById('analyzeBtn');
        const url = repoInput.value.trim();

        if (url && !this.isValidGitHubUrl(url)) {
            repoInput.style.borderColor = 'var(--color-accent-3)';
            submitBtn.disabled = true;
        } else {
            repoInput.style.borderColor = url ? 'var(--color-accent-1)' : 'transparent';
            submitBtn.disabled = !url;
        }
    }

    /**
     * Validate GitHub URL format
     */
    isValidGitHubUrl(url) {
        const githubRegex = /^https?:\/\/(www\.)?github\.com\/[a-zA-Z0-9._-]+\/[a-zA-Z0-9._-]+\/?$/;
        return githubRegex.test(url);
    }

    /**
     * Analyze repository
     */
    async analyzeRepository(repoUrl) {
        this.showLoading();
        
        try {
            // Start progress animation
            this.animateProgress();
            
            const response = await fetch(`${this.apiBaseUrl}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ repo_url: repoUrl })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP ${response.status}`);
            }

            const data = await response.json();
            
            if (data.success) {
                this.currentAnalysis = data;
                this.showResults(data);
            } else {
                throw new Error('Analysis failed');
            }

        } catch (error) {
            console.error('Analysis error:', error);
            this.showError(`Analysis failed: ${error.message}`);
        }
    }

    /**
     * Show loading state with progress animation
     */
    showLoading() {
        this.hideAllSections();
        document.getElementById('loadingSection').classList.remove('hidden');
        
        // Reset progress
        document.getElementById('progressFill').style.width = '0%';
        this.resetProgressSteps();
    }

    /**
     * Animate progress bar and steps
     */
    animateProgress() {
        const progressFill = document.getElementById('progressFill');
        const steps = document.querySelectorAll('.step');
        const messages = [
            'Connecting to GitHub API...',
            'Fetching repository metadata...',
            'Analyzing code structure...',
            'Processing development activity...',
            'Calculating quality metrics...',
            'Finalizing analysis report...'
        ];

        let currentStep = 0;
        const progressInterval = setInterval(() => {
            if (currentStep >= steps.length) {
                clearInterval(progressInterval);
                return;
            }

            // Update progress bar
            const progress = ((currentStep + 1) / steps.length) * 100;
            progressFill.style.width = `${progress}%`;

            // Update step indicators
            if (currentStep > 0) {
                steps[currentStep - 1].classList.remove('active');
            }
            steps[currentStep].classList.add('active');

            // Update loading message
            if (currentStep < messages.length) {
                document.getElementById('loadingMessage').textContent = messages[currentStep];
            }

            currentStep++;
        }, 1000);

        // Clear animation after 30 seconds (fallback)
        setTimeout(() => clearInterval(progressInterval), 30000);
    }

    /**
     * Reset progress step indicators
     */
    resetProgressSteps() {
        const steps = document.querySelectorAll('.step');
        steps.forEach((step, index) => {
            step.classList.toggle('active', index === 0);
        });
    }

    /**
     * Show error state
     */
    showError(message) {
        this.hideAllSections();
        document.getElementById('errorSection').classList.remove('hidden');
        document.getElementById('errorMessage').textContent = message;
    }

    /**
     * Show analysis results
     */
    showResults(data) {
        this.hideAllSections();
        document.getElementById('resultsSection').classList.remove('hidden');

        // Update header info
        const analysis = data.analysis;
        const repoName = this.extractRepoName(data.repo_url);
        document.getElementById('repoTitle').textContent = `${repoName} Analysis`;
        document.getElementById('repoUrlDisplay').textContent = data.repo_url;
        document.getElementById('analysisTime').textContent = new Date(data.timestamp).toLocaleString();

        // Populate analysis sections
        this.populateMetadata(analysis.repository_metadata);
        this.populateArchitecture(analysis.architecture_synopsis);
        this.populateQuality(analysis.code_quality_metrics);
        this.populateDocumentation(analysis.documentation_extraction);
        this.populateActivity(analysis.development_activity);
        this.populateDebt(analysis.technical_debt_assessment);

        // Setup raw data
        document.getElementById('rawDataJson').textContent = JSON.stringify(analysis, null, 2);

        // Store current analysis for chat and export
        this.currentAnalysis = analysis;
        this.currentAnalysisData = analysis;

        // Initialize chat interface
        this.resetChatInterface();

        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    }

    /**
     * Extract repository name from URL
     */
    extractRepoName(url) {
        const match = url.match(/github\.com\/([^\/]+\/[^\/]+)/);
        return match ? match[1] : 'Repository';
    }

    /**
     * Populate metadata section
     */
    populateMetadata(metadata) {
        const content = document.getElementById('metadataContent');
        content.innerHTML = `
            <div class="data-item">
                <span class="data-label">Primary Language</span>
                <span class="data-value">${metadata.primary_stack || 'Unknown'}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Stars</span>
                <span class="data-value">${this.formatNumber(metadata.stars)}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Forks</span>
                <span class="data-value">${this.formatNumber(metadata.forks)}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Contributors</span>
                <span class="data-value">${metadata.contributor_count}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Repository Size</span>
                <span class="data-value">${this.formatSize(metadata.repository_size_kb)}</span>
            </div>
            <div class="data-item">
                <span class="data-label">License</span>
                <span class="data-value">${metadata.license_type || 'None'}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Created</span>
                <span class="data-value">${this.formatDate(metadata.created_date)}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Last Updated</span>
                <span class="data-value">${this.formatDate(metadata.last_updated)}</span>
            </div>
        `;
    }

    /**
     * Populate architecture section
     */
    populateArchitecture(architecture) {
        const content = document.getElementById('architectureContent');
        const deps = architecture.core_dependencies || [];
        const devDeps = architecture.dev_dependencies || [];
        
        content.innerHTML = `
            <div class="data-item">
                <span class="data-label">Build System</span>
                <span class="data-value">${architecture.build_system || 'Unknown'}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Directory Structure</span>
                <span class="data-value">${architecture.directory_structure || 'N/A'}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Dependencies</span>
                <span class="data-value">${architecture.dependency_count || deps.length}</span>
            </div>
            ${deps.length > 0 ? `
                <div style="margin-top: 1rem;">
                    <strong class="data-label">Core Dependencies:</strong>
                    <ul class="data-list">
                        ${deps.slice(0, 8).map(dep => `<li>${dep}</li>`).join('')}
                        ${deps.length > 8 ? `<li>...and ${deps.length - 8} more</li>` : ''}
                    </ul>
                </div>
            ` : ''}
            ${architecture.project_patterns ? `
                <div style="margin-top: 1rem;">
                    <strong class="data-label">Project Patterns:</strong>
                    <ul class="data-list">
                        ${architecture.project_patterns.map(pattern => `<li>${pattern}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        `;
    }

    /**
     * Populate quality section
     */
    populateQuality(quality) {
        const content = document.getElementById('qualityContent');
        content.innerHTML = `
            <div class="data-item">
                <span class="data-label">Testing Framework</span>
                <span class="data-value">${quality.testing_framework || 'Unknown'}</span>
            </div>
            <div class="data-item">
                <span class="data-label">CI/CD Pipeline</span>
                <span class="data-value">${quality.ci_cd_pipeline_status || 'Not detected'}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Linting Standards</span>
                <span class="data-value">${quality.linting_standards || 'Not detected'}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Automation Scope</span>
                <span class="data-value">${quality.automation_scope || 'None detected'}</span>
            </div>
            ${quality.recent_workflow_results && quality.recent_workflow_results.length > 0 ? `
                <div style="margin-top: 1rem;">
                    <strong class="data-label">Recent Workflows:</strong>
                    <ul class="data-list">
                        ${quality.recent_workflow_results.slice(0, 3).map(workflow => 
                            `<li>${workflow.name}: ${workflow.status}</li>`
                        ).join('')}
                    </ul>
                </div>
            ` : ''}
        `;
    }

    /**
     * Populate documentation section
     */
    populateDocumentation(docs) {
        const content = document.getElementById('documentationContent');
        content.innerHTML = `
            <div class="data-item">
                <span class="data-label">Documentation Quality</span>
                <span class="data-value">${docs.documentation_quality || docs.documentation_completeness || 'Unknown'}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Has Documentation Folder</span>
                <span class="data-value">${docs.has_docs_folder ? 'Yes' : 'No'}</span>
            </div>
            <div style="margin-top: 1rem;">
                <strong class="data-label">README Summary:</strong>
                <p style="margin-top: 0.5rem; color: var(--color-tertiary); font-size: var(--text-sm); line-height: 1.5;">
                    ${docs.readme_summary || 'No README summary available'}
                </p>
            </div>
            ${docs.installation_requirements && docs.installation_requirements.length > 0 ? `
                <div style="margin-top: 1rem;">
                    <strong class="data-label">Installation:</strong>
                    <ul class="data-list">
                        ${docs.installation_requirements.slice(0, 3).map(req => `<li>${req}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        `;
    }

    /**
     * Populate activity section
     */
    populateActivity(activity) {
        const content = document.getElementById('activityContent');
        content.innerHTML = `
            <div class="data-item">
                <span class="data-label">Development Consistency</span>
                <span class="data-value">${activity.development_consistency || 'Unknown'}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Recent Commits</span>
                <span class="data-value">${activity.recent_commit_patterns || 'No data'}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Commit Frequency</span>
                <span class="data-value">${activity.commit_frequency_per_day || 0} per day</span>
            </div>
            <div class="data-item">
                <span class="data-label">Open Issues</span>
                <span class="data-value">${activity.open_issues_count || 0}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Open Pull Requests</span>
                <span class="data-value">${activity.open_pull_requests || 0}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Contributor Activity</span>
                <span class="data-value">${activity.contributor_activity || 'No data'}</span>
            </div>
            ${activity.project_velocity ? `
                <div class="data-item">
                    <span class="data-label">Project Velocity</span>
                    <span class="data-value">${activity.project_velocity.velocity_status || 'Unknown'}</span>
                </div>
            ` : ''}
        `;
    }

    /**
     * Populate technical debt section
     */
    populateDebt(debt) {
        const content = document.getElementById('debtContent');
        const indicators = debt.debt_indicators || debt.maintenance_indicators || [];
        
        content.innerHTML = `
            <div class="data-item">
                <span class="data-label">Maintenance Burden</span>
                <span class="data-value">${debt.maintenance_burden || 'Unknown'}</span>
            </div>
            ${debt.dependency_analysis ? `
                <div class="data-item">
                    <span class="data-label">Security Score</span>
                    <span class="data-value">${debt.dependency_analysis.security_score}/100</span>
                </div>
                <div class="data-item">
                    <span class="data-label">Total Dependencies</span>
                    <span class="data-value">${debt.dependency_analysis.total_dependencies || 0}</span>
                </div>
            ` : ''}
            ${debt.scalability_assessment ? `
                <div class="data-item">
                    <span class="data-label">Scalability Score</span>
                    <span class="data-value">${debt.scalability_assessment.scalability_score}/100</span>
                </div>
            ` : ''}
            ${indicators.length > 0 ? `
                <div style="margin-top: 1rem;">
                    <strong class="data-label">Maintenance Indicators:</strong>
                    <ul class="data-list">
                        ${indicators.slice(0, 5).map(indicator => `<li>${indicator}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            ${debt.refactoring_priorities && debt.refactoring_priorities.length > 0 ? `
                <div style="margin-top: 1rem;">
                    <strong class="data-label">Refactoring Priorities:</strong>
                    <ul class="data-list">
                        ${debt.refactoring_priorities.slice(0, 3).map(priority => `<li>${priority}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        `;
    }

    /**
     * Hide all main sections
     */
    hideAllSections() {
        document.getElementById('loadingSection').classList.add('hidden');
        document.getElementById('errorSection').classList.add('hidden');
        document.getElementById('resultsSection').classList.add('hidden');
    }

    /**
     * Retry analysis
     */
    retryAnalysis() {
        const repoUrl = document.getElementById('repoUrl').value.trim();
        if (repoUrl) {
            this.analyzeRepository(repoUrl);
        }
    }

    /**
     * Start new analysis
     */
    startNewAnalysis() {
        this.hideAllSections();
        document.getElementById('repoUrl').value = '';
        document.getElementById('repoUrl').focus();
    }

    /**
     * Toggle raw data display
     */
    toggleRawData() {
        const rawDataContent = document.getElementById('rawDataContent');
        const toggleBtn = document.getElementById('toggleRawData');
        
        if (rawDataContent.classList.contains('hidden')) {
            rawDataContent.classList.remove('hidden');
            toggleBtn.querySelector('.btn-text').textContent = 'Hide Raw Analysis Data';
            toggleBtn.querySelector('.btn-icon').textContent = '🔽';
        } else {
            rawDataContent.classList.add('hidden');
            toggleBtn.querySelector('.btn-text').textContent = 'View Raw Analysis Data';
            toggleBtn.querySelector('.btn-icon').textContent = '🔧';
        }
    }

    /**
     * Format numbers with commas
     */
    formatNumber(num) {
        return new Intl.NumberFormat().format(num);
    }

    /**
     * Format file sizes
     */
    formatSize(kb) {
        if (kb < 1024) return `${kb} KB`;
        if (kb < 1024 * 1024) return `${(kb / 1024).toFixed(1)} MB`;
        return `${(kb / (1024 * 1024)).toFixed(1)} GB`;
    }

    /**
     * Format dates
     */
    formatDate(dateString) {
        if (!dateString) return 'Unknown';
        return new Date(dateString).toLocaleDateString();
    }

    /**
     * Initialize chat functionality
     */
    initializeChat() {
        // Load saved API key
        const apiKeyInput = document.getElementById('geminiApiKey');
        if (this.geminiApiKey) {
            apiKeyInput.value = this.geminiApiKey;
            this.showChatInterface();
        }

        // Chat event listeners
        document.getElementById('saveApiKeyBtn').addEventListener('click', () => this.saveApiKey());
        document.getElementById('chatForm').addEventListener('submit', (e) => this.handleChatSubmit(e));
        document.getElementById('refreshSuggestions').addEventListener('click', () => this.loadSuggestions());

        // Textarea auto-resize
        const textarea = document.getElementById('chatInput');
        textarea.addEventListener('input', () => this.autoResizeTextarea(textarea));
    }

    /**
     * Save Gemini API key to localStorage and enable chat
     */
    saveApiKey() {
        const apiKeyInput = document.getElementById('geminiApiKey');
        const apiKey = apiKeyInput.value.trim();

        if (!apiKey) {
            this.showError('Please enter a valid Gemini API key');
            return;
        }

        this.geminiApiKey = apiKey;
        localStorage.setItem('gemini_api_key', apiKey);
        
        this.showChatInterface();
        this.loadSuggestions();
    }

    /**
     * Show chat interface and load suggestions
     */
    showChatInterface() {
        if (!this.currentAnalysis) return;

        document.getElementById('suggestionsSection').classList.remove('hidden');
        document.getElementById('chatInterface').classList.remove('hidden');
        
        // Hide API key config if key is saved
        if (this.geminiApiKey) {
            document.getElementById('chatConfig').style.display = 'none';
        }
    }

    /**
     * Load suggested questions from AI
     */
    async loadSuggestions() {
        if (!this.currentAnalysis || !this.geminiApiKey) return;

        try {
            const response = await fetch(`${this.apiBaseUrl}/suggestions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    analysis_data: this.currentAnalysis,
                    gemini_api_key: this.geminiApiKey
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to generate suggestions');
            }

            this.displaySuggestions(data.suggestions);

        } catch (error) {
            console.error('Error loading suggestions:', error);
            this.showError(`Failed to load suggestions: ${error.message}`);
        }
    }

    /**
     * Display suggested questions
     */
    displaySuggestions(suggestions) {
        const suggestionsGrid = document.getElementById('suggestionsGrid');
        suggestionsGrid.innerHTML = '';

        suggestions.forEach((suggestion, index) => {
            const suggestionBtn = document.createElement('button');
            suggestionBtn.className = 'suggestion-btn';
            suggestionBtn.textContent = suggestion;
            suggestionBtn.addEventListener('click', () => {
                document.getElementById('chatInput').value = suggestion;
                document.getElementById('chatInput').focus();
            });
            suggestionsGrid.appendChild(suggestionBtn);
        });
    }

    /**
     * Handle chat form submission
     */
    async handleChatSubmit(e) {
        e.preventDefault();

        const chatInput = document.getElementById('chatInput');
        const question = chatInput.value.trim();

        if (!question || !this.currentAnalysis || !this.geminiApiKey) {
            return;
        }

        // Add user message to chat
        this.addMessageToChat('user', question);
        chatInput.value = '';
        this.autoResizeTextarea(chatInput);

        // Show loading
        this.showChatLoading(true);

        try {
            const response = await fetch(`${this.apiBaseUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: question,
                    analysis_data: this.currentAnalysis,
                    gemini_api_key: this.geminiApiKey
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Chat request failed');
            }

            // Add AI response to chat
            this.addMessageToChat('ai', data.response);

        } catch (error) {
            console.error('Error in chat:', error);
            this.addMessageToChat('ai', `I apologize, but I encountered an error: ${error.message}`);
        } finally {
            this.showChatLoading(false);
        }
    }

    /**
     * Add message to chat interface
     */
    addMessageToChat(sender, message) {
        const chatMessages = document.getElementById('chatMessages');
        
        const messageElement = document.createElement('div');
        messageElement.className = `chat-message ${sender}`;
        
        const messageContent = document.createElement('p');
        messageContent.className = 'message-content';
        messageContent.textContent = message;
        
        const timestamp = document.createElement('div');
        timestamp.className = 'message-timestamp';
        timestamp.textContent = new Date().toLocaleTimeString();
        
        messageElement.appendChild(messageContent);
        messageElement.appendChild(timestamp);
        chatMessages.appendChild(messageElement);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Store in history
        this.chatHistory.push({ sender, message, timestamp: new Date().toISOString() });
    }

    /**
     * Show/hide chat loading state
     */
    showChatLoading(show) {
        const loadingElement = document.getElementById('chatLoading');
        const chatInterface = document.getElementById('chatInterface');
        
        if (show) {
            loadingElement.classList.remove('hidden');
            chatInterface.style.opacity = '0.6';
            document.getElementById('sendChatBtn').disabled = true;
        } else {
            loadingElement.classList.add('hidden');
            chatInterface.style.opacity = '1';
            document.getElementById('sendChatBtn').disabled = false;
        }
    }

    /**
     * Auto-resize textarea based on content
     */
    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    /**
     * Export analysis in specified format
     */
    async exportAnalysis(format) {
        if (!this.currentAnalysisData) {
            alert('No analysis data available to export');
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/export`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    analysis_data: this.currentAnalysisData,
                    format: format
                })
            });
            
            if (!response.ok) {
                throw new Error(`Export failed: ${response.statusText}`);
            }
            
            // Get filename from Content-Disposition header
            const contentDisposition = response.headers.get('Content-Disposition');
            const filenameMatch = contentDisposition?.match(/filename=(.+)/);
            const filename = filenameMatch ? filenameMatch[1] : `analysis.${format}`;
            
            // Download the file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            // Show success message
            this.showExportSuccess(format);
            
        } catch (error) {
            console.error('Export error:', error);
            alert(`Failed to export as ${format.toUpperCase()}: ${error.message}`);
        }
    }
    
    /**
     * Show export success message
     */
    showExportSuccess(format) {
        const message = document.createElement('div');
        message.className = 'export-success';
        message.textContent = `✅ Analysis exported as ${format.toUpperCase()}`;
        message.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--color-accent-1);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(message);
        
        setTimeout(() => {
            message.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => document.body.removeChild(message), 300);
        }, 3000);
    }

    /**
     * Reset chat interface for new analysis
     */
    resetChatInterface() {
        this.chatHistory = [];
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = '';
        
        document.getElementById('chatInput').value = '';
        document.getElementById('suggestionsGrid').innerHTML = '';
        
        if (this.geminiApiKey && this.currentAnalysis) {
            this.showChatInterface();
            this.loadSuggestions();
        }
    }
}

// Initialize the application when DOM is loaded
let app; // Global reference for export buttons
document.addEventListener('DOMContentLoaded', () => {
    app = new RepositoryAnalyzer();
});