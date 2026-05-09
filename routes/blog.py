"""
User blog — list, detail, write, edit, delete + tag filter.

Replaces the original 461-LOC static-mock /blog page (hardcoded "John Doe"
sample posts and a "Write a Post" button that linked to a /write-post
route that didn't exist) with real BlogPost CRUD against the model in
users/models.py.

Markdown rendering uses the same bleach-sanitization pipeline as the
user portfolio in routes/profile.py — XSS protection is shared, not
re-implemented.
"""
from fasthtml.common import *
from app import rt, User
from auth_bridge import AuthBridge, csrf_input
from routes.header import SiteHeader
from users.models import BlogPost, Tag
from django.db.models import Count, Q
import markdown
import bleach


# Same sanitizer config as routes/profile.py — keep them in lockstep.
POST_ALLOWED_TAGS = [
    "p", "br", "strong", "em", "code", "pre", "blockquote",
    "ul", "ol", "li", "a", "h1", "h2", "h3", "h4", "h5", "h6",
    "img", "hr", "table", "thead", "tbody", "tr", "th", "td",
    "div", "span",
]
POST_ALLOWED_ATTRS = {
    "*": ["class"],
    "a": ["href", "title", "rel"],
    "img": ["src", "alt", "title"],
    "code": ["class"],
}
POST_ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


def render_markdown(content: str) -> str:
    """Markdown → sanitized HTML. Returns empty string on empty input."""
    if not content:
        return ""
    rendered = markdown.markdown(content, extensions=['extra', 'codehilite'])
    return bleach.clean(
        rendered,
        tags=POST_ALLOWED_TAGS,
        attributes=POST_ALLOWED_ATTRS,
        protocols=POST_ALLOWED_PROTOCOLS,
        strip=True,
    )


def _read_minutes(content: str) -> int:
    """Rough read-time estimate at 200 wpm. Floor of 1 min."""
    if not content:
        return 1
    words = len(content.split())
    return max(1, round(words / 200))


# ---------- Components ----------

def post_card(post: BlogPost):
    """Compact card used in feeds and per-author lists."""
    tag_chips = [Span(t.name, cls="tag") for t in post.tags.all()[:5]]
    return Article(
        Div(
            Img(
                src=post.author.get_avatar_url(),
                alt=f"{post.author.get_display_name()}'s avatar",
                cls="author-avatar",
            ),
            Div(
                P(
                    A(
                        f"by {post.author.get_display_name()}",
                        href=f"/profile/{post.author.username}",
                        cls="author-name",
                    ),
                    cls="author-line",
                ),
                P(f"{_read_minutes(post.content)} min read", cls="read-time"),
                cls="post-meta",
            ),
            cls="post-header",
        ),
        H2(
            A(post.title, href=post.get_absolute_url(), cls="post-title-link"),
            cls="post-title",
        ),
        P(post.excerpt or "(no excerpt)", cls="post-description"),
        Div(*tag_chips, cls="tags") if tag_chips else "",
        cls="post-card",
    )


def trending_topics_sidebar(limit: int = 6):
    """Tags ranked by number of *published* posts they're attached to."""
    tags = (
        Tag.objects
        .annotate(post_count=Count('posts', filter=Q(posts__is_published=True)))
        .filter(post_count__gt=0)
        .order_by('-post_count')[:limit]
    )
    if not tags:
        return Section(
            H2("Trending Topics", cls="sidebar-title"),
            P("No tags yet. Be the first to write.", cls="empty-state"),
            cls="sidebar-section",
        )
    return Section(
        H2("Trending Topics", cls="sidebar-title"),
        Div(
            *[
                A(
                    Span(t.name, cls="topic-name"),
                    Span(f"{t.post_count} post{'s' if t.post_count != 1 else ''}", cls="topic-posts"),
                    href=f"/blog/tag/{t.slug}",
                    cls="topic-item",
                )
                for t in tags
            ],
            cls="topics-list",
        ),
        cls="sidebar-section",
    )


