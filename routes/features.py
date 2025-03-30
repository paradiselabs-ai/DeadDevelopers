from fasthtml.common import *
from app import rt
from routes.header import SiteHeader

@rt('/features')
def get(session):
    """Features page showing platform capabilities"""
    # Store current path in session for active link highlighting
    session['path'] = '/features'
    
    return Titled(
        "Platform Features",
        Div(
            # Add link to features-specific CSS
            Link(rel='stylesheet', href='/css/features.css'),
            
            # Header/Navigation
            SiteHeader(session),
            
            # Main content container
            Main(
                Div(
                    # Header with page title
                    H1("Platform Features", cls="page-title"),
                    
                    # Features grid with cards
                    Div(
                        # Real-Time Chat feature
                        Div(
                            Div(
                                Span("💬", cls="feature-icon"),
                            ),
                            H2("Real-Time Chat", cls="feature-title"),
                            P("Connect instantly with fellow developers through our advanced real-time messaging system."),
                            Div(
                                A("Learn More", href="/features/chat", cls="learn-more-btn"),
                            ),
                            cls="feature-card"
                        ),
                        
                        # Forums & Discussion feature
                        Div(
                            Div(
                                Span("👥", cls="feature-icon"),
                            ),
                            H2("Forums & Discussion", cls="feature-title"),
                            P("Engage in meaningful discussions with the developer community in our organized forums."),
                            Div(
                                A("Learn More", href="/features/forums", cls="learn-more-btn"),
                            ),
                            cls="feature-card"
                        ),
                        
                        # Developer Blogs feature
                        Div(
                            Div(
                                Span("📝", cls="feature-icon"),
                            ),
                            H2("Developer Blogs", cls="feature-title"),
                            P("Share your knowledge and experiences through our integrated blogging platform."),
                            Div(
                                A("Learn More", href="/features/blogs", cls="learn-more-btn"),
                            ),
                            cls="feature-card"
                        ),
                        
                        # Code Challenges feature
                        Div(
                            Div(
                                Span("</>", cls="feature-icon"),
                            ),
                            H2("Code Challenges", cls="feature-title"),
                            P("Test your skills with our upcoming coding challenges and competitions."),
                            Div(
                                A("Learn More", href="/features/challenges", cls="learn-more-btn"),
                            ),
                            cls="feature-card"
                        ),
                        
                        cls="features-grid"
                    ),
                    
                    # Call to action section
                    Section(
                        H2("Ready to Join the Dead Developers?", cls="cta-title"),
                        P("Join our community of developers and start exploring all these features today."),
                        Div(
                            A("Get Started", href="/signup", cls="cta-button"),
                        ),
                        cls="cta-section"
                    ),
                    
                    cls="content-container"
                )
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
            
            cls="features-wrapper"
        )
    )
