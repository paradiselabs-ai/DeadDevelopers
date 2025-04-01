from fasthtml.common import *
from fasthtml.svg import Svg, ft_svg as tag
from pathlib import Path
import random
import json
from typing import Dict, List
from datetime import datetime, timedelta
from app import rt

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

def StarIcon(width=14, height=14):
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
        viewBox="0 0 24 24", width="14", height="14", stroke="currentColor",
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
    return Title("Dashboard - DeadDevHub"), Style(dashboard_css), Script(toggle_js), Div(
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
                                    cls="notification-item"
                                ),
                                Div(
                                    Div(
                                        StarIcon(),
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
                                    cls="notification-item"
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
                                    cls="notification-item"
                                ),
                                cls="notification-list"
                            ),
                            Div(
                                Button("View all notifications", cls="view-all-button"),
                                cls="notification-footer"
                            ),
                            cls="notification-dropdown",
                            style="display: none;"
                        ),
                        cls="notification-container"
                    ),
                    
                    Div(
                        Button(
                            Div(
                                Img(src="/placeholder.svg?height=32&width=32", alt="Profile", crossOrigin="anonymous"),
                                cls="avatar"
                            ),
                            Span("DeadDev_42", cls="username"),
                            cls="user-menu-button",
                            id="user-menu-button"
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
                                    )
                                ),
                                Li(
                                    A(
                                        BillingIcon(),
                                        "Billing",
                                        href="#",
                                        cls="user-dropdown-item"
                                    )
                                ),
                                Li(
                                    A(
                                        SecurityIcon(),
                                        "Security",
                                        href="#",
                                        cls="user-dropdown-item"
                                    )
                                ),
                                Li(
                                    A(
                                        SignOutIcon(),
                                        "Sign Out",
                                        href="#",
                                        cls="user-dropdown-item"
                                    ),
                                    cls="dropdown-divider"
                                ),
                                cls="user-dropdown-menu"
                            ),
                            cls="user-dropdown",
                            style="display: none;"
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
                            Img(src="/placeholder.svg?height=48&width=48", alt="Profile", crossOrigin="anonymous"),
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
        cls="dashboard-container"
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

