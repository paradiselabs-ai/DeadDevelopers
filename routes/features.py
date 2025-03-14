from fasthtml.common import *
from app import rt

@rt('/features')
def get():
    """Features page showing platform capabilities"""
    return Titled(
        "Platform Features",
        Div(
            # Add link to features-specific CSS
            Link(rel='stylesheet', href='/css/features.css'),
            
            # Header/Navigation - Using the same structure as main.py
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
                    cls="main-nav",
                    script="""
                    // Handle scroll effect
                    window.addEventListener('scroll', () => {
                        const header = document.querySelector('.site-header');
                        if (window.scrollY > 10) {
                            header.classList.add('scrolled');
                        } else {
                            header.classList.remove('scrolled');
                        }
                    });

                    // Handle mobile menu
                    const menuButton = document.querySelector('.menu-button');
                    const navCenter = document.querySelector('.nav-center');
                    const navRight = document.querySelector('.nav-right');

                    // Create backdrop
                    const backdrop = document.createElement('div');
                    backdrop.style.cssText = `
                        position: fixed;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background: rgba(0, 0, 0, 0.5);
                        backdrop-filter: blur(4px);
                        opacity: 0;
                        visibility: hidden;
                        transition: all 0.3s ease;
                        z-index: 999;
                    `;
                    document.body.appendChild(backdrop);

                    // Toggle menu
                    menuButton.addEventListener('click', (e) => {
                        e.stopPropagation();
                        const isActive = navCenter.classList.contains('active');
                        navCenter.classList.toggle('active');
                        navRight.classList.toggle('active');
                        backdrop.style.opacity = isActive ? '0' : '1';
                        backdrop.style.visibility = isActive ? 'hidden' : 'visible';
                    });

                    // Close menu when clicking outside
                    backdrop.addEventListener('click', () => {
                        navCenter.classList.remove('active');
                        navRight.classList.remove('active');
                        backdrop.style.opacity = '0';
                        backdrop.style.visibility = 'hidden';
                    });

                    // Close menu when clicking nav links
                    document.querySelectorAll('.nav-center a, .nav-right a').forEach(link => {
                        link.addEventListener('click', () => {
                            navCenter.classList.remove('active');
                            navRight.classList.remove('active');
                            backdrop.style.opacity = '0';
                            backdrop.style.visibility = 'hidden';
                        });
                    });
                    """
                ),
                cls="site-header"
            ),
            
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
                    P("© 2025 ParadiseLabs - All Rights Reserved. Built with AI assistance"),
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
