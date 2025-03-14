from fasthtml.common import *
from app import rt
from starlette.responses import RedirectResponse

@rt('/blog')
def get(req):
    """Blog page for DeadDevelopers platform"""
    # Check if user is authenticated
    is_authenticated = req.scope.get('auth') is not None
    
    # Create write post button with appropriate action
    write_post_btn = Button(
        Svg(
            Path(d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"),
            viewBox="0 0 24 24",
            cls="write-icon"
        ),
        "Write a Post",
        cls="write-post-btn",
        # If authenticated, this would point to a write post page
        # If not authenticated, redirect to login
        onclick="window.location.href = '" + ('/write-post' if is_authenticated else '/login') + "'"
    )
    
    return Titled(
        "DeadDevelopers Blog",
        Div(
            # Add blog-specific CSS
            Style("""
                /* Base styles and CSS variables */
                :root {
                  --color-background: #1a1a1a;
                  --color-card: #2a2a2a;
                  --color-accent: #00ff66;
                  --color-text: #ffffff;
                  --color-text-secondary: #cccccc;
                  --border-radius: 8px;
                  --spacing-unit: 1rem;
                }

                * {
                  margin: 0;
                  padding: 0;
                  box-sizing: border-box;
                }

                /* Layout */
                .blog-container {
                  display: grid;
                  grid-template-columns: 1fr;
                  gap: var(--spacing-unit);
                  max-width: 1400px;
                  margin: 0 auto;
                  padding: var(--spacing-unit);
                  margin-top: 3rem;
                }

                .section-title {
                  font-size: clamp(1.5rem, 3vw, 2rem);
                  font-weight: 600;
                }

                .write-post-btn {
                  display: flex;
                  align-items: center;
                  gap: 0.5rem;
                  background-color: var(--color-accent);
                  color: var(--color-background);
                  border: none;
                  border-radius: var(--border-radius);
                  padding: 0.75rem 1rem;
                  font-size: 0.875rem;
                  font-weight: 500;
                  cursor: pointer;
                  transition: transform 0.2s ease, box-shadow 0.2s ease;
                }

                .write-post-btn:hover {
                  transform: translateY(-2px);
                  box-shadow: 0 4px 12px rgba(0, 255, 102, 0.2);
                }

                .write-icon {
                  width: 1.25rem;
                  height: 1.25rem;
                  fill: currentColor;
                }

                /* Posts Grid */
                .posts-grid {
                  display: grid;
                  gap: var(--spacing-unit);
                }

                .post-card {
                  background-color: var(--color-card);
                  border-radius: var(--border-radius);
                  padding: 1.5rem;
                  transition: transform 0.2s ease;
                }

                .post-card:hover {
                  transform: translateY(-4px);
                }

                .post-header {
                  display: flex;
                  align-items: center;
                  gap: 0.75rem;
                  margin-bottom: 1rem;
                }

                .author-avatar {
                  width: 2.5rem;
                  height: 2.5rem;
                  border-radius: 50%;
                  object-fit: cover;
                }

                .post-meta {
                  font-size: 0.875rem;
                }

                .author-name {
                  color: var(--color-text);
                  font-weight: 500;
                }

                .read-time {
                  color: var(--color-text-secondary);
                }

                .post-title {
                  font-size: 1.25rem;
                  font-weight: 600;
                  margin-bottom: 0.75rem;
                }

                .post-description {
                  color: var(--color-text-secondary);
                  font-size: 0.875rem;
                  margin-bottom: 1rem;
                }

                .tags {
                  display: flex;
                  gap: 0.5rem;
                  flex-wrap: wrap;
                }

                .tag {
                  background-color: rgba(0, 255, 102, 0.1);
                  color: var(--color-accent);
                  padding: 0.25rem 0.75rem;
                  border-radius: 1rem;
                  font-size: 0.75rem;
                  font-weight: 500;
                }

                /* Sidebar */
                .sidebar {
                  display: flex;
                  flex-direction: column;
                  gap: var(--spacing-unit);
                }

                .sidebar-section {
                  background-color: var(--color-card);
                  border-radius: var(--border-radius);
                  padding: 1.5rem;
                }

                .sidebar-title {
                  font-size: 1.25rem;
                  font-weight: 600;
                  margin-bottom: 1rem;
                }

                /* Topics List */
                .topics-list {
                  display: flex;
                  flex-direction: column;
                  gap: 0.75rem;
                }

                .topic-item {
                  display: flex;
                  justify-content: space-between;
                  align-items: center;
                  padding: 0.5rem 0;
                }

                .topic-name {
                  color: var(--color-accent);
                  font-weight: 500;
                }

                .topic-posts {
                  color: var(--color-text-secondary);
                  font-size: 0.875rem;
                }

                /* Authors List */
                .authors-list {
                  display: flex;
                  flex-direction: column;
                  gap: 1rem;
                }

                .author-item {
                  display: flex;
                  align-items: center;
                  gap: 0.75rem;
                }

                .author-info {
                  display: flex;
                  flex-direction: column;
                }

                .author-role {
                  color: var(--color-text-secondary);
                  font-size: 0.875rem;
                }

                /* Responsive Design */
                @media (min-width: 768px) {
                  .blog-container {
                    grid-template-columns: 2fr 1fr;
                    gap: 2rem;
                    padding: 2rem;
                  }

                  .posts-grid {
                    gap: 1.5rem;
                  }
                }

                @media (min-width: 1024px) {
                  .blog-container {
                    padding: 3rem;
                  }

                  .post-card {
                    padding: 2rem;
                  }
                }

                /* Touch Device Optimizations */
                @media (hover: none) {
                  .post-card:hover {
                    transform: none;
                  }

                  .write-post-btn:hover {
                    transform: none;
                    box-shadow: none;
                  }
                }

                /* Accessibility */
                @media (prefers-reduced-motion: reduce) {
                  .post-card,
                  .write-post-btn {
                    transition: none;
                  }
                }

                /* Focus States */
                .write-post-btn:focus-visible,
                .post-card:focus-visible {
                  outline: 2px solid var(--color-accent);
                  outline-offset: 2px;
                }
            """),
            
            # Blog Container
            Div(
                # Main Content
                Div(
                    # Header/Navigation - Using the same structure as in features.py
                    Header(
                        Nav(
                            Div(
                                A(
                                    Div(
                                        Img(src="/img/logo.png", cls="nav-logo"),
                                        Span("DEADDEVELOPERS", cls="nav-text"),
                                        cls="nav-logo-container"
                                    ),
                                    href="/",
                                    cls="brand-logo"
                                ),
                                Button("☰", cls="menu-button", onclick="menuButton.click();"),
                                cls="nav-left"
                            ),
                            Div(
                                A("/Features", href="/features"),
                                A("/Community", href="/community"),
                                A("/Blog", href="/blog"),
                                A("/About", href="/about"),
                                cls="nav-center"
                            ),
                            Div(
                                A("Log in", href="/login", cls="nav-login"),
                                A("Sign up", href="/signup", cls="nav-signup"),
                                cls="nav-right"
                            ),
                            cls="main-nav"
                        ),
                        cls="site-header"
                    ),
                    
                    # Write Post Button Section
                    Div(
                        H1("Latest Posts", cls="section-title"),
                        write_post_btn,
                        cls="header",
                        style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--spacing-unit); margin-top: 2rem;"
                    ),
                    
                    # Posts Grid
                    Div(
                        # Post Card 1
                        Article(
                            Div(
                                Img(src="/placeholder.svg?height=40&width=40", alt="John Doe", cls="author-avatar"),
                                Div(
                                    P("by John Doe", cls="author-name"),
                                    P("5 min read", cls="read-time"),
                                    cls="post-meta"
                                ),
                                cls="post-header"
                            ),
                            H2("Building Scalable APIs with Node.js", cls="post-title"),
                            P("Learn how to build robust and scalable APIs using Node.js and Express framework with best practices...", cls="post-description"),
                            Div(
                                Span("NodeJS", cls="tag"),
                                Span("API", cls="tag"),
                                cls="tags"
                            ),
                            cls="post-card"
                        ),
                        
                        # Post Card 2
                        Article(
                            Div(
                                Img(src="/placeholder.svg?height=40&width=40", alt="Jane Smith", cls="author-avatar"),
                                Div(
                                    P("by Jane Smith", cls="author-name"),
                                    P("8 min read", cls="read-time"),
                                    cls="post-meta"
                                ),
                                cls="post-header"
                            ),
                            H2("Understanding React Hooks", cls="post-title"),
                            P("Deep dive into React Hooks and how they revolutionize state management in functional components...", cls="post-description"),
                            Div(
                                Span("React", cls="tag"),
                                Span("JavaScript", cls="tag"),
                                cls="tags"
                            ),
                            cls="post-card"
                        ),
                        
                        cls="posts-grid"
                    ),
                    
                    cls="main-content"
                ),
                
                # Sidebar
                Div(
                    # Trending Topics Section
                    Section(
                        H2("Trending Topics", cls="sidebar-title"),
                        Div(
                            # Topic Item 1
                            Div(
                                Span("JavaScript", cls="topic-name"),
                                Span("2.5k posts", cls="topic-posts"),
                                cls="topic-item"
                            ),
                            # Topic Item 2
                            Div(
                                Span("Python", cls="topic-name"),
                                Span("1.8k posts", cls="topic-posts"),
                                cls="topic-item"
                            ),
                            # Topic Item 3
                            Div(
                                Span("DevOps", cls="topic-name"),
                                Span("1.2k posts", cls="topic-posts"),
                                cls="topic-item"
                            ),
                            cls="topics-list"
                        ),
                        cls="sidebar-section"
                    ),
                    
                    # Popular Authors Section
                    Section(
                        H2("Popular Authors", cls="sidebar-title"),
                        Div(
                            # Author Item 1
                            Div(
                                Img(src="/placeholder.svg?height=40&width=40", alt="Alex Johnson", cls="author-avatar"),
                                Div(
                                    P("Alex Johnson", cls="author-name"),
                                    P("Frontend Expert", cls="author-role"),
                                    cls="author-info"
                                ),
                                cls="author-item"
                            ),
                            # Author Item 2
                            Div(
                                Img(src="/placeholder.svg?height=40&width=40", alt="Sarah Miller", cls="author-avatar"),
                                Div(
                                    P("Sarah Miller", cls="author-name"),
                                    P("DevOps Engineer", cls="author-role"),
                                    cls="author-info"
                                ),
                                cls="author-item"
                            ),
                            cls="authors-list"
                        ),
                        cls="sidebar-section"
                    ),
                    
                    cls="sidebar"
                    
                ),
                
                cls="blog-container"
            ),
            
            # Footer
            Footer(
                Div(
                    Div(
                        Img(src="/img/logo.svg", cls="footer-logo"),
                        P("Building the future of AI-assisted development", cls="footer-tagline"),
                        cls="footer-brand"
                    ),
                    Nav(
                        Div(
                            H4("Product"),
                            A("Features", href="/features"),
                            A("Challenges", href="/challenges"),
                            A("Community", href="/community"),
                            A("Blog", href="/blog"),
                            cls="footer-links"
                        ),
                        Div(
                            H4("Company"),
                            A("About", href="/about"),
                            A("Team", href="/team"),
                            A("Careers", href="/careers"),
                            A("Contact", href="/contact"),
                            cls="footer-links"
                        ),
                        Div(
                            H4("Resources"),
                            A("Documentation", href="/docs"),
                            A("API", href="/api"),
                            A("Privacy", href="/privacy"),
                            A("Terms", href="/terms"),
                            cls="footer-links"
                        ),
                        cls="footer-nav"
                    ),
                    cls="footer-top"
                ),
                Div(
                    P(" 2025 ParadiseLabs - All Rights Reserved. Built with AI assistance"),
                    Div(
                        A("Twitter", href="https://twitter.com/paradiselabs_ai", cls="social-link"),
                        A("GitHub", href="https://github.com/paradiselabs-ai", cls="social-link"),
                        A("Discord", href="https://discord.gg/paradiselabs-ai", cls="social-link"),
                        cls="social-links"
                    ),
                    cls="footer-bottom"
                ),
                cls="main-footer"
            ),
        )
    )
