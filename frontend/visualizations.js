/**
 * Advanced Visualization Suite for GitHub Repository Analyzer
 * Provides interactive charts and graphs for repository data
 */

class VisualizationSuite {
    constructor() {
        this.charts = {};
        this.colors = {
            primary: '#8D5EB7',
            secondary: '#6F68BD',
            accent: '#E56C48',
            success: '#4CAF50',
            warning: '#E69780',
            dark: '#211D49',
            light: '#F9F9F9',
            chartColors: [
                '#8D5EB7', '#6F68BD', '#E56C48', '#E69780', 
                '#4CAF50', '#2196F3', '#FF9800', '#9C27B0',
                '#00BCD4', '#CDDC39', '#795548', '#607D8B'
            ]
        };
    }

    /**
     * Initialize all visualizations with the analysis data
     */
    initializeVisualizations(analysisData) {
        // Clear any existing charts
        this.clearAllCharts();
        
        // Create visualization containers
        this.createVisualizationContainers();
        
        // Initialize each visualization
        this.createLanguageDistributionChart(analysisData.repository_metadata);
        this.createContributionTimeline(analysisData.development_activity);
        this.createActivityCalendar(analysisData.development_activity);
        this.createFileSizeTreemap(analysisData.architecture_synopsis);
        this.createDependencyGraph(analysisData.architecture_synopsis);
        this.createCodeComplexityHeatmap(analysisData.technical_debt_assessment);
        this.createCommitFrequencyChart(analysisData.development_activity);
        this.createIssuesPRChart(analysisData.development_activity);
    }

    /**
     * Create containers for all visualizations
     */
    createVisualizationContainers() {
        const visualizationsHTML = `
            <div class="visualizations-section">
                <h2 class="section-title">
                    <span class="title-icon">📊</span>
                    Visual Analytics Dashboard
                </h2>
                
                <div class="viz-grid">
                    <!-- Language Distribution -->
                    <div class="viz-card">
                        <h3 class="viz-title">Language Distribution</h3>
                        <div class="chart-container">
                            <canvas id="languageChart"></canvas>
                        </div>
                    </div>
                    
                    <!-- Contribution Timeline -->
                    <div class="viz-card viz-full-width">
                        <h3 class="viz-title">Contribution Timeline</h3>
                        <div class="chart-container">
                            <canvas id="contributionTimeline"></canvas>
                        </div>
                    </div>
                    
                    <!-- Activity Calendar -->
                    <div class="viz-card viz-full-width">
                        <h3 class="viz-title">Activity Heatmap</h3>
                        <div id="activityCalendar" class="calendar-container"></div>
                    </div>
                    
                    <!-- Commit Frequency -->
                    <div class="viz-card">
                        <h3 class="viz-title">Commit Frequency</h3>
                        <div class="chart-container">
                            <canvas id="commitFrequency"></canvas>
                        </div>
                    </div>
                    
                    <!-- Issues & PRs -->
                    <div class="viz-card">
                        <h3 class="viz-title">Issues & Pull Requests</h3>
                        <div class="chart-container">
                            <canvas id="issuesPRChart"></canvas>
                        </div>
                    </div>
                    
                    <!-- File Size Treemap -->
                    <div class="viz-card viz-full-width">
                        <h3 class="viz-title">Repository Structure</h3>
                        <div id="fileSizeTreemap" class="treemap-container"></div>
                    </div>
                    
                    <!-- Dependency Graph -->
                    <div class="viz-card viz-full-width">
                        <h3 class="viz-title">Dependency Network</h3>
                        <div id="dependencyGraph" class="graph-container"></div>
                    </div>
                    
                    <!-- Code Complexity Heatmap -->
                    <div class="viz-card viz-full-width">
                        <h3 class="viz-title">Technical Debt Heatmap</h3>
                        <div id="complexityHeatmap" class="heatmap-container"></div>
                    </div>
                </div>
            </div>
        `;
        
        // Insert into visualizations tab
        const vizTab = document.getElementById('visualizationsContainer');
        if (vizTab) {
            vizTab.innerHTML = visualizationsHTML;
        } else {
            // Fallback: Insert after results section
            const resultsSection = document.getElementById('resultsSection');
            const vizContainer = document.createElement('div');
            vizContainer.innerHTML = visualizationsHTML;
            resultsSection.appendChild(vizContainer);
        }
    }