def popular_authors_sidebar(limit: int = 5):
    """Users ranked by number of published posts."""
    authors = (
        User.objects
        .annotate(post_count=Count('blog_posts', filter=Q(blog_posts__is_published=True)))
        .filter(post_count__gt=0)
        .order_by('-post_count')[:limit]
    )
    if not authors:
        return ""
    return Section(
        H2("Popular Authors", cls="sidebar-title"),
        Div(
            *[
                A(
                    Img(src=u.get_avatar_url(), alt=f"{u.username}", cls="author-avatar-sm"),
                    Span(u.get_display_name(), cls="author-name-sm"),
                    Span(f"{u.post_count} posts", cls="author-post-count"),
                    href=f"/profile/{u.username}",
                    cls="popular-author",
                )
                for u in authors
            ],
            cls="popular-authors-list",
        ),
        cls="sidebar-section",
    )


def write_button(is_authenticated: bool):
    href = "/blog/write" if is_authenticated else "/login?next=/blog/write"
    return A("✎ Write a Post", href=href, cls="write-post-btn btn-primary")


# ---------- Routes ----------

@rt('/blog')
def get(req, session):
    """Global blog feed — latest published posts across all users."""
    session['path'] = '/blog'

    user = AuthBridge.get_current_user(req, session)
    is_authed = user is not None

    posts = (
        BlogPost.objects
        .filter(is_published=True)
        .select_related('author')
        .prefetch_related('tags')
        [:30]
    )

    feed = (
        Div(*[post_card(p) for p in posts], cls="posts-grid")
        if posts
        else P("No posts published yet. Be the first.", cls="empty-state")
    )

    return Titled(
        "Blog | DeadDevelopers",
        Container(
            SiteHeader(session),
            Div(
                Div(
                    Div(
                        H1("Latest Posts", cls="section-title"),
                        write_button(is_authed),
                        cls="header section-header",
                    ),
                    feed,
                    cls="main-content",
                ),
                Div(
                    trending_topics_sidebar(),
                    popular_authors_sidebar(),
                    cls="sidebar",
                ),
                cls="blog-container",
            ),
        ),
    )


@rt('/blog/tag/{tag_slug}')
def get(req, session, tag_slug: str):
    """Posts filtered by tag."""
    session['path'] = f'/blog/tag/{tag_slug}'

    user = AuthBridge.get_current_user(req, session)
    is_authed = user is not None

    try:
        tag = Tag.objects.get(slug=tag_slug)
    except Tag.DoesNotExist:
        return RedirectResponse('/blog', status_code=303)

    posts = (
        tag.posts
        .filter(is_published=True)
        .select_related('author')
        .prefetch_related('tags')
        [:50]
    )

    feed = (
        Div(*[post_card(p) for p in posts], cls="posts-grid")
        if posts
        else P("No posts with this tag yet.", cls="empty-state")
    )

    return Titled(
        f"#{tag.name} | Blog | DeadDevelopers",
        Container(
            SiteHeader(session),
            Div(
                Div(
                    A("← All Posts", href="/blog", cls="back-link"),
                    Div(
                        H1(f"#{tag.name}", cls="section-title"),
                        write_button(is_authed),
                        cls="header section-header",
                    ),
                    feed,
                    cls="main-content",
                ),
                Div(
                    trending_topics_sidebar(),
                    popular_authors_sidebar(),
                    cls="sidebar",
                ),
                cls="blog-container",
            ),
        ),
    )


@rt('/blog/write')
def get(req, session):
    """New-post composer."""
    user = AuthBridge.get_current_user(req, session)
    if not user:
        session['next'] = '/blog/write'
        return RedirectResponse('/login', status_code=303)

    return Titled(
        "Write a Post | DeadDevelopers",
        Container(
            SiteHeader(session),
            Section(
                A("← Blog", href="/blog", cls="back-link"),
                H1("Write a Post"),
                Form(
                    csrf_input(req),
                    Div(
                        Label("Title", _for="title"),
                        Input(
                            type="text", name="title", id="title",
                            placeholder="Make it punchy",
                            required=True, maxlength=200,
                        ),
                        cls="form-group",
                    ),
                    Div(
                        Label("Excerpt (optional, autogenerated if blank)", _for="excerpt"),
                        Input(
                            type="text", name="excerpt", id="excerpt",
                            placeholder="One-line summary",
                            maxlength=400,
                        ),
                        cls="form-group",
                    ),
                    Div(
                        Label("Tags (comma-separated)", _for="tags"),
                        Input(
                            type="text", name="tags", id="tags",
                            placeholder="python, fastapi, ai",
                        ),
                        cls="form-group",
                    ),
                    Div(
                        Label("Content (Markdown)", _for="content"),
                        Textarea(
                            name="content", id="content",
                            placeholder="# Hello\n\nWrite something interesting…",
                            required=True, rows=18,
                        ),
                        P("Markdown supported. <script> tags and other XSS vectors are stripped automatically.", cls="help-text"),
                        cls="form-group",
                    ),
                    Div(
                        Div(
                            Input(type="checkbox", name="is_published", id="is_published", value="1", checked=True),
                            Label("Publish immediately (uncheck to save as draft)", _for="is_published"),
                            cls="checkbox-group",
                        ),
                        cls="form-group",
                    ),
                    Div(
                        Button("Save", type="submit", cls="btn-primary"),
                        A("Cancel", href="/blog", cls="btn-secondary"),
                        cls="form-actions",
                    ),
                    method="post",
                    action="/blog/write",
                    cls="blog-write-form",
                ),
                cls="blog-write-section",
            ),
        ),
    )


