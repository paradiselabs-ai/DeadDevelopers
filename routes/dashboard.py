from fasthtml.common import *
from fasthtml.svg import Svg, ft_svg as tag
from pathlib import Path
import random
import json
from typing import Dict, List
from datetime import datetime, timedelta
from app import rt, app, User
from starlette.responses import RedirectResponse
from routes.components import (
    dashboard_css, scrollbar_styles, get_toggle_js,
    DashboardLayout, Sidebar, Header,
    PlusIcon, ArrowIcon, DotsIcon, CalendarIcon, StarIcon,
    EditProfileIcon, BillingIcon, SecurityIcon, NotificationIcon,
    TeamNotificationIcon, StarIconNotification, MessageIcon, SignOutIcon,
    SearchIcon, MenuIcon, SettingsIcon, HomeIcon, ProjectsIcon, AnalyticsIcon,
    TeamIcon, DocsIcon
)

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
    return Div(
        Div(id="resource-container", cls="resource-canvas"),
        Script("""
        document.addEventListener('DOMContentLoaded', function() {
            const container = document.getElementById('resource-container');
            if (!container) return;
            
            // Create canvas element
            const canvas = document.createElement('canvas');
            canvas.id = 'resource-canvas';
            canvas.style.width = '100%';
            canvas.style.height = '100%';
            container.appendChild(canvas);
            
            const ctx = canvas.getContext('2d');
            if (!ctx) return;
            
            // Set canvas dimensions
            const rect = container.getBoundingClientRect();
            canvas.width = rect.width;
            canvas.height = rect.height;
            
            // Clear canvas
            ctx.clearRect(0, 0, rect.width, rect.height);
            
            // Same drawing code as above
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
                ctx.fillStyle = "#999";
                ctx.font = "12px sans-serif";
                ctx.textAlign = "left";
                ctx.fillText(resource.name, 0, y + barHeight / 2 + 4);
                const barX = labelWidth;
                const barWidth = rect.width - labelWidth - valueWidth;
                ctx.fillStyle = "#252525";
                ctx.beginPath();
                ctx.roundRect(barX, y, barWidth, barHeight, barRadius);
                ctx.fill();
                ctx.fillStyle = resource.color;
                const usageWidth = barWidth * resource.usage;
                ctx.beginPath();
                ctx.roundRect(barX, y, usageWidth, barHeight, barRadius);
                ctx.fill();
                ctx.fillStyle = "#fff";
                ctx.textAlign = "right";
                ctx.fillText(`${Math.round(resource.usage * 100)}%`, rect.width, y + barHeight / 2 + 4);
            });
        });
        """)
    )

# Define main dashboard route
@rt("/dashboard")
def dashboard(session, req):
    # Check if user is authenticated
    if 'auth' not in session or not session['auth']:
        # User is not authenticated, redirect to login page
        return RedirectResponse('/login', status_code=303)

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

    # Get the username from the session
    username = session['auth']
    
    # Get the toggle JavaScript from the components module
    toggle_js = get_toggle_js()
    
    # Create the dashboard UI
    dashboard_content = Div(
            
# Main Dashboard Content
                # Profile Header
                Div(
                    Div(
                        Div(
                            Img(src="\img\code-avatar.svg?height=48&width=48", alt="Profile", crossorigin="anonymous"),
                            cls="profile-avatar"
                        ),
                        Div(
                            H1(username, cls="profile-name"),
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
    )

    return Title("Dashboard - DeadDevHub"), dashboard_css, scrollbar_styles, Script(toggle_js), DashboardLayout(username, state, dashboard_content)

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