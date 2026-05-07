from fasthtml.common import *
from app import app, rt
from routes.header import SiteHeader
from django.shortcuts import get_object_or_404
from users.models import User
import markdown
import bleach

# Tags + attrs allowed in user-rendered portfolio markdown.
# Anything else (script, iframe, on* handlers, etc.) is stripped.
PORTFOLIO_ALLOWED_TAGS = [
    "p", "br", "strong", "em", "code", "pre", "blockquote",
    "ul", "ol", "li", "a", "h1", "h2", "h3", "h4", "h5", "h6",
    "img", "hr", "table", "thead", "tbody", "tr", "th", "td",
    "div", "span",
]
PORTFOLIO_ALLOWED_ATTRS = {
    "*": ["class"],
    "a": ["href", "title", "rel"],
    "img": ["src", "alt", "title"],
    "code": ["class"],
}
PORTFOLIO_ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


@rt('/profile/{username}')
def get(username: str, session, req):
    """Display a user's profile page"""
    # Store current path in session
    session['path'] = f'/profile/{username}'
    
    # Get the user or 404
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Titled(
            "User Not Found",
            Container(
                SiteHeader(session),
                Section(
                    H1("User Not Found"),
                    P(f"The user '{username}' does not exist."),
                    A("← Back to Home", href="/", cls="btn-secondary"),
                    cls="error-section"
                )
            )
        )
    
    # Check if profile is public or if viewing own profile
    from auth_bridge import AuthBridge
    current_user = AuthBridge.get_current_user(req, session)
    is_own_profile = current_user and current_user.id == profile_user.id
    
    if not profile_user.is_public and not is_own_profile:
        return Titled(
            "Private Profile",
            Container(
                SiteHeader(session),
                Section(
                    H1("Private Profile"),
                    P(f"This profile is private."),
                    A("← Back to Home", href="/", cls="btn-secondary"),
                    cls="error-section"
                )
            )
        )
    
    # Convert portfolio markdown to HTML, then sanitize against XSS.
    # markdown.markdown() does NOT strip raw HTML tags, so untrusted user
    # content could inject <script> or event handlers without bleach.
    portfolio_html = ""
    if profile_user.portfolio_content:
        rendered = markdown.markdown(
            profile_user.portfolio_content,
            extensions=['extra', 'codehilite']
        )
        portfolio_html = bleach.clean(
            rendered,
            tags=PORTFOLIO_ALLOWED_TAGS,
            attributes=PORTFOLIO_ALLOWED_ATTRS,
            protocols=PORTFOLIO_ALLOWED_PROTOCOLS,
            strip=True,
        )
    
    return Titled(
        f"{profile_user.get_display_name()} - Profile",
        Container(
            SiteHeader(session),
            
            # Profile CSS
            Style("""
                .profile-container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 2rem 1rem;
                }
                
                .profile-header {
                    display: flex;
                    gap: 2rem;
                    align-items: flex-start;
                    margin-bottom: 3rem;
                    padding: 2rem;
                    background: #1a1a1a;
                    border: 1px solid #00ff66;
                    border-radius: 8px;
                }
                
                .profile-avatar {
                    flex-shrink: 0;
                }
                
                .profile-avatar img {
                    width: 150px;
                    height: 150px;
                    border-radius: 50%;
                    border: 3px solid #00ff66;
                    object-fit: cover;
                }
                
                .profile-info {
                    flex-grow: 1;
                }
                
                .profile-name {
                    font-size: 2rem;
                    margin: 0 0 0.5rem 0;
                    color: #00ff66;
                }
                
                .profile-username {
                    font-size: 1.2rem;
                    color: #888;
                    margin: 0 0 1rem 0;
                }
                
                .profile-tagline {
                    font-size: 1.1rem;
                    color: #ccc;
                    margin: 0 0 1rem 0;
                    font-style: italic;
                }
                
                .profile-bio {
                    color: #fff;
                    line-height: 1.6;
                    margin-bottom: 1rem;
                }
                
                .profile-meta {
                    display: flex;
                    gap: 2rem;
                    flex-wrap: wrap;
                    margin-top: 1rem;
                }
                
                .profile-meta-item {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    color: #ccc;
                }
                
                .profile-stats {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 1rem;
                    margin-bottom: 3rem;
                }
                
                .stat-card {
                    background: #1a1a1a;
                    border: 1px solid #333;
                    border-radius: 8px;
                    padding: 1.5rem;
                    text-align: center;
                }
                
                .stat-value {
                    font-size: 2.5rem;
                    color: #00ff66;
                    font-weight: bold;
                    margin: 0;
                }
                
                .stat-label {
                    color: #888;
                    margin: 0.5rem 0 0 0;
                }
                
                .profile-social {
                    display: flex;
                    gap: 1rem;
                    flex-wrap: wrap;
                    margin-top: 1rem;
                }
                
                .social-link {
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                    padding: 0.5rem 1rem;
                    background: #2a2a2a;
                    border: 1px solid #00ff66;
                    border-radius: 4px;
                    color: #00ff66;
                    text-decoration: none;
                    transition: all 0.3s;
                }
                
                .social-link:hover {
                    background: #00ff66;
                    color: #000;
                }
                
                .portfolio-section {
                    background: #1a1a1a;
                    border: 1px solid #333;
                    border-radius: 8px;
                    padding: 2rem;
                    margin-bottom: 2rem;
                }
                
                .portfolio-section h2 {
                    color: #00ff66;
                    margin-top: 0;
                }
                
                .portfolio-content {
                    color: #fff;
                    line-height: 1.8;
                }
                
                .portfolio-content pre {
                    background: #0a0a0a;
                    border: 1px solid #333;
                    border-radius: 4px;
                    padding: 1rem;
                    overflow-x: auto;
                }
                
                .portfolio-content code {
                    color: #00ff66;
                    font-family: 'JetBrains Mono', monospace;
                }
                
                .edit-profile-btn {
                    display: inline-block;
                    padding: 0.75rem 1.5rem;
                    background: #00ff66;
                    color: #000;
                    text-decoration: none;
                    border-radius: 4px;
                    font-weight: bold;
                    transition: all 0.3s;
                }
                
                .edit-profile-btn:hover {
                    background: #00cc52;
                    transform: translateY(-2px);
                }
                
                @media (max-width: 768px) {
                    .profile-header {
                        flex-direction: column;
                        align-items: center;
                        text-align: center;
                    }
                    
                    .profile-meta {
                        justify-content: center;
                    }
                }
            """),
            
            Div(
                # Profile Header
                Div(
                    Div(
                        Img(src=profile_user.get_avatar_url(), alt=f"{profile_user.get_display_name()}'s avatar"),
                        cls="profile-avatar"
                    ),
                    Div(
                        H1(profile_user.get_display_name(), cls="profile-name"),
                        P(f"@{profile_user.username}", cls="profile-username"),
                        P(profile_user.tagline, cls="profile-tagline") if profile_user.tagline else None,
                        P(profile_user.bio, cls="profile-bio") if profile_user.bio else None,
                        
                        # Meta information
                        Div(
                            Div("📍 " + profile_user.location, cls="profile-meta-item") if profile_user.location else None,
                            Div("📧 " + profile_user.email, cls="profile-meta-item") if profile_user.show_email else None,
                            Div(f"📅 Joined {profile_user.date_joined.strftime('%B %Y')}", cls="profile-meta-item"),
                            cls="profile-meta"
                        ),
                        
                        # Social links
                        Div(
                            A("🐙 GitHub", href=f"https://github.com/{profile_user.github_username}", 
                              target="_blank", cls="social-link") if profile_user.github_username else None,
                            A("🐦 Twitter", href=f"https://twitter.com/{profile_user.twitter_username}", 
                              target="_blank", cls="social-link") if profile_user.twitter_username else None,
                            A("💼 LinkedIn", href=f"https://linkedin.com/in/{profile_user.linkedin_username}", 
                              target="_blank", cls="social-link") if profile_user.linkedin_username else None,
                            A("🌐 Website", href=profile_user.website, 
                              target="_blank", cls="social-link") if profile_user.website else None,
                            A("📁 Portfolio", href=profile_user.portfolio_url, 
                              target="_blank", cls="social-link") if profile_user.portfolio_url else None,
                            cls="profile-social"
                        ) if any([profile_user.github_username, profile_user.twitter_username, 
                                 profile_user.linkedin_username, profile_user.website, profile_user.portfolio_url]) else None,
                        
                        # Edit button (only for own profile)
                        A("✏️ Edit Profile", href=f"/profile/{username}/edit", cls="edit-profile-btn") if is_own_profile else None,
                        
                        cls="profile-info"
                    ),
                    cls="profile-header"
                ),
                
                # Stats
                Div(
                    Div(
                        H2(f"{profile_user.ai_percentage}%", cls="stat-value"),
                        P("AI-Generated Code", cls="stat-label"),
                        cls="stat-card"
                    ),
                    Div(
                        H2(str(profile_user.completed_projects), cls="stat-value"),
                        P("Completed Projects", cls="stat-label"),
                        cls="stat-card"
                    ),
                    Div(
                        H2(str(profile_user.challenge_count), cls="stat-value"),
                        P("Challenges Completed", cls="stat-label"),
                        cls="stat-card"
                    ),
                    cls="profile-stats"
                ),
                
                # Portfolio
                Div(
                    H2("Portfolio"),
                    Div(
                        NotStr(portfolio_html) if portfolio_html else P("No portfolio content yet.", style="color: #888;"),
                        cls="portfolio-content"
                    ),
                    cls="portfolio-section"
                ) if portfolio_html or is_own_profile else None,
                
                cls="profile-container"
            )
        )
    )