def _set_tags(post: BlogPost, raw: str):
    """Split a comma-separated tag string into Tag rows + attach to post."""
    names = [n.strip()[:40] for n in (raw or "").split(",") if n.strip()]
    if not names:
        post.tags.clear()
        return
    tag_objs = []
    for name in names[:10]:  # cap at 10 tags per post
        tag, _ = Tag.objects.get_or_create(name=name)
        tag_objs.append(tag)
    post.tags.set(tag_objs)


@rt('/blog/write')
def post(req, session,
         title: str, content: str,
         excerpt: str = "", tags: str = "",
         is_published: str = ""):
    """Create a new post."""
    user = AuthBridge.get_current_user(req, session)
    if not user:
        return RedirectResponse('/login', status_code=303)

    title = (title or "").strip()
    content = content or ""
    if not title or not content.strip():
        add_toast(session, "Title and content are required.", "error")
        return RedirectResponse('/blog/write', status_code=303)

    # Resolve slug collisions per-author by appending an integer suffix.
    from django.utils.text import slugify
    base_slug = slugify(title)[:200] or "untitled"
    slug = base_slug
    n = 2
    while BlogPost.objects.filter(author=user, slug=slug).exists():
        slug = f"{base_slug}-{n}"[:220]
        n += 1

    post = BlogPost.objects.create(
        author=user,
        title=title[:200],
        slug=slug,
        excerpt=excerpt[:400],
        content=content,
        is_published=bool(is_published),
    )
    _set_tags(post, tags)

    add_toast(
        session,
        "Post published." if post.is_published else "Draft saved.",
        "success",
    )
    return RedirectResponse(post.get_absolute_url(), status_code=303)


@rt('/blog/{username}/{slug}')
def get(req, session, username: str, slug: str):
    """Post detail view."""
    session['path'] = f'/blog/{username}/{slug}'

    try:
        post = (
            BlogPost.objects
            .select_related('author')
            .prefetch_related('tags')
            .get(author__username=username, slug=slug)
        )
    except BlogPost.DoesNotExist:
        return RedirectResponse('/blog', status_code=303)

    current = AuthBridge.get_current_user(req, session)
    is_owner = current is not None and current.id == post.author_id

    # Drafts are visible only to the author.
    if not post.is_published and not is_owner:
        return RedirectResponse('/blog', status_code=303)

    # Track views (cheap atomic UPDATE; skip for the author's own reads).
    if not is_owner:
        post.increment_views()

    body = render_markdown(post.content)
    tag_chips = [
        A(t.name, href=f"/blog/tag/{t.slug}", cls="tag")
        for t in post.tags.all()
    ]

    actions = ""
    if is_owner:
        actions = Div(
            A("Edit", href=f"/blog/{username}/{slug}/edit", cls="btn-secondary"),
            Form(
                csrf_input(req),
                Button("Delete", type="submit", cls="btn-danger"),
                method="post",
                action=f"/blog/{username}/{slug}/delete",
                onsubmit="return confirm('Delete this post? Cannot be undone.');",
            ),
            cls="post-owner-actions",
        )

    return Titled(
        f"{post.title} | {post.author.get_display_name()}",
        Container(
            SiteHeader(session),
            Article(
                A("← Blog", href="/blog", cls="back-link"),
                H1(post.title, cls="post-detail-title"),
                Div(
                    Img(
                        src=post.author.get_avatar_url(),
                        alt=f"{post.author.username}'s avatar",
                        cls="author-avatar",
                    ),
                    Div(
                        A(
                            post.author.get_display_name(),
                            href=f"/profile/{post.author.username}",
                            cls="author-name",
                        ),
                        Span(
                            f"{post.published_at:%b %d, %Y}" if post.published_at else "Draft",
                            cls="post-date",
                        ),
                        Span(f"{_read_minutes(post.content)} min read", cls="read-time"),
                        Span(f"{post.view_count} views", cls="view-count"),
                        cls="post-meta",
                    ),
                    cls="post-author-block",
                ),
                Div(*tag_chips, cls="tags") if tag_chips else "",
                Div(NotStr(body), cls="post-body"),
                actions,
                cls="post-detail",
            ),
        ),
    )