    /**
     * Create language distribution donut chart
     */
    createLanguageDistributionChart(metadata) {
        const ctx = document.getElementById('languageChart');
        if (!ctx || !metadata.language_composition) return;
        
        const languages = Object.entries(metadata.language_composition);
        const data = {
            labels: languages.map(([lang, _]) => lang),
            datasets: [{
                data: languages.map(([_, percent]) => percent),
                backgroundColor: this.colors.chartColors.slice(0, languages.length),
                borderWidth: 2,
                borderColor: this.colors.dark
            }]
        };
        
        this.charts.language = new Chart(ctx, {
            type: 'doughnut',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: this.colors.light,
                            padding: 15,
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                return `${context.label}: ${context.parsed}%`;
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Create contribution timeline line chart
     */
    createContributionTimeline(activity) {
        const ctx = document.getElementById('contributionTimeline');
        if (!ctx) return;
        
        // Generate sample timeline data (in real app, this would come from commits)
        const last30Days = Array.from({length: 30}, (_, i) => {
            const date = new Date();
            date.setDate(date.getDate() - (29 - i));
            return date.toISOString().split('T')[0];
        });
        
        const data = {
            labels: last30Days,
            datasets: [{
                label: 'Commits',
                data: last30Days.map(() => Math.floor(Math.random() * 15)),
                borderColor: this.colors.primary,
                backgroundColor: this.colors.primary + '20',
                tension: 0.4,
                fill: true
            }]
        };
        
        this.charts.timeline = new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: this.colors.dark + '20'
                        },
                        ticks: {
                            color: this.colors.light,
                            maxRotation: 45,
                            minRotation: 45
                        }
                    },
                    y: {
                        grid: {
                            color: this.colors.dark + '20'
                        },
                        ticks: {
                            color: this.colors.light
                        }
                    }
                }
            }
        });
    }

    /**
     * Create activity calendar heatmap
     */
    createActivityCalendar(activity) {
        const container = document.getElementById('activityCalendar');
        if (!container) return;
        
        // Create GitHub-style contribution calendar
        const weeks = 52;
        const days = 7;
        let calendarHTML = '<div class="calendar-grid">';
        
        // Day labels
        const dayLabels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        calendarHTML += '<div class="calendar-labels">';
        dayLabels.forEach(day => {
            calendarHTML += `<div class="day-label">${day}</div>`;
        });
        calendarHTML += '</div>';
        
        // Calendar grid
        calendarHTML += '<div class="calendar-weeks">';
        for (let week = 0; week < weeks; week++) {
            calendarHTML += '<div class="calendar-week">';
            for (let day = 0; day < days; day++) {
                const intensity = Math.floor(Math.random() * 5);
                calendarHTML += `<div class="calendar-day" data-intensity="${intensity}" title="Commits: ${intensity * 3}"></div>`;
            }
            calendarHTML += '</div>';
        }
        calendarHTML += '</div></div>';
        
        container.innerHTML = calendarHTML;
    }

    /**
     * Create commit frequency bar chart
     */
    createCommitFrequencyChart(activity) {
        const ctx = document.getElementById('commitFrequency');
        if (!ctx) return;
        
        const data = {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Commits by Day',
                data: [12, 19, 15, 25, 22, 8, 5],
                backgroundColor: this.colors.primary,
                borderColor: this.colors.primary,
                borderWidth: 1
            }]
        };
        
        this.charts.frequency = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: this.colors.dark + '20'
                        },
                        ticks: {
                            color: this.colors.light
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: this.colors.light
                        }
                    }
                }
            }
        });
    }

    /**
     * Create issues and pull requests comparison chart
     */
    createIssuesPRChart(activity) {
        const ctx = document.getElementById('issuesPRChart');
        if (!ctx) return;
        
        const openIssues = activity.open_issues_count || 0;
        const openPRs = activity.open_pull_requests || 0;
        
        const data = {
            labels: ['Open Issues', 'Open PRs'],
            datasets: [{
                data: [openIssues, openPRs],
                backgroundColor: [this.colors.warning, this.colors.success],
                borderWidth: 2,
                borderColor: this.colors.dark
            }]
        };
        
        this.charts.issuesPR = new Chart(ctx, {
            type: 'doughnut',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: this.colors.light,
                            padding: 15,
                            font: { size: 12 }
                        }
                    }
                }
            }
        });
    }

    /**
     * Create file size treemap using D3.js
     */
    createFileSizeTreemap(architecture) {
        const container = document.getElementById('fileSizeTreemap');
        if (!container) return;
        
        // Sample treemap data structure
        const data = {
            name: "root",
            children: [
                {
                    name: "backend",
                    children: [
                        { name: "app.py", value: 250 },
                        { name: "repo_processor.py", value: 450 },
                        { name: "deep_analyzer.py", value: 320 },
                        { name: "github_analyzer.py", value: 280 }
                    ]
                },
                {
                    name: "frontend",
                    children: [
                        { name: "index.html", value: 180 },
                        { name: "app.js", value: 520 },
                        { name: "styles.css", value: 380 },
                        { name: "visualizations.js", value: 420 }
                    ]
                },
                {
                    name: "docs",
                    children: [
                        { name: "README.md", value: 150 },
                        { name: "ARCHITECTURE.md", value: 200 }
                    ]
                }
            ]
        };
        
        const width = container.offsetWidth;
        const height = 400;
        
        // Create treemap layout
        const treemap = d3.treemap()
            .size([width, height])
            .padding(2)
            .round(true);
        
        const root = d3.hierarchy(data)
            .sum(d => d.value)
            .sort((a, b) => b.value - a.value);
        
        treemap(root);
        
        // Create SVG
        const svg = d3.select(container)
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .style('font', '12px sans-serif');
        
        // Create cells
        const cell = svg.selectAll('g')
            .data(root.leaves())
            .enter().append('g')
            .attr('transform', d => `translate(${d.x0},${d.y0})`);
        
        // Add rectangles
        cell.append('rect')
            .attr('width', d => d.x1 - d.x0)
            .attr('height', d => d.y1 - d.y0)
            .attr('fill', (d, i) => this.colors.chartColors[i % this.colors.chartColors.length])
            .attr('stroke', this.colors.dark)
            .attr('stroke-width', 1);
        
        // Add text labels
        cell.append('text')
            .attr('x', 4)
            .attr('y', 20)
            .text(d => d.data.name)
            .attr('fill', 'white')
            .style('font-size', '11px');
    }

    /**
     * Create dependency graph network visualization
     */
    createDependencyGraph(architecture) {
        const container = document.getElementById('dependencyGraph');
        if (!container) return;
        
        // Sample dependency data
        const nodes = [
            { id: 'app', label: 'Application', group: 1 },
            { id: 'fastapi', label: 'FastAPI', group: 2 },
            { id: 'uvicorn', label: 'Uvicorn', group: 2 },
            { id: 'httpx', label: 'httpx', group: 2 },
            { id: 'pydantic', label: 'Pydantic', group: 2 },
            { id: 'github', label: 'GitHub API', group: 3 },
            { id: 'gemini', label: 'Gemini AI', group: 3 }
        ];
        
        const links = [
            { source: 'app', target: 'fastapi', value: 1 },
            { source: 'app', target: 'uvicorn', value: 1 },
            { source: 'app', target: 'httpx', value: 1 },
            { source: 'app', target: 'pydantic', value: 1 },
            { source: 'httpx', target: 'github', value: 1 },
            { source: 'app', target: 'gemini', value: 1 }
        ];
        
        const width = container.offsetWidth;
        const height = 400;
        
        // Create SVG
        const svg = d3.select(container)
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        
        // Create force simulation
        const simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(links).id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2));
        
        // Create links
        const link = svg.append('g')
            .selectAll('line')
            .data(links)
            .enter().append('line')
            .attr('stroke', this.colors.light + '40')
            .attr('stroke-width', 2);
        
        // Create nodes
        const node = svg.append('g')
            .selectAll('circle')
            .data(nodes)
            .enter().append('circle')
            .attr('r', 20)
            .attr('fill', d => this.colors.chartColors[d.group])
            .attr('stroke', this.colors.dark)
            .attr('stroke-width', 2)
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));
        
        // Add labels
        const label = svg.append('g')
            .selectAll('text')
            .data(nodes)
            .enter().append('text')
            .text(d => d.label)
            .attr('font-size', 12)
            .attr('fill', this.colors.light)
            .attr('text-anchor', 'middle')
            .attr('dy', 4);
        
        // Update positions on tick
        simulation.on('tick', () => {
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            
            node
                .attr('cx', d => d.x)
                .attr('cy', d => d.y);
            
            label
                .attr('x', d => d.x)
                .attr('y', d => d.y);
        });
        
        // Drag functions
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
        
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }
        
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
    }

    /**
     * Create code complexity heatmap
     */
    createCodeComplexityHeatmap(technicalDebt) {
        const container = document.getElementById('complexityHeatmap');
        if (!container) return;
        
        // Sample complexity data
        const data = [
            { file: 'repo_processor.py', complexity: 85, lines: 450, issues: 3 },
            { file: 'deep_analyzer.py', complexity: 72, lines: 320, issues: 2 },
            { file: 'app.js', complexity: 68, lines: 520, issues: 1 },
            { file: 'github_analyzer.py', complexity: 45, lines: 280, issues: 0 },
            { file: 'styles.css', complexity: 20, lines: 380, issues: 0 }
        ];
        
        // Create heatmap grid
        let heatmapHTML = '<div class="heatmap-grid">';
        
        data.forEach(item => {
            const intensity = Math.min(100, item.complexity);
            const color = this.getHeatmapColor(intensity);
            
            heatmapHTML += `
                <div class="heatmap-item" style="background: ${color}">
                    <div class="heatmap-label">${item.file}</div>
                    <div class="heatmap-stats">
                        <span>Complexity: ${item.complexity}</span>
                        <span>Lines: ${item.lines}</span>
                        <span>Issues: ${item.issues}</span>
                    </div>
                </div>
            `;
        });
        
        heatmapHTML += '</div>';
        container.innerHTML = heatmapHTML;
    }

    /**
     * Get color for heatmap based on intensity
     */
    getHeatmapColor(intensity) {
        if (intensity < 30) return '#4CAF50';
        if (intensity < 50) return '#8BC34A';
        if (intensity < 70) return '#FFC107';
        if (intensity < 85) return '#FF9800';
        return '#F44336';
    }

    /**
     * Clear all existing charts
     */
    clearAllCharts() {
        Object.values(this.charts).forEach(chart => {
            if (chart) chart.destroy();
        });
        this.charts = {};
    }
}

// Export for use in main app
window.VisualizationSuite = VisualizationSuite;