from fasthtml.common import *
from app import app, rt
from dataclasses import dataclass

@dataclass
class Project:
    name: str
    description: str
    ai_percentage: int
    status: str

# Mock data - In production, this would come from a database
SAMPLE_PROJECTS = [
    Project("E-commerce Site", "AI-generated online store with cart and checkout", 85, "in_progress"),
    Project("Task Manager", "Simple todo app with AI-powered task suggestions", 90, "completed"),
    Project("Portfolio Website", "Personal portfolio with AI-optimized content", 75, "completed")
]

@rt('/dashboard')
def get(session):
    user = session.get('user', {})
    return Titled(
        f"Dashboard - {user.get('name', 'Developer')}",
        Container(
            # Header with User Stats
            Section(
                Grid(
                    Card(
                        H3(f"{user.get('ai_percent', 80)}%"),
                        P("AI-Generated Code"),
                        cls="stat-card highlight"
                    ),
                    Card(
                        H3(f"{len(SAMPLE_PROJECTS)}"),
                        P("Active Projects"),
                        cls="stat-card"
                    ),
                    Card(
                        H3("Pro"),
                        P("Account Status"),
                        cls="stat-card"
                    ),
                    cls="dashboard-stats"
                ),
                cls="dashboard-header"
            ),

            # Projects Section
            Section(
                H2("Your Projects"),
                Grid(
                    *[project_card(p) for p in SAMPLE_PROJECTS],
                    Button(
                        "New Project",
                        cls="new-project-btn",
                        hx_get="/dashboard/new-project"
                    ),
                    cls="projects-grid"
                ),
                cls="projects-section"
            ),

            # Recent Activity
            Section(
                H2("Recent Activity"),
                Card(
                    Ul(
                        Li("Generated responsive navigation component", cls="activity-item"),
                        Li("Optimized database queries with AI suggestions", cls="activity-item"),
                        Li("Created API documentation automatically", cls="activity-item"),
                        cls="activity-list"
                    ),
                    cls="activity-card"
                ),
                cls="activity-section"
            ),

            # AI Assistant Section
            Section(
                H2("AI Assistant"),
                Card(
                    Form(
                        Textarea(
                            placeholder="Ask your AI assistant anything...",
                            rows=3,
                            cls="assistant-input",
                            name="query"
                        ),
                        Button(
                            "Ask AI",
                            type="submit",
                            cls="assistant-submit"
                        ),
                        hx_post="/dashboard/ask",
                        hx_target="#assistant-response"
                    ),
                    Div(id="assistant-response", cls="assistant-response"),
                    cls="assistant-card"
                ),
                cls="assistant-section"
            )
        )
    )

def project_card(project: Project):
    status_cls = {
        'completed': 'status-completed',
        'in_progress': 'status-in-progress',
        'planned': 'status-planned'
    }.get(project.status, '')

    return Card(
        H3(project.name),
        P(project.description),
        Div(
            f"AI Generated: {project.ai_percentage}%",
            cls=f"project-status {status_cls}"
        ),
        Button(
            "View Details",
            hx_get=f"/dashboard/project/{project.name.lower().replace(' ', '-')}",
            cls="project-btn"
        ),
        cls="project-card"
    )

@rt('/dashboard/new-project')
def get(session):
    add_toast(session, "Starting a new AI-powered project! Let's build something amazing.", "info")
    return Card(
        H3("Create New Project"),
        Form(
            Input(
                type="text",
                name="name",
                placeholder="Project Name",
                required=True
            ),
            Textarea(
                name="description",
                placeholder="Project Description",
                required=True,
                rows=3
            ),
            Button(
                "Create Project",
                type="submit",
                cls="create-project-btn"
            ),
            hx_post="/dashboard/create-project"
        ),
        cls="new-project-card"
    )

@rt('/dashboard/create-project')
def post(name: str, description: str, session):
    # TODO: Actually create the project in the database
    add_toast(session, f"Project '{name}' created! AI is ready to help you build it.", "success")
    return project_card(Project(name, description, 0, "planned"))

@rt('/dashboard/ask')
def post(query: str, session):
    # TODO: Implement actual AI assistant integration
    sample_response = """Based on your project structure, I recommend:
    1. Breaking down the component into smaller, reusable parts
    2. Adding proper error handling
    3. Implementing caching for better performance
    """
    add_toast(session, "AI assistant has analyzed your query!", "success")
    return Card(
        H4("AI Assistant Response"),
        Pre(sample_response),
        cls="response-card"
    )
