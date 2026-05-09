from fasthtml.common import *
from app import app, rt, User
from auth_bridge import AuthBridge
from routes.ai import get_ai_response
from routes.header import SiteHeader
from users.models import Project
from chat.models import ChatMessage


# ---------- Components ----------

STATUS_LABELS = dict(Project.STATUS_CHOICES)


def project_card(project: Project):
    """Card view for one Project row."""
    status_cls = {
        'completed': 'status-completed',
        'in_progress': 'status-in-progress',
        'planned': 'status-planned',
        'archived': 'status-archived',
    }.get(project.status, '')

    extras = []
    if project.repo_url:
        extras.append(A("Repo", href=project.repo_url, target="_blank", cls="project-link"))
    if project.live_url:
        extras.append(A("Live", href=project.live_url, target="_blank", cls="project-link"))

    return Card(
        H3(project.name),
        P(project.description or "No description yet."),
        Div(
            Span(STATUS_LABELS.get(project.status, project.status), cls=f"project-status {status_cls}"),
            Span(f"AI {project.ai_percentage}%", cls="project-ai-pct"),
            cls="project-meta",
        ),
        Div(*extras, cls="project-links") if extras else "",
        Div(
            A("View", href=f"/dashboard/project/{project.slug}", cls="btn-secondary"),
            Form(
                Button("Delete", type="submit", cls="btn-danger"),
                hx_delete=f"/dashboard/project/{project.slug}",
                hx_confirm=f"Delete '{project.name}'? Cannot be undone.",
                hx_target=f"#project-{project.id}",
                hx_swap="outerHTML",
            ),
            cls="project-actions",
        ),
        id=f"project-{project.id}",
        cls="project-card",
    )


def stat_card(value, label, cls=""):
    return Card(H3(str(value)), P(label), cls=f"stat-card {cls}".strip())


def activity_item(icon, text, when):
    return Li(
        Span(icon, cls="activity-icon"),
        Div(
            P(text, cls="activity-text"),
            Span(when, cls="activity-time"),
            cls="activity-body",
        ),
        cls="activity-item",
    )


def _format_when(dt):
    """Tiny relative-time formatter so we don't drag in dateutil."""
    from django.utils import timezone
    delta = timezone.now() - dt
    secs = int(delta.total_seconds())
    if secs < 60:
        return "just now"
    if secs < 3600:
        return f"{secs // 60}m ago"
    if secs < 86400:
        return f"{secs // 3600}h ago"
    if secs < 86400 * 7:
        return f"{secs // 86400}d ago"
    return dt.strftime("%b %d")


def recent_activity(user, limit=8):
    """Build the activity feed from real DB rows.

    Combines the user's most recent Project changes with their recent
    ChatMessages, ordered by recency.
    """
    items = []

    for p in Project.objects.filter(owner=user).order_by('-updated_at')[:limit]:
        verb = "Created" if p.created_at == p.updated_at else "Updated"
        items.append(("📦", f"{verb} project '{p.name}'", p.updated_at))

    for m in ChatMessage.objects.filter(user=user).order_by('-timestamp')[:limit]:
        snippet = m.content[:60] + ("…" if len(m.content) > 60 else "")
        items.append(("💬", f"In #{m.room.slug}: {snippet}", m.timestamp))

    items.sort(key=lambda t: t[2], reverse=True)
    items = items[:limit]

    if not items:
        return P("No activity yet. Create a project or join a chat to get started.", cls="empty-state")

    return Ul(*[activity_item(i, t, _format_when(w)) for (i, t, w) in items], cls="activity-list")


def new_project_form():
    return Form(
        H4("New project"),
        Input(type="text", name="name", placeholder="Project name", required=True, maxlength=120),
        Textarea(name="description", placeholder="What is it? (optional)", rows=3, maxlength=2000),
        Div(
            Label("AI %"),
            Input(type="number", name="ai_percentage", min=0, max=100, value=80),
            cls="form-row",
        ),
        Select(
            *[Option(label, value=val, selected=(val == 'in_progress')) for val, label in Project.STATUS_CHOICES if val != 'archived'],
            name="status",
        ),
        Input(type="url", name="repo_url", placeholder="Repo URL (optional)"),
        Input(type="url", name="live_url", placeholder="Live URL (optional)"),
        Button("Create", type="submit", cls="btn-primary"),
        hx_post="/dashboard/projects",
        hx_target="#projects-grid",
        hx_swap="afterbegin",
        cls="new-project-form",
    )


def assistant_widget():
    return Card(
        Form(
            Textarea(
                placeholder="Ask the AI anything — code review, debugging, architecture…",
                rows=3,
                cls="assistant-input",
                name="query",
                required=True,
            ),
            Button("Ask AI", type="submit", cls="assistant-submit btn-primary"),
            hx_post="/dashboard/ask",
            hx_target="#assistant-response",
            hx_swap="innerHTML",
        ),
        Div(id="assistant-response", cls="assistant-response"),
        cls="assistant-card",
    )


# ---------- Routes ----------