@rt('/profile/{username}/edit')
def get(username: str, session, req):
    """Display the profile edit form"""
    # Store current path in session
    session['path'] = f'/profile/{username}/edit'

    # Get the current user
    from auth_bridge import AuthBridge, csrf_input
    current_user = AuthBridge.get_current_user(req, session)
    
    # Check authentication
    if not current_user:
        session['next'] = f'/profile/{username}/edit'
        return RedirectResponse('/login', status_code=303)
    
    # Check if user is editing their own profile
    if current_user.username != username:
        return Titled(
            "Unauthorized",
            Container(
                SiteHeader(session),
                Section(
                    H1("Unauthorized"),
                    P("You can only edit your own profile."),
                    A("← Back to Profile", href=f"/profile/{username}", cls="btn-secondary"),
                    cls="error-section"
                )
            )
        )
    
    return Titled(
        "Edit Profile",
        Container(
            SiteHeader(session),
            
            Style("""
                .edit-profile-container {
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 2rem 1rem;
                }
                
                .edit-profile-form {
                    background: #1a1a1a;
                    border: 1px solid #00ff66;
                    border-radius: 8px;
                    padding: 2rem;
                }
                
                .form-section {
                    margin-bottom: 2rem;
                }
                
                .form-section h2 {
                    color: #00ff66;
                    margin-top: 0;
                    margin-bottom: 1rem;
                    font-size: 1.5rem;
                }
                
                .form-group {
                    margin-bottom: 1.5rem;
                }
                
                .form-group label {
                    display: block;
                    color: #00ff66;
                    margin-bottom: 0.5rem;
                    font-weight: bold;
                }
                
                .form-group input[type="text"],
                .form-group input[type="email"],
                .form-group input[type="url"],
                .form-group textarea,
                .form-group select {
                    width: 100%;
                    padding: 0.75rem;
                    background: #0a0a0a;
                    border: 1px solid #333;
                    border-radius: 4px;
                    color: #fff;
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 1rem;
                }
                
                .form-group textarea {
                    min-height: 150px;
                    resize: vertical;
                }
                
                .form-group input:focus,
                .form-group textarea:focus,
                .form-group select:focus {
                    outline: none;
                    border-color: #00ff66;
                }
                
                .form-group .help-text {
                    font-size: 0.875rem;
                    color: #888;
                    margin-top: 0.25rem;
                }
                
                .checkbox-group {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                
                .checkbox-group input[type="checkbox"] {
                    width: auto;
                }
                
                .form-actions {
                    display: flex;
                    gap: 1rem;
                    margin-top: 2rem;
                }
                
                .btn-primary {
                    padding: 0.75rem 1.5rem;
                    background: #00ff66;
                    color: #000;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.3s;
                }
                
                .btn-primary:hover {
                    background: #00cc52;
                    transform: translateY(-2px);
                }
                
                .btn-secondary {
                    padding: 0.75rem 1.5rem;
                    background: #2a2a2a;
                    color: #00ff66;
                    border: 1px solid #00ff66;
                    border-radius: 4px;
                    text-decoration: none;
                    display: inline-block;
                    transition: all 0.3s;
                }
                
                .btn-secondary:hover {
                    background: #3a3a3a;
                }
            """),
            
            Div(
                H1("Edit Profile"),
                
                Form(
                    csrf_input(req),  # CSRF protection
                    # Personal Information
                    Div(
                        H2("Personal Information"),
                        Div(
                            Label("Avatar", _for="avatar"),
                            Input(type="file", name="avatar", id="avatar", accept="image/*"),
                            P("Upload a profile picture (max 5MB, JPG/PNG/GIF/WEBP)", cls="help-text"),
                            cls="form-group"
                        ),
                        Div(
                            Label("First Name", _for="first_name"),
                            Input(type="text", name="first_name", id="first_name", 
                                  value=current_user.first_name or ""),
                            cls="form-group"
                        ),
                        Div(
                            Label("Last Name", _for="last_name"),
                            Input(type="text", name="last_name", id="last_name", 
                                  value=current_user.last_name or ""),
                            cls="form-group"
                        ),
                        Div(
                            Label("Tagline", _for="tagline"),
                            Input(type="text", name="tagline", id="tagline", 
                                  value=current_user.tagline or "", 
                                  placeholder="e.g., Full-stack developer & AI enthusiast"),
                            P("A short headline that appears on your profile", cls="help-text"),
                            cls="form-group"
                        ),
                        Div(
                            Label("Bio", _for="bio"),
                            Textarea(current_user.bio or "", name="bio", id="bio", 
                                    placeholder="Tell us about yourself..."),
                            cls="form-group"
                        ),
                        Div(
                            Label("Location", _for="location"),
                            Input(type="text", name="location", id="location", 
                                  value=current_user.location or "", 
                                  placeholder="e.g., San Francisco, CA"),
                            cls="form-group"
                        ),
                        cls="form-section"
                    ),
                    
                    # Social Links
                    Div(
                        H2("Social Links"),
                        Div(
                            Label("GitHub Username", _for="github_username"),
                            Input(type="text", name="github_username", id="github_username", 
                                  value=current_user.github_username or "", 
                                  placeholder="username"),
                            cls="form-group"
                        ),
                        Div(
                            Label("Twitter Username", _for="twitter_username"),
                            Input(type="text", name="twitter_username", id="twitter_username", 
                                  value=current_user.twitter_username or "", 
                                  placeholder="username"),
                            cls="form-group"
                        ),
                        Div(
                            Label("LinkedIn Username", _for="linkedin_username"),
                            Input(type="text", name="linkedin_username", id="linkedin_username", 
                                  value=current_user.linkedin_username or "", 
                                  placeholder="username"),
                            cls="form-group"
                        ),
                        Div(
                            Label("Website", _for="website"),
                            Input(type="url", name="website", id="website", 
                                  value=current_user.website or "", 
                                  placeholder="https://yourwebsite.com"),
                            cls="form-group"
                        ),
                        Div(
                            Label("External Portfolio URL", _for="portfolio_url"),
                            Input(type="url", name="portfolio_url", id="portfolio_url", 
                                  value=current_user.portfolio_url or "", 
                                  placeholder="https://portfolio.com"),
                            cls="form-group"
                        ),
                        cls="form-section"
                    ),
                    
                    # Portfolio Content
                    Div(
                        H2("Portfolio"),
                        Div(
                            Label("Portfolio Content (Markdown)", _for="portfolio_content"),
                            Textarea(current_user.portfolio_content or "", 
                                    name="portfolio_content", id="portfolio_content",
                                    placeholder="# My Projects\n\n## Project 1\nDescription here..."),
                            P("Use Markdown to format your portfolio. Supports headings, lists, code blocks, etc.", 
                              cls="help-text"),
                            cls="form-group"
                        ),
                        cls="form-section"
                    ),
                    
                    # Privacy Settings
                    Div(
                        H2("Privacy Settings"),
                        Div(
                            Div(
                                Input(type="checkbox", name="is_public", id="is_public", 
                                      checked=current_user.is_public),
                                Label("Make my profile public", _for="is_public"),
                                cls="checkbox-group"
                            ),
                            P("If unchecked, only you can see your profile", cls="help-text"),
                            cls="form-group"
                        ),
                        Div(
                            Div(
                                Input(type="checkbox", name="show_email", id="show_email", 
                                      checked=current_user.show_email),
                                Label("Show my email on my profile", _for="show_email"),
                                cls="checkbox-group"
                            ),
                            cls="form-group"
                        ),
                        cls="form-section"
                    ),
                    
                    # Preferences
                    Div(
                        H2("Preferences"),
                        Div(
                            Label("Theme", _for="theme_preference"),
                            Select(
                                Option("Dark", value="dark", selected=(current_user.theme_preference == "dark")),
                                Option("Light", value="light", selected=(current_user.theme_preference == "light")),
                                name="theme_preference", id="theme_preference"
                            ),
                            cls="form-group"
                        ),
                        cls="form-section"
                    ),
                    
                    # Form Actions
                    Div(
                        Button("Save Changes", type="submit", cls="btn-primary"),
                        A("Cancel", href=f"/profile/{username}", cls="btn-secondary"),
                        cls="form-actions"
                    ),
                    
                    method="post",
                    action=f"/profile/{username}/edit",
                    enctype="multipart/form-data",
                    cls="edit-profile-form"
                ),
                
                cls="edit-profile-container"
            )
        )
    )