# Define CSS for dashboard
dashboard_css = """
:root {
  --terminal-dark: #0a0a0a;
  --terminal-light: #1a1a1a;
  --light: #ffffff;
  --dark: #13131f;
  --primary: #00ff66;
  --secondary: #00ffff;
  --gray-dark: #2c2c3b;
  --gray: #4a4a64;
  --gray-light: #8686a3;
}

.dashboard-container {
  display: flex;
  min-height: 100vh;
  background: var(--dark);
  color: var(--light);
  font-family: 'Inter', system-ui, sans-serif;
}

.sidebar-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 98;
}

.sidebar-overlay.active {
  display: block;
}

.sidebar {
  display: flex;
  flex-direction: column;
  background: var(--gray-dark);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  z-index: 99;
  width: 250px;
  height: 100vh;
  position: fixed;
  overflow-y: auto;
}

.sidebar.desktop-closed {
  width: 70px;
}

.sidebar.mobile-closed {
  transform: translateX(-100%);
}

.sidebar.mobile-open {
  transform: translateX(0);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--light);
  margin: 0;
}

.logo-accent {
  color: var(--primary);
}

.logo-icon {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary);
}

.sidebar-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: var(--light);
  cursor: pointer;
  width: 32px;
  height: 32px;
  border-radius: 4px;
  transition: all 0.2s;
}

.sidebar-toggle:hover {
  background: rgba(255, 255, 255, 0.1);
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  padding: 1rem 0;
  flex: 1;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  color: var(--gray-light);
  background: transparent;
  border: none;
  cursor: pointer;
  width: 100%;
  text-align: left;
  font-size: 1rem;
  transition: all 0.2s;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--light);
}

.nav-item.active {
  color: var(--primary);
  background: rgba(0, 255, 102, 0.05);
  border-left: 3px solid var(--primary);
}

.recent-projects {
  padding: 1.5rem;
  margin-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.recent-projects-title {
  font-size: 0.875rem;
  color: var(--gray-light);
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.recent-projects-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.recent-project-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0;
  color: var(--light);
  text-decoration: none;
  font-size: 0.875rem;
}

.project-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--primary);
}

.project-dot.python {
  background: #3572A5;
}

.project-dot.javascript {
  background: #F0DB4F;
}

.project-dot.git {
  background: #F34F29;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.main-content {
  flex: 1;
  margin-left: 250px;
  transition: margin-left 0.3s ease;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: var(--gray-dark);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.menu-button {
  display: none;
  background: transparent;
  border: none;
  color: var(--light);
  cursor: pointer;
}

.search-container {
  position: relative;
  width: 300px;
}

.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--gray-light);
}

.search-input {
  width: 100%;
  padding: 0.5rem 0.5rem 0.5rem 2rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: var(--light);
  font-size: 0.875rem;
}

.search-input::placeholder {
  color: var(--gray-light);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.notification-container, .user-menu-container {
  position: relative;
}

.notification-button, .user-menu-button {
  display: flex;
  align-items: center;
  background: transparent;
  border: none;
  color: var(--light);
  cursor: pointer;
  position: relative;
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  width: 18px;
  height: 18px;
  background: var(--primary);
  color: var(--dark);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: bold;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--gray);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.username {
  margin-left: 0.5rem;
  font-weight: 500;
}

.notification-dropdown, .user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 320px;
  background: var(--gray-dark);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  z-index: 100;
  margin-top: 0.5rem;
}

.notification-header, .user-dropdown-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.notification-header h3, .user-dropdown-header p.user-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.mark-read-button {
  background: transparent;
  border: none;
  color: var(--primary);
  cursor: pointer;
  font-size: 0.75rem;
}

.notification-list {
  max-height: 400px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  gap: 0.75rem;
}

.notification-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-icon.team {
  background: rgba(0, 153, 255, 0.2);
  color: #0099ff;
}

.notification-icon.star {
  background: rgba(255, 204, 0, 0.2);
  color: #ffcc00;
}

.notification-icon.message {
  background: rgba(102, 51, 255, 0.2);
  color: #6633ff;
}

.notification-content p {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.4;
}

.notification-time {
  color: var(--gray-light);
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

.bold {
  font-weight: 600;
}

.notification-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.view-all-button {
  background: transparent;
  border: none;
  color: var(--primary);
  cursor: pointer;
  font-size: 0.875rem;
}

.user-dropdown-header {
  flex-direction: column;
  align-items: flex-start;
}

.user-role {
  margin: 0.25rem 0 0;
  font-size: 0.75rem;
  color: var(--gray-light);
}

.user-dropdown-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.user-dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: var(--light);
  text-decoration: none;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.user-dropdown-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.dropdown-divider {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 0.5rem;
}

.dashboard-main {
  padding: 1.5rem;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.profile-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.profile-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--gray);
}

.profile-name {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.profile-role {
  margin: 0.25rem 0 0;
  font-size: 0.875rem;
  color: var(--gray-light);
}

.profile-actions {
  display: flex;
  gap: 0.75rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: var(--primary);
  color: var(--dark);
  border: none;
}

.btn-primary:hover {
  filter: brightness(1.1);
}

.btn-secondary {
  background: transparent;
  color: var(--light);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.metric-card {
  background: var(--gray-dark);
  border-radius: 8px;
  padding: 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.metric-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.metric-label {
  font-size: 0.875rem;
  color: var(--gray-light);
}

.metric-icon {
  color: var(--primary);
}

.metric-icon.code {
  color: #3572A5;
}

.metric-icon.streak {
  color: #F0DB4F;
}

.metric-icon.health {
  color: #FF6B6B;
}

.metric-value {
  font-size: 2rem;
  font-weight: 700;
  margin: 0.5rem 0;
}

.metric-subtitle {
  font-size: 0.75rem;
  color: var(--gray-light);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 2rem 0 1rem;
}

.section-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.view-all-link {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: var(--primary);
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.project-card {
  background: var(--gray-dark);
  border-radius: 8px;
  padding: 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.project-title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.project-badge {
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
}

.project-badge.active {
  background: rgba(0, 255, 102, 0.15);
  color: var(--primary);
}

.project-badge.beta {
  background: rgba(255, 204, 0, 0.15);
  color: #ffcc00;
}

.project-description {
  color: var(--gray-light);
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.project-stats {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.project-stat {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
}

.project-stat-icon {
  color: var(--gray-light);
}

.project-stat-icon.star {
  color: #ffcc00;
}

.project-language {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  margin-left: auto;
}

.language-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.project-language.python .language-dot {
  background: #3572A5;
}

.project-language.javascript .language-dot {
  background: #F0DB4F;
}

.project-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.project-members {
  display: flex;
  align-items: center;
}

.member {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--gray);
  color: var(--light);
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: -8px;
  border: 2px solid var(--gray-dark);
}

.project-menu {
  background: transparent;
  border: none;
  color: var(--gray-light);
  cursor: pointer;
}

.three-column-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.two-column-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.dashboard-card {
  background: var(--gray-dark);
  border-radius: 8px;
  padding: 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
}

.card-menu {
  background: transparent;
  border: none;
  color: var(--gray-light);
  cursor: pointer;
}

.network-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 1rem;
}

.network-stat {
  text-align: center;
}

.network-value {
  font-size: 1.5rem;
  font-weight: 700;
}

.network-label {
  font-size: 0.75rem;
  color: var(--gray-light);
}

.card-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 1rem 0;
}

.connections-title {
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
}

.connection-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.connection-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.connection-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.connection-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--gray);
  color: var(--light);
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.connection-name {
  margin: 0;
  font-size: 0.875rem;
}

.connection-role {
  margin: 0;
  font-size: 0.75rem;
  color: var(--gray-light);
}

.connect-button {
  background: transparent;
  border: 1px solid var(--primary);
  color: var(--primary);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  cursor: pointer;
}

.contribution-graph {
  height: 150px;
  background: var(--dark);
  border-radius: 4px;
  margin-bottom: 1rem;
  position: relative;
}

.contribution-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.contribution-count {
  font-size: 0.875rem;
}

.highlight {
  color: var(--primary);
  font-weight: 600;
}

.contribution-period {
  font-size: 0.75rem;
  color: var(--gray-light);
}

.plan-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.current-plan {
  font-size: 0.875rem;
}

.plan-label {
  color: var(--gray-light);
}

.plan-value {
  font-weight: 600;
}

.upgrade-button {
  background: transparent;
  border: 1px solid var(--primary);
  color: var(--primary);
  padding: 0.375rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  cursor: pointer;
}

.activity-feed {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  gap: 0.75rem;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.activity-icon-code {
  background: rgba(53, 114, 165, 0.2);
  color: #3572A5;
}

.activity-icon-alert {
  background: rgba(255, 107, 107, 0.2);
  color: #FF6B6B;
}

.activity-icon-git {
  background: rgba(243, 79, 41, 0.2);
  color: #F34F29;
}

.activity-icon-message {
  background: rgba(102, 51, 255, 0.2);
  color: #6633ff;
}

.activity-icon-star {
  background: rgba(255, 204, 0, 0.2);
  color: #ffcc00;
}

.activity-content {
  flex: 1;
}

.activity-message {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.4;
}

.activity-project {
  font-weight: 600;
}

.activity-time {
  margin: 0.25rem 0 0;
  font-size: 0.75rem;
  color: var(--gray-light);
}

.add-task-button {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: transparent;
  border: 1px solid var(--primary);
  color: var(--primary);
  padding: 0.375rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  cursor: pointer;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.task-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.02);
}

.task-checkbox {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  flex-shrink: 0;
}

.task-checkbox.high {
  border: 2px solid #FF6B6B;
}

.task-checkbox.medium {
  border: 2px solid #F0DB4F;
}

.task-checkbox.low {
  border: 2px solid #0099ff;
}

.task-checkbox.review {
  border: 2px solid #6633ff;
}

.task-content {
  flex: 1;
}

.task-title {
  margin: 0;
  font-size: 0.875rem;
}

.task-project {
  margin: 0.25rem 0 0;
  font-size: 0.75rem;
  color: var(--gray-light);
}

.task-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.task-priority {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.125rem 0.375rem;
  border-radius: 10px;
  text-align: center;
}

.task-priority.high {
  background: rgba(255, 107, 107, 0.15);
  color: #FF6B6B;
}

.task-priority.medium {
  background: rgba(240, 219, 79, 0.15);
  color: #F0DB4F;
}

.task-priority.low {
  background: rgba(0, 153, 255, 0.15);
  color: #0099ff;
}

.task-priority.review {
  background: rgba(102, 51, 255, 0.15);
  color: #6633ff;
}

.task-due-date {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: var(--gray-light);
}

.settings-section {
  margin-top: 2rem;
}

.settings-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.settings-card {
  background: var(--gray-dark);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.settings-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.2s;
}

.settings-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.settings-item:last-child {
  border-bottom: none;
}

.settings-item-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
}

.settings-item-description {
  margin: 0.25rem 0 0;
  font-size: 0.75rem;
  color: var(--gray-light);
}

.settings-icon {
  color: var(--gray-light);
}

@media (max-width: 768px) {
  .menu-button {
    display: block;
  }
  
  .sidebar {
    transform: translateX(-100%);
  }
  
  .sidebar.mobile-open {
    transform: translateX(0);
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .two-column-grid, .three-column-grid {
    grid-template-columns: 1fr;
  }
  
  .search-container {
    width: 200px;
  }
  
  .profile-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .profile-actions {
    width: 100%;
  }
}

/* Canvas specific stylings */
.contribution-canvas, .resource-canvas {
  width: 100%;
  height: 100%;
}

.resource-canvas {
  height: 100px;
}

.hidden {
  display: none;
}
"""