@rt('/blog/{username}/{slug}/edit')
def get(req, session, username: str, slug: str):
    """Edit form for an existing post (owner only)."""
    user = AuthBridge.get_current_user(req, session)
    if not user or user.username != username:
        return RedirectResponse('/blog', status_code=303)

    try:
        post = BlogPost.objects.prefetch_related('tags').get(author=user, slug=slug)
    except BlogPost.DoesNotExist:
        return RedirectResponse('/blog', status_code=303)

    tags_str = ", ".join(t.name for t in post.tags.all())

    return Titled(
        f"Edit: {post.title} | DeadDevelopers",
        Container(
            SiteHeader(session),
            Section(
                A("← Post", href=post.get_absolute_url(), cls="back-link"),
                H1("Edit Post"),
                Form(
                    csrf_input(req),
                    Div(
                        Label("Title", _for="title"),
                        Input(type="text", name="title", id="title", value=post.title, required=True, maxlength=200),
                        cls="form-group",
                    ),
                    Div(
                        Label("Excerpt", _for="excerpt"),
                        Input(type="text", name="excerpt", id="excerpt", value=post.excerpt, maxlength=400),
                        cls="form-group",
                    ),
                    Div(
                        Label("Tags (comma-separated)", _for="tags"),
                        Input(type="text", name="tags", id="tags", value=tags_str),
                        cls="form-group",
                    ),
                    Div(
                        Label("Content (Markdown)", _for="content"),
                        Textarea(post.content, name="content", id="content", required=True, rows=18),
                        cls="form-group",
                    ),
                    Div(
                        Div(
                            Input(type="checkbox", name="is_published", id="is_published", value="1", checked=post.is_published),
                            Label("Published", _for="is_published"),
                            cls="checkbox-group",
                        ),
                        cls="form-group",
                    ),
                    Div(
                        Button("Save", type="submit", cls="btn-primary"),
                        A("Cancel", href=post.get_absolute_url(), cls="btn-secondary"),
                        cls="form-actions",
                    ),
                    method="post",
                    action=f"/blog/{username}/{slug}/edit",
                    cls="blog-write-form",
                ),
                cls="blog-write-section",
            ),
        ),
    )


@rt('/blog/{username}/{slug}/edit')
def post(req, session, username: str, slug: str,
         title: str, content: str,
         excerpt: str = "", tags: str = "",
         is_published: str = ""):
    """Save edits to an existing post (owner only)."""
    user = AuthBridge.get_current_user(req, session)
    if not user or user.username != username:
        return RedirectResponse('/blog', status_code=303)

    try:
        post = BlogPost.objects.get(author=user, slug=slug)
    except BlogPost.DoesNotExist:
        return RedirectResponse('/blog', status_code=303)

    title = (title or "").strip()
    if not title or not (content or "").strip():
        add_toast(session, "Title and content are required.", "error")
        return RedirectResponse(f'/blog/{username}/{slug}/edit', status_code=303)

    post.title = title[:200]
    post.excerpt = excerpt[:400]
    post.content = content
    post.is_published = bool(is_published)
    post.save()
    _set_tags(post, tags)

    add_toast(session, "Post updated.", "success")
    return RedirectResponse(post.get_absolute_url(), status_code=303)


@rt('/blog/{username}/{slug}/delete')
def post(req, session, username: str, slug: str):
    """Delete a post (owner only)."""
    user = AuthBridge.get_current_user(req, session)
    if not user or user.username != username:
        return RedirectResponse('/blog', status_code=303)

    BlogPost.objects.filter(author=user, slug=slug).delete()
    add_toast(session, "Post deleted.", "info")
    return RedirectResponse('/blog', status_code=303)