@rt('/profile/{username}/edit')
async def post(username: str, session, req):
    """Handle profile update form submission"""
    # Get the current user
    from auth_bridge import AuthBridge
    current_user = AuthBridge.get_current_user(req, session)
    
    # Check authentication
    if not current_user:
        return RedirectResponse('/login', status_code=303)
    
    # Check if user is editing their own profile
    if current_user.username != username:
        return RedirectResponse(f'/profile/{username}', status_code=303)
    
    # Get form data
    form_data = await req.form()
    
    # Handle avatar upload
    avatar_file = form_data.get('avatar')
    if avatar_file and hasattr(avatar_file, 'filename') and avatar_file.filename:
        # Validate file type
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        import os
        file_ext = os.path.splitext(avatar_file.filename)[1].lower()
        
        if file_ext in allowed_extensions:
            # Validate file size (max 5MB)
            avatar_content = await avatar_file.read()
            if len(avatar_content) <= 5 * 1024 * 1024:  # 5MB
                # Save the file
                from django.core.files.uploadedfile import SimpleUploadedFile
                uploaded_file = SimpleUploadedFile(
                    name=f"{username}_avatar{file_ext}",
                    content=avatar_content,
                    content_type=avatar_file.content_type
                )
                current_user.avatar = uploaded_file
            else:
                session['flash_error'] = "Avatar file is too large (max 5MB)"
        else:
            session['flash_error'] = "Invalid file type. Please upload JPG, PNG, GIF, or WEBP"
    
    # Update user fields
    current_user.first_name = form_data.get('first_name', '')
    current_user.last_name = form_data.get('last_name', '')
    current_user.tagline = form_data.get('tagline', '')
    current_user.bio = form_data.get('bio', '')
    current_user.location = form_data.get('location', '')
    current_user.github_username = form_data.get('github_username', '')
    current_user.twitter_username = form_data.get('twitter_username', '')
    current_user.linkedin_username = form_data.get('linkedin_username', '')
    current_user.website = form_data.get('website', '')
    current_user.portfolio_url = form_data.get('portfolio_url', '')
    current_user.portfolio_content = form_data.get('portfolio_content', '')
    current_user.is_public = 'is_public' in form_data
    current_user.show_email = 'show_email' in form_data
    current_user.theme_preference = form_data.get('theme_preference', 'dark')
    
    # Save to database
    current_user.save()
    
    # Redirect back to profile with success message
    session['flash_message'] = "Profile updated successfully!"
    return RedirectResponse(f'/profile/{username}', status_code=303)
