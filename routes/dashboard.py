from fasthtml.common import *
from fasthtml.svg import Svg, ft_svg as tag
from pathlib import Path
import random
import json
from typing import Dict, List
from datetime import datetime, timedelta
from app import rt, app

# Create dashboard-specific headers
dashboard_css = Link(rel='stylesheet', href='\css\dashboard.css', type='text/css')

# Helper functions for generating data
def generate_random_contribution_data():
    """Generate random contribution data for the last 12 weeks."""
    data = []
    now = datetime.now()
    
    # Generate data for the last 12 weeks (84 days)
    for i in range(84):
        date = (now - timedelta(days=i)).strftime("%Y-%m-%d")
        count = random.randint(0, 10)
        data.append({"date": date, "count": count})
    
    return list(reversed(data))

def generate_activities():
    """Generate activity feed data."""
    return [
        {
            "id": 1,
            "type": "commit",
            "project": "AI Code Generator",
            "message": "Fixed model training pipeline",
            "time": "2 hours ago",
            "icon": "code",
        },
        {
            "id": 2,
            "type": "issue",
            "project": "DeadBot",
            "message": "Opened issue #24: Discord API rate limiting",
            "time": "Yesterday",
            "icon": "alert",
        },
        {
            "id": 3,
            "type": "pull",
            "project": "AI Code Generator",
            "message": "Merged PR #42: Add new language models",
            "time": "2 days ago",
            "icon": "git",
        },
        {
            "id": 4,
            "type": "comment",
            "project": "DeadBot",
            "message": "Commented on issue #18",
            "time": "3 days ago",
            "icon": "message",
        },
        {
            "id": 5,
            "type": "star",
            "project": "AI Code Generator",
            "message": "Received 15 new stars",
            "time": "5 days ago",
            "icon": "star",
        },
    ]

# Store state in the session
contribution_data = generate_random_contribution_data()
activities = generate_activities()

