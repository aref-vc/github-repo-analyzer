/**
 * Advanced Visualization Suite for GitHub Repository Analyzer
 * Provides interactive charts and graphs for repository data
 * All data is pulled from actual repository analysis - no mock data
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
        
        // Initialize each visualization with real data
        this.createLanguageDistributionChart(analysisData.repository_metadata);
        this.createContributionTimeline(analysisData.development_activity);
        this.createActivityCalendar(analysisData.development_activity);
        this.createFileSizeTreemap(analysisData.architecture_synopsis);
        this.createDependencyGraph(analysisData.architecture_synopsis);
        this.createCodeComplexityHeatmap(analysisData);
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
                        <h3 class="viz-title">Commit Activity Timeline</h3>
                        <div class="chart-container">
                            <canvas id="contributionTimeline"></canvas>
                        </div>
                    </div>
                    
                    <!-- Activity Calendar -->
                    <div class="viz-card viz-full-width">
                        <h3 class="viz-title">Development Activity Heatmap</h3>
                        <div id="activityCalendar" class="calendar-container"></div>
                    </div>
                    
                    <!-- Commit Frequency -->
                    <div class="viz-card">
                        <h3 class="viz-title">Commit Patterns by Day</h3>
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
                        <h3 class="viz-title">Repository File Structure</h3>
                        <div id="fileSizeTreemap" class="treemap-container"></div>
                    </div>
                    
                    <!-- Dependency Graph -->
                    <div class="viz-card viz-full-width">
                        <h3 class="viz-title">Dependency Network</h3>
                        <div id="dependencyGraph" class="graph-container"></div>
                    </div>
                    
                    <!-- Code Complexity Heatmap -->
                    <div class="viz-card viz-full-width">
                        <h3 class="viz-title">Code Quality Metrics</h3>
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
     * Create language distribution donut chart (USES REAL DATA)
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
     * Create contribution timeline using real commit history
     */
    createContributionTimeline(activity) {
        const ctx = document.getElementById('contributionTimeline');
        if (!ctx) return;
        
        // Use real commit history data if available
        let timelineData = [];
        let labels = [];
        
        if (activity.commit_history && activity.commit_history.length > 0) {
            // Group commits by date
            const commitsByDate = {};
            activity.commit_history.forEach(commit => {
                const date = commit.date ? commit.date.split('T')[0] : 'Unknown';
                commitsByDate[date] = (commitsByDate[date] || 0) + 1;
            });
            
            // Sort dates and create timeline
            const sortedDates = Object.keys(commitsByDate).sort();
            labels = sortedDates.slice(-30); // Last 30 dates with commits
            timelineData = labels.map(date => commitsByDate[date] || 0);
        } else if (activity.commit_patterns) {
            // Fallback to commit patterns if available
            labels = Object.keys(activity.commit_patterns.by_month || {});
            timelineData = Object.values(activity.commit_patterns.by_month || {});
        } else {
            // If no commit data available, show message
            labels = ['No commit data available'];
            timelineData = [0];
        }
        
        const data = {
            labels: labels,
            datasets: [{
                label: 'Commits',
                data: timelineData,
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
                            color: this.colors.light,
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }

    /**
     * Create activity calendar using real development metrics
     */
    createActivityCalendar(activity) {
        const container = document.getElementById('activityCalendar');
        if (!container) return;
        
        // Create activity intensity map from real data
        const activityMap = new Map();
        
        if (activity.commit_history && activity.commit_history.length > 0) {
            // Map actual commit activity
            activity.commit_history.forEach(commit => {
                if (commit.date) {
                    const date = commit.date.split('T')[0];
                    activityMap.set(date, (activityMap.get(date) || 0) + 1);
                }
            });
        }
        
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
        
        // Calendar grid with real activity data
        calendarHTML += '<div class="calendar-weeks">';
        const today = new Date();
        
        for (let week = 51; week >= 0; week--) {
            calendarHTML += '<div class="calendar-week">';
            for (let day = 0; day < days; day++) {
                const date = new Date(today);
                date.setDate(date.getDate() - (week * 7 + (6 - day)));
                const dateStr = date.toISOString().split('T')[0];
                const commits = activityMap.get(dateStr) || 0;
                
                // Calculate intensity (0-4 scale)
                let intensity = 0;
                if (commits > 0) intensity = 1;
                if (commits > 2) intensity = 2;
                if (commits > 5) intensity = 3;
                if (commits > 10) intensity = 4;
                
                calendarHTML += `<div class="calendar-day" data-intensity="${intensity}" title="${dateStr}: ${commits} commits"></div>`;
            }
            calendarHTML += '</div>';
        }
        calendarHTML += '</div></div>';
        
        // Add legend
        calendarHTML += '<div class="calendar-legend">Less <div class="legend-scale">';
        for (let i = 0; i <= 4; i++) {
            calendarHTML += `<div class="calendar-day" data-intensity="${i}"></div>`;
        }
        calendarHTML += '</div> More</div>';
        
        container.innerHTML = calendarHTML;
    }

    /**
     * Create commit frequency chart using real patterns
     */
    createCommitFrequencyChart(activity) {
        const ctx = document.getElementById('commitFrequency');
        if (!ctx) return;
        
        // Use real commit patterns by day of week
        let dayData = [0, 0, 0, 0, 0, 0, 0]; // Sun-Sat
        
        if (activity.commit_patterns && activity.commit_patterns.by_day_of_week) {
            // Use provided day of week data
            const dayMapping = {
                'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3,
                'Thursday': 4, 'Friday': 5, 'Saturday': 6
            };
            
            Object.entries(activity.commit_patterns.by_day_of_week).forEach(([day, count]) => {
                const dayIndex = dayMapping[day];
                if (dayIndex !== undefined) {
                    dayData[dayIndex] = count;
                }
            });
        } else if (activity.commit_history && activity.commit_history.length > 0) {
            // Calculate from commit history
            activity.commit_history.forEach(commit => {
                if (commit.date) {
                    const date = new Date(commit.date);
                    const dayOfWeek = date.getDay();
                    dayData[dayOfWeek]++;
                }
            });
        }
        
        const data = {
            labels: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
            datasets: [{
                label: 'Commits by Day',
                data: dayData,
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
                            color: this.colors.light,
                            stepSize: 1
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
     * Create issues and pull requests chart (USES REAL DATA)
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
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                return `${context.label}: ${context.parsed}`;
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Create file size treemap using real file tree data
     */
    createFileSizeTreemap(architecture) {
        const container = document.getElementById('fileSizeTreemap');
        if (!container || !architecture.file_tree) return;
        
        // Convert file tree to hierarchical structure for treemap
        const convertToTreemap = (tree, name = 'root') => {
            if (!tree || typeof tree !== 'object') return null;
            
            const children = [];
            let totalSize = 0;
            
            Object.entries(tree).forEach(([key, value]) => {
                if (typeof value === 'object' && !value.type) {
                    // It's a directory
                    const child = convertToTreemap(value, key);
                    if (child) children.push(child);
                } else if (value.type === 'file') {
                    // It's a file - use lines of code or size as value
                    const fileSize = value.lines || value.size || 100;
                    children.push({
                        name: key,
                        value: fileSize
                    });
                    totalSize += fileSize;
                }
            });
            
            if (children.length === 0 && name === 'root') {
                // If no detailed file tree, use file type distribution
                if (architecture.file_type_distribution) {
                    Object.entries(architecture.file_type_distribution).forEach(([type, count]) => {
                        children.push({
                            name: type,
                            value: count * 50 // Approximate size
                        });
                    });
                }
            }
            
            return children.length > 0 ? { name, children } : null;
        };
        
        const data = convertToTreemap(architecture.file_tree) || {
            name: 'Repository',
            children: Object.entries(architecture.file_type_distribution || {}).map(([type, count]) => ({
                name: `${type} files (${count})`,
                value: count * 100
            }))
        };
        
        if (!data.children || data.children.length === 0) {
            container.innerHTML = '<div style="padding: 20px; color: #999;">No file structure data available</div>';
            return;
        }
        
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
        
        // Clear container and create SVG
        d3.select(container).selectAll('*').remove();
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
            .text(d => {
                const width = d.x1 - d.x0;
                const name = d.data.name;
                return width > 50 ? name : ''; // Only show label if enough space
            })
            .attr('fill', 'white')
            .style('font-size', '11px');
    }

    /**
     * Create dependency graph using real dependency data
     */
    createDependencyGraph(architecture) {
        const container = document.getElementById('dependencyGraph');
        if (!container) return;
        
        // Extract real dependencies from architecture data
        const nodes = [];
        const links = [];
        const nodeMap = new Map();
        
        // Add main application node
        nodes.push({ id: 'app', label: 'Application', group: 1 });
        nodeMap.set('app', true);
        
        // Process dependencies from different package managers
        const addDependencies = (deps, group) => {
            if (!deps) return;
            
            Object.keys(deps).forEach(dep => {
                if (!nodeMap.has(dep)) {
                    nodes.push({ id: dep, label: dep, group });
                    nodeMap.set(dep, true);
                    links.push({ source: 'app', target: dep, value: 1 });
                }
            });
        };
        
        // Add dependencies from various sources
        if (architecture.dependencies) {
            // npm dependencies
            addDependencies(architecture.dependencies.npm?.dependencies, 2);
            addDependencies(architecture.dependencies.npm?.devDependencies, 3);
            
            // Python dependencies
            addDependencies(architecture.dependencies.pip?.dependencies, 2);
            addDependencies(architecture.dependencies.pip?.devDependencies, 3);
            
            // Other package managers
            addDependencies(architecture.dependencies.cargo?.dependencies, 2);
            addDependencies(architecture.dependencies.maven?.dependencies, 2);
            addDependencies(architecture.dependencies.gradle?.dependencies, 2);
        }
        
        // If no dependencies found, show a message
        if (nodes.length === 1) {
            container.innerHTML = '<div style="padding: 20px; color: #999;">No dependency data available</div>';
            return;
        }
        
        const width = container.offsetWidth;
        const height = 400;
        
        // Clear container and create SVG
        d3.select(container).selectAll('*').remove();
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
            .attr('r', d => d.id === 'app' ? 25 : 15)
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
            .attr('font-size', 11)
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
     * Create code complexity heatmap using real metrics
     */
    createCodeComplexityHeatmap(analysisData) {
        const container = document.getElementById('complexityHeatmap');
        if (!container) return;
        
        // Extract real complexity data from analysis
        const complexityData = [];
        
        // Get data from technical debt assessment
        if (analysisData.technical_debt_assessment) {
            const debt = analysisData.technical_debt_assessment;
            
            // Add code organization metrics
            if (debt.code_organization) {
                Object.entries(debt.code_organization).forEach(([key, value]) => {
                    if (typeof value === 'number') {
                        complexityData.push({
                            category: 'Code Organization',
                            metric: key.replace(/_/g, ' '),
                            value: value,
                            severity: value > 70 ? 'high' : value > 40 ? 'medium' : 'low'
                        });
                    }
                });
            }
            
            // Add maintenance metrics
            if (debt.maintenance_metrics) {
                Object.entries(debt.maintenance_metrics).forEach(([key, value]) => {
                    if (typeof value === 'number') {
                        complexityData.push({
                            category: 'Maintenance',
                            metric: key.replace(/_/g, ' '),
                            value: value,
                            severity: value > 70 ? 'high' : value > 40 ? 'medium' : 'low'
                        });
                    }
                });
            }
        }
        
        // Add code quality metrics if available
        if (analysisData.code_quality_metrics) {
            const quality = analysisData.code_quality_metrics;
            
            if (quality.test_coverage !== undefined) {
                complexityData.push({
                    category: 'Quality',
                    metric: 'Test Coverage',
                    value: quality.test_coverage,
                    severity: quality.test_coverage < 30 ? 'high' : quality.test_coverage < 60 ? 'medium' : 'low'
                });
            }
            
            if (quality.documentation_coverage !== undefined) {
                complexityData.push({
                    category: 'Quality',
                    metric: 'Documentation Coverage',
                    value: quality.documentation_coverage,
                    severity: quality.documentation_coverage < 30 ? 'high' : quality.documentation_coverage < 60 ? 'medium' : 'low'
                });
            }
        }
        
        // If no complexity data available, show message
        if (complexityData.length === 0) {
            container.innerHTML = '<div style="padding: 20px; color: #999;">No code quality metrics available</div>';
            return;
        }
        
        // Create heatmap grid
        let heatmapHTML = '<div class="heatmap-grid">';
        
        // Group data by category
        const categories = {};
        complexityData.forEach(item => {
            if (!categories[item.category]) {
                categories[item.category] = [];
            }
            categories[item.category].push(item);
        });
        
        // Render each category
        Object.entries(categories).forEach(([category, items]) => {
            heatmapHTML += `<div class="heatmap-category">
                <h4 class="category-title">${category}</h4>
                <div class="heatmap-items">`;
            
            items.forEach(item => {
                const color = this.getHeatmapColor(item.value, item.severity);
                heatmapHTML += `
                    <div class="heatmap-item" style="background: ${color}">
                        <div class="heatmap-label">${item.metric}</div>
                        <div class="heatmap-value">${item.value}%</div>
                    </div>
                `;
            });
            
            heatmapHTML += '</div></div>';
        });
        
        heatmapHTML += '</div>';
        container.innerHTML = heatmapHTML;
    }

    /**
     * Get color for heatmap based on value and severity
     */
    getHeatmapColor(value, severity) {
        if (severity === 'high') return '#F44336';
        if (severity === 'medium') return '#FF9800';
        if (severity === 'low') return '#4CAF50';
        
        // Fallback to value-based coloring
        if (value < 30) return '#F44336';
        if (value < 50) return '#FF9800';
        if (value < 70) return '#FFC107';
        if (value < 85) return '#8BC34A';
        return '#4CAF50';
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