@rt('/dashboard')
def get(req, session):
    """Main dashboard: stats, projects, activity, AI assistant."""
    session['path'] = '/dashboard'

    user = AuthBridge.get_current_user(req, session)
    if not user:
        return RedirectResponse('/login', status_code=303)

    projects = list(Project.objects.filter(owner=user))
    active_count = sum(1 for p in projects if p.status in ('planned', 'in_progress'))
    completed_count = sum(1 for p in projects if p.status == 'completed')

    # Compute live AI % from active projects (fall back to user's stored value)
    if projects:
        avg_ai = round(sum(p.ai_percentage for p in projects) / len(projects))
    else:
        avg_ai = user.ai_percentage

    return Titled(
        f"Dashboard - {user.get_display_name()}",
        Container(
            SiteHeader(session),

            Section(
                Grid(
                    stat_card(f"{avg_ai}%", "AI-Generated Code", cls="highlight"),
                    stat_card(active_count, "Active Projects"),
                    stat_card(completed_count, "Completed"),
                    stat_card(user.challenge_count, "Challenges"),
                    cls="dashboard-stats",
                ),
                cls="dashboard-header",
            ),

            Section(
                Div(
                    H2("Your Projects"),
                    Button("+ New", cls="btn-primary new-project-btn",
                           hx_get="/dashboard/projects/new",
                           hx_target="#new-project-slot",
                           hx_swap="innerHTML"),
                    cls="section-header",
                ),
                Div(id="new-project-slot"),
                Grid(
                    *[project_card(p) for p in projects] if projects
                      else [P("No projects yet. Hit '+ New' to start one.", cls="empty-state")],
                    id="projects-grid",
                    cls="projects-grid",
                ),
                cls="projects-section",
            ),

            Section(
                H2("Recent Activity"),
                Card(recent_activity(user), cls="activity-card"),
                cls="activity-section",
            ),

            Section(
                H2("AI Assistant"),
                assistant_widget(),
                cls="assistant-section",
            ),
        ),
    )


@rt('/dashboard/projects/new')
def get(req, session):
    """Render the inline new-project form (HTMX target)."""
    user = AuthBridge.get_current_user(req, session)
    if not user:
        return RedirectResponse('/login', status_code=303)
    return new_project_form()


@rt('/dashboard/projects')
def post(req, session, name: str, description: str = "",
         ai_percentage: int = 0, status: str = "planned",
         repo_url: str = "", live_url: str = ""):
    """Create a real Project row and return the new card."""
    user = AuthBridge.get_current_user(req, session)
    if not user:
        return RedirectResponse('/login', status_code=303)

    name = (name or "").strip()
    if not name:
        return P("Project name is required.", cls="form-error")

    if status not in dict(Project.STATUS_CHOICES):
        status = 'planned'

    project = Project.objects.create(
        owner=user,
        name=name[:120],
        description=description[:2000],
        ai_percentage=max(0, min(100, ai_percentage or 0)),
        status=status,
        repo_url=repo_url.strip()[:200],
        live_url=live_url.strip()[:200],
    )

    add_toast(session, f"Project '{project.name}' created.", "success")
    return project_card(project)


@rt('/dashboard/project/{slug}')
def get(req, session, slug: str):
    """Detail view for a single project."""
    user = AuthBridge.get_current_user(req, session)
    if not user:
        return RedirectResponse('/login', status_code=303)

    try:
        project = Project.objects.get(owner=user, slug=slug)
    except Project.DoesNotExist:
        return RedirectResponse('/dashboard', status_code=303)

    return Titled(
        f"{project.name} - DeadDevelopers",
        Container(
            SiteHeader(session),
            Section(
                A("← Dashboard", href="/dashboard", cls="back-link"),
                H1(project.name),
                P(project.description or "No description.", cls="project-detail-description"),
                Div(
                    Span(STATUS_LABELS.get(project.status, project.status), cls=f"project-status status-{project.status.replace('_', '-')}"),
                    Span(f"AI {project.ai_percentage}%", cls="project-ai-pct"),
                    Span(f"Created {project.created_at:%b %d, %Y}", cls="project-meta-item"),
                    cls="project-detail-meta",
                ),
                Div(
                    A("Repository", href=project.repo_url, target="_blank", cls="btn-secondary") if project.repo_url else "",
                    A("Live site", href=project.live_url, target="_blank", cls="btn-secondary") if project.live_url else "",
                    cls="project-detail-links",
                ),
                cls="project-detail",
            ),
        ),
    )


@rt('/dashboard/project/{slug}')
def delete(req, session, slug: str):
    """Delete a project (HTMX target — returns empty so the card disappears)."""
    user = AuthBridge.get_current_user(req, session)
    if not user:
        return RedirectResponse('/login', status_code=303)

    Project.objects.filter(owner=user, slug=slug).delete()
    add_toast(session, "Project deleted.", "info")
    return ""


@rt('/dashboard/ask')
async def post(req, query: str, session):
    """AI assistant (OpenRouter-backed; see routes/ai.py)."""
    user = await AuthBridge.aget_current_user(req, session)
    if not user:
        return RedirectResponse('/login', status_code=303)

    response = await get_ai_response(query, user.id)
    return Card(
        H4("AI Assistant"),
        Pre(response, cls="ai-response"),
        cls="response-card",
    )