# Helper components
def MenuIcon():
    return Svg(
        tag("line", x1="3", y1="12", x2="21", y2="12"),
        tag("line", x1="3", y1="6", x2="21", y2="6"),
        tag("line", x1="3", y1="18", x2="21", y2="18"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def HomeIcon():
    return Svg(
        tag("path", d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"),
        tag("polyline", points="9 22 9 12 15 12 15 22"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def ProjectsIcon():
    return Svg(
        tag("path", d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"),
        tag("polyline", points="14 2 14 8 20 8"),
        tag("line", x1="16", y1="13", x2="8", y2="13"),
        tag("line", x1="16", y1="17", x2="8", y2="17"),
        tag("polyline", points="10 9 9 9 8 9"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def AnalyticsIcon():
    return Svg(
        tag("line", x1="18", y1="20", x2="18", y2="10"),
        tag("line", x1="12", y1="20", x2="12", y2="4"),
        tag("line", x1="6", y1="20", x2="6", y2="14"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def TeamIcon():
    return Svg(
        tag("path", d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"),
        tag("circle", cx="9", cy="7", r="4"),
        tag("path", d="M23 21v-2a4 4 0 0 0-3-3.87"),
        tag("path", d="M16 3.13a4 4 0 0 1 0 7.75"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def DocsIcon():
    return Svg(
        tag("path", d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"),
        tag("path", d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def SettingsIcon():
    return Svg(
        tag("circle", cx="12", cy="12", r="3"),
        tag("path", d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def SearchIcon():
    return Svg(
        tag("circle", cx="11", cy="11", r="8"),
        tag("line", x1="21", y1="21", x2="16.65", y2="16.65"),
        viewBox="0 0 24 24", width="18", height="18", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def NotificationIcon():
    return Svg(
        tag("path", d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"),
        tag("path", d="M13.73 21a2 2 0 0 1-3.46 0"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def TeamNotificationIcon():
    return Svg(
        tag("path", d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"),
        tag("circle", cx="9", cy="7", r="4"),
        tag("path", d="M23 21v-2a4 4 0 0 0-3-3.87"),
        tag("path", d="M16 3.13a4 4 0 0 1 0 7.75"),
        viewBox="0 0 24 24", width="14", height="14", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def StarIcon(width=15, height=15):
    return Svg(
        tag("polygon", points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"),
        viewBox="0 0 24 24", width=width, height=height, stroke="#00FF00",
        strokeWidth="2", fill="none"
    )
    
def StarIconNotification(width=14, height=14):
    return Svg(
        tag("polygon", points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"),
        viewBox="0 0 24 24", width=width, height=height, stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def MessageIcon():
    return Svg(
        tag("path", d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"),
        viewBox="0 0 24 24", width="14", height="14", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def EditProfileIcon():
    return Svg(
        tag("path", d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"),
        tag("path", d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"),
        viewBox="0 0 24 24", width="16", height="16", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def BillingIcon():
    return Svg(
        tag("rect", x="1", y="4", width="22", height="16", rx="2", ry="2"),
        tag("line", x1="1", y1="10", x2="23", y2="10"),
        viewBox="0 0 24 24", width="16", height="16", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def SecurityIcon():
    return Svg(
        tag("rect", x="3", y="11", width="18", height="11", rx="2", ry="2"),
        tag("path", d="M7 11V7a5 5 0 0 1 10 0v4"),
        viewBox="0 0 24 24", width="16", height="16", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def SignOutIcon():
    return Svg(
        tag("path", d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"),
        tag("polyline", points="16 17 21 12 16 7"),
        tag("line", x1="21", y1="12", x2="9", y2="12"),
        viewBox="0 0 24 24", width="16", height="16", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def PlusIcon():
    return Svg(
        tag("line", x1="12", y1="5", x2="12", y2="19"),
        tag("line", x1="5", y1="12", x2="19", y2="12"),
        viewBox="0 0 24 24", width="16", height="16", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def ArrowIcon():
    return Svg(
        tag("line", x1="7", y1="17", x2="17", y2="7"),
        tag("polyline", points="7 7 17 7 17 17"),
        viewBox="0 0 24 24", width="18", height="18", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def DotsIcon():
    return Svg(
        tag("circle", cx="12", cy="12", r="1"),
        tag("circle", cx="19", cy="12", r="1"),
        tag("circle", cx="5", cy="12", r="1"),
        viewBox="0 0 24 24", width="18", height="18", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def CalendarIcon():
    return Svg(
        tag("rect", x="3", y="4", width="18", height="18", rx="2", ry="2"),
        tag("line", x1="16", y1="2", x2="16", y2="6"),
        tag("line", x1="8", y1="2", x2="8", y2="6"),
        tag("line", x1="3", y1="10", x2="21", y2="10"),
        viewBox="0 0 24 24", width="12", height="12", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

# UI Component Helpers
def ActivityFeed():
    icon_map = {
        "code": "activity-icon-code",
        "alert": "activity-icon-alert",
        "git": "activity-icon-git",
        "message": "activity-icon-message",
        "star": "activity-icon-star"
    }
    
    icon_content = {
        "code": "{ }",
        "alert": "!",
        "git": "⌥",
        "message": "💬",
        "star": "★"
    }
    
    return Div(
        *[Div(
            Div(icon_content.get(activity["icon"], "•"), cls=f"activity-icon {icon_map.get(activity['icon'], 'activity-icon-default')}"),
            Div(
                P(
                    Span(activity["project"], cls="activity-project"), 
                    f": {activity['message']}", 
                    cls="activity-message"
                ),
                P(activity["time"], cls="activity-time"),
                cls="activity-content"
            ),
            cls="activity-item"
        ) for activity in activities],
        cls="activity-feed"
    )

def ContributionGraph():
    # In FastHTML, we generate the graph using a server-side script
    # We use a placeholder for the contribution graph that will be filled with JS
    contribution_count = sum(item["count"] for item in contribution_data)
    
    return Div(
        Div(id="contribution-graph", cls="contribution-graph"),
        Div(
            Div(Span(str(contribution_count), cls="highlight"), " contributions", cls="contribution-count"),
            Div("Last 12 weeks", cls="contribution-period"),
            cls="contribution-stats"
        )
    )

def ResourceUsage():
    # Another canvas-based component
    return Div(
        Div(id="resource-canvas", cls="resource-canvas"),
        Script("""
        document.addEventListener('DOMContentLoaded', function() {
            const canvas = document.getElementById('resource-canvas');
            if (!canvas) return;
            
            const ctx = canvas.getContext('2d');
            if (!ctx) return;
            
            // Set canvas dimensions
            const rect = canvas.getBoundingClientRect();
            canvas.width = rect.width;
            canvas.height = rect.height;
            
            // Clear canvas
            ctx.clearRect(0, 0, rect.width, rect.height);
            
            // Resource usage data
            const resources = [
                { name: "CPU", usage: 0.65, color: "#00ff00" },
                { name: "Memory", usage: 0.42, color: "#F0DB4F" },
                { name: "Storage", usage: 0.78, color: "#3572A5" },
            ];
            
            const barHeight = 12;
            const barGap = 24;
            const barRadius = 6;
            const labelWidth = 60;
            const valueWidth = 40;
            
            resources.forEach((resource, index) => {
                const y = index * barGap + 10;
                
                // Draw label
                ctx.fillStyle = "#999";
                ctx.font = "12px sans-serif";
                ctx.textAlign = "left";
                ctx.fillText(resource.name, 0, y + barHeight / 2 + 4);
                
                // Draw background bar
                const barX = labelWidth;
                const barWidth = rect.width - labelWidth - valueWidth;
                
                ctx.fillStyle = "#252525";
                ctx.beginPath();
                ctx.roundRect(barX, y, barWidth, barHeight, barRadius);
                ctx.fill();
                
                // Draw usage bar
                ctx.fillStyle = resource.color;
                const usageWidth = barWidth * resource.usage;
                
                ctx.beginPath();
                ctx.roundRect(barX, y, usageWidth, barHeight, barRadius);
                ctx.fill();
                
                // Draw percentage
                ctx.fillStyle = "#fff";
                ctx.textAlign = "right";
                ctx.fillText(`${Math.round(resource.usage * 100)}%`, rect.width, y + barHeight / 2 + 4);
            });
        });
        """)
    )

# Define main dashboard route
@rt("/dashboard")
def dashboard(session):
    # Get session state or set defaults
    if 'dashboard_state' not in session:
        session['dashboard_state'] = {
            'sidebarOpen': False,
            'activeTab': 'dashboard',
            'showNotifications': False,
            'showUserMenu': False,
            'searchQuery': '',
            'isMobile': False
        }
    
    state = session['dashboard_state']
    
    # Determine if mobile (this would normally be done with JS on client side)
    is_mobile = state.get('isMobile', False)
    sidebar_open = state.get('sidebarOpen', False)
    active_tab = state.get('activeTab', 'dashboard')
    
    # The CSS and JavaScript to handle toggling
    toggle_js = """
    document.addEventListener('DOMContentLoaded', function() {
        const sidebarToggle = document.getElementById('sidebar-toggle');
        const menuButton = document.getElementById('menu-button');
        const sidebar = document.getElementById('sidebar');
        const overlay = document.querySelector('.sidebar-overlay');
        const notificationButton = document.getElementById('notification-button');
        const notificationDropdown = document.querySelector('.notification-dropdown');
        const userMenuButton = document.getElementById('user-menu-button');
        const userDropdown = document.querySelector('.user-dropdown');
        
        // Check if mobile
        const checkMobile = () => {
            const isMobile = window.innerWidth < 768;
            if (isMobile) {
                sidebar.classList.remove('desktop-open', 'desktop-closed');
                sidebar.classList.add('mobile-closed');
                document.querySelector('.main-content').style.marginLeft = '0';
            } else {
                sidebar.classList.remove('mobile-open', 'mobile-closed');
                sidebar.classList.add('desktop-closed');
                document.querySelector('.main-content').style.marginLeft = '70px';
            }
        };
        
        checkMobile();
        window.addEventListener('resize', checkMobile);
        
        // Toggle sidebar
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', function() {
                if (sidebar.classList.contains('mobile-closed')) {
                    sidebar.classList.remove('mobile-closed');
                    sidebar.classList.add('mobile-open');
                    overlay.classList.add('active');
                } else if (sidebar.classList.contains('mobile-open')) {
                    sidebar.classList.remove('mobile-open');
                    sidebar.classList.add('mobile-closed');
                    overlay.classList.remove('active');
                } else if (sidebar.classList.contains('desktop-closed')) {
                    sidebar.classList.remove('desktop-closed');
                    sidebar.classList.add('desktop-open');
                    document.querySelector('.main-content').style.marginLeft = '250px';
                } else {
                    sidebar.classList.remove('desktop-open');
                    sidebar.classList.add('desktop-closed');
                    document.querySelector('.main-content').style.marginLeft = '70px';
                }
                
                // Close dropdowns when sidebar is toggled
                if (notificationDropdown) notificationDropdown.style.display = 'none';
                if (userDropdown) userDropdown.style.display = 'none';
            });
        }
        
        // Mobile menu button
        if (menuButton) {
            menuButton.addEventListener('click', function() {
                if (sidebar.classList.contains('mobile-closed')) {
                    sidebar.classList.remove('mobile-closed');
                    sidebar.classList.add('mobile-open');
                    overlay.classList.add('active');
                } else {
                    sidebar.classList.remove('mobile-open');
                    sidebar.classList.add('mobile-closed');
                    overlay.classList.remove('active');
                }
            });
        }
        
        // Close sidebar when clicking outside on mobile
        if (overlay) {
            overlay.addEventListener('click', function() {
                sidebar.classList.remove('mobile-open');
                sidebar.classList.add('mobile-closed');
                overlay.classList.remove('active');
            });
        }
        
        // Toggle notification dropdown
        if (notificationButton) {
            notificationButton.addEventListener('click', function(e) {
                e.stopPropagation();
                const isVisible = notificationDropdown.style.display === 'block';
                notificationDropdown.style.display = isVisible ? 'none' : 'block';
                if (userDropdown) userDropdown.style.display = 'none';
            });
        }
        
        // Toggle user menu dropdown
        if (userMenuButton) {
            userMenuButton.addEventListener('click', function(e) {
                e.stopPropagation();
                const isVisible = userDropdown.style.display === 'block';
                userDropdown.style.display = isVisible ? 'none' : 'block';
                if (notificationDropdown) notificationDropdown.style.display = 'none';
            });
        }
        
        // Close dropdowns when clicking elsewhere
        document.addEventListener('click', function() {
            if (notificationDropdown) notificationDropdown.style.display = 'none';
            if (userDropdown) userDropdown.style.display = 'none';
        });
        
        // Initialize contribution graph
        const contributionCanvas = document.getElementById('contribution-graph');
        if (contributionCanvas) {
            const data = JSON.parse(contributionCanvas.getAttribute('data-contributions'));
            renderContributionGraph(contributionCanvas, data);
        }
    });
    
    function renderContributionGraph(container, data) {
        const canvas = document.createElement('canvas');
        canvas.className = 'contribution-canvas';
        container.appendChild(canvas);
        
        const ctx = canvas.getContext('2d');
        if (!ctx) return;
        
        // Set canvas dimensions
        const rect = container.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = rect.height;
        
        // Clear canvas
        ctx.clearRect(0, 0, rect.width, rect.height);
        
        // Draw contribution graph
        const cellSize = 12;
        const cellGap = 3;
        const totalWidth = rect.width;
        const totalHeight = rect.height;
        
        // Calculate how many cells we can fit
        const cellsPerRow = Math.floor(totalHeight / (cellSize + cellGap));
        const cellsPerColumn = Math.floor(totalWidth / (cellSize + cellGap));
        const totalCells = cellsPerRow * cellsPerColumn;
        
        // Use only the most recent data that fits
        const recentData = data.slice(-totalCells);
        
        // Draw cells
        let x = 0;
        let y = 0;
        
        recentData.forEach((item) => {
            const intensity = item.count / 10; // Normalize to 0-1
            
            // Set color based on intensity (green with varying opacity)
            ctx.fillStyle = `rgba(0, 255, 0, ${Math.max(0.1, intensity)})`;
            
            // Draw cell
            ctx.fillRect(x, y, cellSize, cellSize);
            
            // Move to next position
            x += cellSize + cellGap;
            
            // If we reach the end of the row, move to the next row
            if (x + cellSize > totalWidth) {
                x = 0;
                y += cellSize + cellGap;
            }
        });
    }
    """
    
    # Create the dashboard UI
    return Title("Dashboard - DeadDevHub"), dashboard_css, Script(toggle_js), Div(
        # Overlay when sidebar is open
        Div(cls=f"sidebar-overlay {'active' if sidebar_open and is_mobile else ''}", id="sidebar-overlay"),
        
        # Sidebar
        Aside(
            Div(
                H1("DeadDev", Span("Hub", cls="logo-accent"), cls="logo") if sidebar_open or not is_mobile else Span("D", cls="logo-icon"),
                Button(MenuIcon(), cls="sidebar-toggle", id="sidebar-toggle"),
                cls="sidebar-header"
            ),
            Nav(
                Ul(
                    Li(
                        Button(
                            HomeIcon(),
                            Span("Dashboard", cls=f"{'hidden' if not sidebar_open and not is_mobile else ''}", id="dashboard-label"),
                            cls=f"nav-item {'active' if active_tab == 'dashboard' else ''}",
                            hx_post="/toggle_tab", 
                            hx_vals='{"tab": "dashboard"}',
                            hx_target="body",
                            hx_swap="none"
                        )
                    ),
                    Li(
                        Button(
                            ProjectsIcon(),
                            Span("Projects", cls=f"{'hidden' if not sidebar_open and not is_mobile else ''}", id="projects-label"),
                            cls=f"nav-item {'active' if active_tab == 'projects' else ''}",
                            hx_post="/toggle_tab", 
                            hx_vals='{"tab": "projects"}',
                            hx_target="body",
                            hx_swap="none"
                        )
                    ),
                    Li(
                        Button(
                            AnalyticsIcon(),
                            Span("Analytics", cls=f"{'hidden' if not sidebar_open and not is_mobile else ''}", id="analytics-label"),
                            cls=f"nav-item {'active' if active_tab == 'analytics' else ''}",
                            hx_post="/toggle_tab", 
                            hx_vals='{"tab": "analytics"}',
                            hx_target="body",
                            hx_swap="none"
                        )
                    ),
                    Li(
                        Button(
                            TeamIcon(),
                            Span("Team", cls=f"{'hidden' if not sidebar_open and not is_mobile else ''}", id="team-label"),
                            cls=f"nav-item {'active' if active_tab == 'team' else ''}",
                            hx_post="/toggle_tab", 
                            hx_vals='{"tab": "team"}',
                            hx_target="body",
                            hx_swap="none"
                        )
                    ),
                    Li(
                        Button(
                            DocsIcon(),
                            Span("Documentation", cls=f"{'hidden' if not sidebar_open and not is_mobile else ''}", id="docs-label"),
                            cls=f"nav-item {'active' if active_tab == 'docs' else ''}",
                            hx_post="/toggle_tab", 
                            hx_vals='{"tab": "docs"}',
                            hx_target="body",
                            hx_swap="none"
                        )
                    ),
                    cls="nav-list"
                ),
                
                # Recent Projects (shown when sidebar is expanded)
                Div(
                    H3("Recent Projects", cls="recent-projects-title"),
                    Ul(
                        Li(
                            A(
                                Span(cls="project-dot python"),
                                "AI Code Generator",
                                href="#",
                                cls="recent-project-item"
                            )
                        ),
                        Li(
                            A(
                                Span(cls="project-dot javascript"),
                                "DeadBot",
                                href="#",
                                cls="recent-project-item"
                            )
                        ),
                        Li(
                            A(
                                Span(cls="project-dot git"),
                                "GitSync",
                                href="#",
                                cls="recent-project-item"
                            )
                        ),
                        cls="recent-projects-list"
                    ),
                    cls=f"recent-projects {'hidden' if not sidebar_open and not is_mobile else ''}"
                ),
                cls="sidebar-nav"
            ),
            
            # Sidebar Footer
            Div(
                Button(
                    SettingsIcon(),
                    Span("Settings", cls=f"{'hidden' if not sidebar_open and not is_mobile else ''}", id="settings-label"),
                    cls=f"nav-item {'active' if active_tab == 'settings' else ''}",
                    hx_post="/toggle_tab", 
                    hx_vals='{"tab": "settings"}',
                    hx_target="body",
                    hx_swap="none"
                ),
                cls="sidebar-footer"
            ),
            
            id="sidebar",
            cls=f"sidebar {is_mobile and (sidebar_open and 'mobile-open' or 'mobile-closed') or (sidebar_open and 'desktop-open' or 'desktop-closed')}"
        ),
        
        # Main Content
        Div(
            # Header
            Header(
                Div(
                    Button(
                        MenuIcon(),
                        cls="menu-button",
                        id="menu-button"
                    ),
                    Div(
                        Div(
                            SearchIcon(),
                            cls="search-icon"
                        ),
                        Input(
                            type="text",
                            placeholder="Search projects, docs, or users...",
                            cls="search-input",
                            value=state.get('searchQuery', ''),
                            id="search-input"
                        ),
                        cls="search-container"
                    ),
                    cls="header-left"
                ),
                
                Div(
                    Div(
                        Button(
                            NotificationIcon(),
                            Span("3", cls="notification-badge"),
                            cls="notification-button",
                            id="notification-button"
                        ),
                        
                        # Notification Dropdown
                        Div(
                            Div(
                                H3("Notifications"),
                                Button("Mark all as read", cls="mark-read-button"),
                                cls="notification-header"
                            ),
                            Div(
                                Div(
                                    Div(
                                        TeamNotificationIcon(),
                                        cls="notification-icon team"
                                    ),
                                    Div(
                                        P(
                                            Span("TeamSync", cls="bold"),
                                            " invited you to collaborate"
                                        ),
                                        P("2 minutes ago", cls="notification-time"),
                                        cls="notification-content"
                                    ),
                                    cls="notification-item flex items-center"
                                ),
                                Div(
                                    Div(
                                        StarIconNotification(),
                                        cls="notification-icon star"
                                    ),
                                    Div(
                                        P(
                                            Span("DeadBot", cls="bold"),
                                            " received 5 new stars"
                                        ),
                                        P("1 hour ago", cls="notification-time"),
                                        cls="notification-content"
                                    ),
                                    cls="notification-item flex items-center"
                                ),
                                Div(
                                    Div(
                                        MessageIcon(),
                                        cls="notification-icon message"
                                    ),
                                    Div(
                                        P(
                                            Span("AI Code Generator", cls="bold"),
                                            " new comment from ",
                                            Span("user123", cls="bold")
                                        ),
                                        P("Yesterday", cls="notification-time"),
                                        cls="notification-content"
                                    ),
                                    cls="notification-item flex items-center"
                                ),
                                cls="notification-list"
                            ),
                            Div(
                                Button("View all notifications", cls="view-all-button"),
                                cls="notification-footer"
                            ),
                            cls="notification-dropdown",
                            id="notification-dropdown",
                            style="display: none;"
                        ),
                        cls="notification-container"
                    ),
                    
                    Div(
                        Button(
                            Div(
                                Img(src="/placeholder.svg?height=32&width=32", 
                                    alt="Profile", 
                                    crossorigin="anonymous", 
                                    cls="avatar"
                                ),
                                cls="avatar-container"
                            ),
                            Span("DeadDev_42", cls="username"),
                            cls="user-menu-button",
                            id="user-menu-button",
                            # Adding HTMX attributes for dropdown toggle
                            hx_target="#user-dropdown",
                            hx_swap="innerHTML"
                        ),
                        
                        # User Dropdown
                        Div(
                            Div(
                                P("DeadDev_42", cls="user-name"),
                                P("Senior AI Developer", cls="user-role"),
                                cls="user-dropdown-header"
                            ),
                            Ul(
                                Li(
                                    A(
                                        EditProfileIcon(),
                                        "Edit Profile",
                                        href="#",
                                        cls="user-dropdown-item"
                                    ),
                                    style="list-style: none;"
                                ),
                                Li(
                                    A(
                                        BillingIcon(),
                                        "Billing",
                                        href="#",
                                        cls="user-dropdown-item"
                                    ),
                                    style="list-style: none;"
                                ),
                                Li(
                                    A(
                                        SecurityIcon(),
                                        "Security",
                                        href="#",
                                        cls="user-dropdown-item"
                                    ),
                                    style="list-style: none;"
                                ),
                                Li(
                                    A(
                                        SignOutIcon(),
                                        "Sign Out",
                                        href="#",
                                        cls="user-dropdown-item"
                                    ),
                                    cls="dropdown-divider",
                                    style="list-style: none;"
                                ),
                                cls="user-dropdown-menu"
                            ),
                            cls="user-dropdown",
                            id="user-dropdown",
                            style="display: none;"  # Consider handling visibility with CSS/JS instead
                        ),
                        cls="user-menu-container"
                    ),
                    cls="header-right"
                ),
                cls="header"
            ),
            
            # Main Dashboard Content
            Main(
                # Profile Header
                Div(
                    Div(
                        Div(
                            Img(src="/placeholder.svg?height=48&width=48", alt="Profile", crossorigin="anonymous"),
                            cls="profile-avatar"
                        ),
                        Div(
                            H1("DeadDev_42", cls="profile-name"),
                            P("Senior AI Developer", cls="profile-role")
                        ),
                        cls="profile-info"
                    ),
                    Div(
                        Button(
                            PlusIcon(),
                            "New Project",
                            cls="btn btn-secondary"
                        ),
                        Button(
                            EditProfileIcon(),
                            "Edit Profile",
                            cls="btn btn-primary"
                        ),
                        cls="profile-actions"
                    ),
                    cls="profile-header"
                ),
                
                # Metrics Cards
                Div(
                    Div(
                        Div(
                            Span("Code Percentage", cls="metric-label"),
                            Svg(
                                tag("path",
                                    d="M16 18l6-6-6-6M8 6l-6 6 6 6",
                                    fill="none",
                                    stroke="currentColor",
                                    strokeWidth="2",
                                    strokeLinecap="round",
                                    strokeLinejoin="round"
                                ),
                                viewBox="0 0 24 24", width="16", height="16", cls="metric-icon code"
                            ),
                            cls="metric-header"
                        ),
                        Div("87%", cls="metric-value"),
                        Div("Last 30 days", cls="metric-subtitle"),
                        cls="metric-card"
                    ),
                    Div(
                        Div(
                            Span("Challenge Streak", cls="metric-label"),
                            Svg(
                                tag("path",
                                    d="M13 2L3 14h9l-1 8 10-12h-9l1-8z",
                                    fill="none",
                                    stroke="currentColor",
                                    strokeWidth="2",
                                    strokeLinecap="round",
                                    strokeLinejoin="round"
                                ),
                                viewBox="0 0 24 24", width="16", height="16", cls="metric-icon streak"
                            ),
                            cls="metric-header"
                        ),
                        Div("42", cls="metric-value"),
                        Div("Days", cls="metric-subtitle"),
                        cls="metric-card"
                    ),
                    Div(
                        Div(
                            Span("Project Health", cls="metric-label"),
                            Svg(
                                tag("path",
                                    d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z",
                                    fill="none",
                                    stroke="currentColor",
                                    strokeWidth="2",
                                    strokeLinecap="round",
                                    strokeLinejoin="round"
                                ),
                                viewBox="0 0 24 24", width="16", height="16", cls="metric-icon health"
                            ),
                            cls="metric-header"
                        ),
                        Div("95%", cls="metric-value"),
                        Div("Overall Score", cls="metric-subtitle"),
                        cls="metric-card"
                    ),
                    cls="metrics-grid"
                ),
                
                # Project Showcase
                Div(
                    H2("Project Showcase"),
                    Button(
                        "View All",
                        ArrowIcon(),
                        cls="view-all-link"
                    ),
                    cls="section-header"
                ),
                
                Div(
                    Div(
                        Div(
                            H3("AI Code Generator", cls="project-title"),
                            Span("Active", cls="project-badge active"),
                            cls="project-header"
                        ),
                        P("Neural network-based code generation system", cls="project-description"),
                        Div(
                            Div(
                                StarIcon(),
                                Span("156"),
                                cls="project-stat"
                            ),
                            Div(
                                Svg(
                                    tag("path",
                                        d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22",
                                        fill="none",
                                        stroke="currentColor",
                                        strokeWidth="2",
                                        strokeLinecap="round",
                                        strokeLinejoin="round"
                                    ),
                                    viewBox="0 0 24 24", width="14", height="14", cls="project-stat-icon"
                                ),
                                Span("89"),
                                cls="project-stat"
                            ),
                            Div(
                                Span(cls="language-dot"),
                                Span("Python"),
                                cls="project-language python"
                            ),
                            cls="project-stats"
                        ),
                        Div(
                            Div(
                                Div("JD", cls="member"),
                                Div("KL", cls="member"),
                                Div("+3", cls="member"),
                                cls="project-members"
                            ),
                            Button(
                                DotsIcon(),
                                cls="project-menu"
                            ),
                            cls="project-footer"
                        ),
                        cls="project-card"
                    ),
                    Div(
                        Div(
                            H3("DeadBot", cls="project-title"),
                            Span("Beta", cls="project-badge beta"),
                            cls="project-header"
                        ),
                        P("AI-powered Discord bot for developers", cls="project-description"),
                        Div(
                            Div(
                                StarIcon(),
                                Span("78"),
                                cls="project-stat"
                            ),
                            Div(
                                Svg(
                                    tag("path",
                                        d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22",
                                        fill="none",
                                        stroke="currentColor",
                                        strokeWidth="2",
                                        strokeLinecap="round",
                                        strokeLinejoin="round"
                                    ),
                                    viewBox="0 0 24 24", width="14", height="14", cls="project-stat-icon"
                                ),
                                Span("45"),
                                cls="project-stat"
                            ),
                            Div(
                                Span(cls="language-dot"),
                                Span("JavaScript"),
                                cls="project-language javascript"
                            ),
                            cls="project-stats"
                        ),
                        Div(
                            Div(
                                Div("TS", cls="member"),
                                Div("MR", cls="member"),
                                cls="project-members"
                            ),
                            Button(
                                DotsIcon(),
                                cls="project-menu"
                            ),
                            cls="project-footer"
                        ),
                        cls="project-card"
                    ),
                    cls="projects-grid"
                ),
                
                # Network, Contribution Graph, and Resource Usage
                Div(
                    Div(
                        H3("Network", cls="card-title"),
                        Div(
                            Div(
                                Div("1.2k", cls="network-value"),
                                Div("Following", cls="network-label"),
                                cls="network-stat"
                            ),
                            Div(
                                Div("3.4k", cls="network-value"),
                                Div("Followers", cls="network-label"),
                                cls="network-stat"
                            ),
                            cls="network-stats"
                        ),
                        Div(cls="card-divider"),
                        Div(
                            H4("Suggested Connections", cls="connections-title"),
                            Div(
                                Div(
                                    Div(
                                        Div("AR", cls="connection-avatar"),
                                        Div(
                                            P("Alex Rivera", cls="connection-name"),
                                            P("ML Engineer", cls="connection-role")
                                        ),
                                        cls="connection-info"
                                    ),
                                    Button("Connect", cls="connect-button"),
                                    cls="connection-item"
                                ),
                                Div(
                                    Div(
                                        Div("JL", cls="connection-avatar"),
                                        Div(
                                            P("Jamie Liu", cls="connection-name"),
                                            P("Frontend Dev", cls="connection-role")
                                        ),
                                        cls="connection-info"
                                    ),
                                    Button("Connect", cls="connect-button"),
                                    cls="connection-item"
                                ),
                                cls="connection-list"
                            ),
                            cls="suggested-connections"
                        ),
                        cls="dashboard-card"
                    ),
                    Div(
                        H3("Contribution Graph", cls="card-title"),
                        Div(
                            Div(
                                id="contribution-graph",
                                cls="contribution-graph",
                                **{"data-contributions": json.dumps(contribution_data)}
                            ),
                            cls="contribution-graph"
                        ),
                        Div(cls="card-divider"),
                        Div(
                            Div(
                                Span("842", cls="highlight"),
                                " contributions",
                                cls="contribution-count"
                            ),
                            Div("Last 12 weeks", cls="contribution-period"),
                            cls="contribution-stats"
                        ),
                        cls="dashboard-card"
                    ),
                    Div(
                        H3("Resource Usage", cls="card-title"),
                        ResourceUsage(),
                        Div(cls="card-divider"),
                        Div(
                            Div(
                                Span("Current Plan:", cls="plan-label"),
                                Span("Pro Developer", cls="plan-value"),
                                cls="current-plan"
                            ),
                            Button("Upgrade Plan", cls="upgrade-button"),
                            cls="plan-info"
                        ),
                        cls="dashboard-card"
                    ),
                    cls="three-column-grid"
                ),
                
                # Recent Activity and Upcoming Tasks
                Div(
                    Div(
                        Div(
                            H3("Recent Activity", cls="card-title"),
                            Button(
                                DotsIcon(),
                                cls="card-menu"
                            ),
                            cls="card-header"
                        ),
                        ActivityFeed(),
                        cls="dashboard-card"
                    ),
                    Div(
                        Div(
                            H3("Upcoming Tasks", cls="card-title"),
                            Button(
                                PlusIcon(),
                                "Add Task",
                                cls="add-task-button"
                            ),
                            cls="card-header"
                        ),
                        Div(
                            Div(
                                Div(cls="task-checkbox high"),
                                Div(
                                    P("Finish AI model training", cls="task-title"),
                                    P("AI Code Generator", cls="task-project"),
                                    cls="task-content"
                                ),
                                Div(
                                    Span("High", cls="task-priority high"),
                                    Div(
                                        CalendarIcon(),
                                        Span("Today"),
                                        cls="task-due-date"
                                    ),
                                    cls="task-meta"
                                ),
                                cls="task-item"
                            ),
                            Div(
                                Div(cls="task-checkbox medium"),
                                Div(
                                    P("Fix Discord API integration", cls="task-title"),
                                    P("DeadBot", cls="task-project"),
                                    cls="task-content"
                                ),
                                Div(
                                    Span("Medium", cls="task-priority medium"),
                                    Div(
                                        CalendarIcon(),
                                        Span("Tomorrow"),
                                        cls="task-due-date"
                                    ),
                                    cls="task-meta"
                                ),
                                cls="task-item"
                            ),
                            Div(
                                Div(cls="task-checkbox low"),
                                Div(
                                    P("Update documentation", cls="task-title"),
                                    P("All Projects", cls="task-project"),
                                    cls="task-content"
                                ),
                                Div(
                                    Span("Low", cls="task-priority low"),
                                    Div(
                                        CalendarIcon(),
                                        Span("May 15"),
                                        cls="task-due-date"
                                    ),
                                    cls="task-meta"
                                ),
                                cls="task-item"
                            ),
                            Div(
                                Div(cls="task-checkbox review"),
                                Div(
                                    P("Code review for PR #42", cls="task-title"),
                                    P("AI Code Generator", cls="task-project"),
                                    cls="task-content"
                                ),
                                Div(
                                    Span("Review", cls="task-priority review"),
                                    Div(
                                        CalendarIcon(),
                                        Span("May 18"),
                                        cls="task-due-date"
                                    ),
                                    cls="task-meta"
                                ),
                                cls="task-item"
                            ),
                            cls="tasks-list"
                        ),
                        cls="dashboard-card"
                    ),
                    cls="two-column-grid"
                ),
                
                # Settings
                Div(
                    H2("Settings", cls="settings-title"),
                    Div(
                        Div(
                            Div(
                                H3("API Keys", cls="settings-item-title"),
                                P("Manage your API access tokens", cls="settings-item-description"),
                                cls="settings-info"
                            ),
                            ArrowIcon(),
                            cls="settings-item"
                        ),
                        Div(
                            Div(
                                H3("Notifications", cls="settings-item-title"),
                                P("Configure your alert preferences", cls="settings-item-description"),
                                cls="settings-info"
                            ),
                            NotificationIcon(),
                            cls="settings-item"
                        ),
                        Div(
                            Div(
                                H3("Security", cls="settings-item-title"),
                                P("Manage account security settings", cls="settings-item-description"),
                                cls="settings-info"
                            ),
                            SecurityIcon(),
                            cls="settings-item"
                        ),
                        Div(
                            Div(
                                H3("Billing", cls="settings-item-title"),
                                P("Manage subscription and payment methods", cls="settings-item-description"),
                                cls="settings-info"
                            ),
                            BillingIcon(),
                            cls="settings-item"
                        ),
                        cls="settings-card"
                    ),
                    cls="settings-section"
                ),
                cls="dashboard-main"
            ),
            cls="main-content"
        ),
        cls="dashboard-container dashboard-page"
    )

# Route for handling state updates
@rt("/toggle_tab", methods=["POST"])
def toggle_tab(session, tab:str):
    if 'dashboard_state' not in session:
        session['dashboard_state'] = {
            'sidebarOpen': False,
            'activeTab': 'dashboard',
            'showNotifications': False,
            'showUserMenu': False,
            'searchQuery': '',
            'isMobile': False
        }
    
    session['dashboard_state']['activeTab'] = tab
    return "OK"