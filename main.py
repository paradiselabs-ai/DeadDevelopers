from fasthtml.common import *
from app import app, rt

# Import routes
from routes.auth import *
from routes.demo import *
from routes.dashboard import *
from routes.features import *
from routes.community import *
from routes.blog import *
from routes.about import *
from routes.header import SiteHeader
from routes.email_confirmation import *
from routes.components import chat_send_message

# We'll import toast setup at the end of the file

# Landing page route
@rt('/')
def get(session):
    # Store current path in session for active link highlighting
    session['path'] = '/'
    
    return Titled(
        "",
        Container(
            # Header/Navigation
            SiteHeader(session),

            # Hero Section
            Section(
                Div(
                    Div(
                        Pre(
                            Code(
                                Div(
                                    Span("// AI Assistant"),
                                    Span("function buildFeature() {"),
                                    Span("  const idea = 'Your vision';"),
                                    Span("  const code = AI.generate(idea);"),
                                    Span("  return deploy(code);"),
                                    Span("}"),
                                    Span(""),
                                    Span("// Result"),
                                    Span("Deployed in 0.3s ✨"),
                                    cls="code-lines"
                                ),
                                cls="editor-content"
                            ),
                            cls="code-window"
                        ),
                        cls="animated-editor"
                    ),
                    H1("Humans (mostly) Not Required"),
                    P("Where AI writes 80% of your code, and you're proud of it.", cls="hero-tagline"),
                    Div(
                        Button("Start Building with AI", cls="cta-primary", hx_get="/signup"),
                        A("See How It Works", href="/demo", cls="cta-secondary"),
                        cls="cta-group"
                    ),
                    cls="hero-content"
                ),
                cls="hero"
            ),
            
            # Live Stats Section
            Section(
                H2("Embrace AI-First Development", cls="section-title"),
                Grid(
                    Card(
                        H3("80%+"),
                        P("Let AI Handle the Heavy Lifting"),
                        cls="stat-card"
                    ),
                    Card(
                        H3("24/7"),
                        P("AI Assistance Available"),
                        cls="stat-card"
                    ),
                    Card(
                        H3("2x+"),
                        P("Boost Your Development Speed"),
                        cls="stat-card"
                    ),
                    cls="stats-grid"
                ),
                cls="live-stats"
            ),

            # Features Section
            Section(
                H2("Build Smarter, Not Harder", cls="section-title"),
                P("Embrace the future of development with AI automation that adapts to your workflow", 
                  cls="section-subtitle"),
                Grid(
                    Card(
                        Div(
                            Span("🤝", cls="feature-icon"),
                            cls="icon-container"
                        ),
                        H3("Real-time AI Pairing"),
                        P("Code alongside GPT-4 with our collaborative editor. Get real-time suggestions, explanations, and solutions as you type."),
                        Div(
                            Button("Try Now", hx_get="/pair-demo", cls="feature-btn"),
                            A("Learn more →", href="/features#pairing", cls="feature-link"),
                            cls="feature-actions"
                        ),
                        cls="feature-card"
                    ),
                    Card(
                        Div(
                            Span("🎯", cls="feature-icon"),
                            cls="icon-container"
                        ),
                        H3("Daily AI Challenges"),
                        P("Sharpen your AI-assisted coding skills with daily challenges designed to push the boundaries of human-AI collaboration."),
                        Div(
                            Button("View Challenges", hx_get="/challenges", cls="feature-btn"),
                            A("Learn more →", href="/features#challenges", cls="feature-link"),
                            cls="feature-actions"
                        ),
                        cls="feature-card"
                    ),
                    Card(
                        Div(
                            Span("💬", cls="feature-icon"),
                            cls="icon-container"
                        ),
                        H3("AI Dev Chat"),
                        P("Connect with fellow developers, share effective prompts, and learn optimal AI workflows in our real-time community."),
                        Div(
                            Button("Join Chat", hx_get="/chat", cls="feature-btn"),
                            A("Learn more →", href="/features#community", cls="feature-link"),
                            cls="feature-actions"
                        ),
                        cls="feature-card"
                    ),
                    cls="features-grid"
                ),
                cls="features"
            ),

            # Live Feeds Section
            Section(
                H2("Community Activity", cls="section-title"),
                P("Real-time updates from our network of AI-powered developers", cls="section-subtitle"),
                Div(
                    Div(
                        Div(
                            H3("// LIVE UPDATES", cls="feed-title"),
                            Div(
                                Ul(
                                    Li(
                                        Span("@sarah", cls="username"),
                                        " completed the daily challenge using AI pair programming",
                                        cls="update-item"
                                    ),
                                    Li(
                                        Span("@maya", cls="username"),
                                        " deployed a new feature in 0.3s with AI assistance",
                                        cls="update-item"
                                    ),
                                    Li(
                                        Span("@chris", cls="username"),
                                        " optimized database queries using AI suggestions",
                                        cls="update-item"
                                    ),
                                    Li(
                                        Span("@taylor", cls="username"),
                                        " created a responsive layout with AI pair programming",
                                        cls="update-item"
                                    ),
                                    Li(
                                        Span("@jordan", cls="username"),
                                        " automated testing with AI-generated test cases",
                                        cls="update-item"
                                    ),
                                    Li(
                                        Span("@quinn", cls="username"),
                                        " improved API documentation using AI",
                                        cls="update-item"
                                    ),
                                    Li(
                                        Span("@riley", cls="username"),
                                        " fixed 3 bugs with AI code analysis",
                                        cls="update-item"
                                    ),
                                    # Duplicate items for smooth scrolling
                                    Li(
                                        Span("@sarah", cls="username"),
                                        " completed the daily challenge using AI pair programming",
                                        cls="update-item"
                                    ),
                                    Li(
                                        Span("@maya", cls="username"),
                                        " deployed a new feature in 0.3s with AI assistance",
                                        cls="update-item"
                                    ),
                                    Li(
                                        Span("@chris", cls="username"),
                                        " optimized database queries using AI suggestions",
                                        cls="update-item"
                                    ),
                                    Li(
                                        Span("@taylor", cls="username"),
                                        " created a responsive layout with AI pair programming",
                                        cls="update-item"
                                    ),
                                    Li(
                                        Span("@jordan", cls="username"),
                                        " automated testing with AI-generated test cases",
                                        cls="update-item"
                                    ),
                                    Li(
                                        Span("@quinn", cls="username"),
                                        " improved API documentation using AI",
                                        cls="update-item"
                                    ),
                                    Li(
                                        Span("@riley", cls="username"),
                                        " fixed 3 bugs with AI code analysis",
                                        cls="update-item"
                                    ),
                                    cls="updates-list"
                                ),
                                cls="feed-scroll"
                            ),
                            cls="feed-column"
                        ),
                        
                        # Live Feed Column
                        Div(
                            Div(
                                H3("// LIVE FEED", cls="feed-title"),
                                Div(
                                    Ul(
                                        Li(
                                            Span("📢 ANNOUNCEMENT", cls="announcement"),
                                            " AI Code Challenge Week starts Monday! Get ready to compete! 🏆",
                                            cls="feed-item announcement-item"
                                        ),
                                        Li(
                                            Span("@sophia", cls="username"),
                                            " published: 'Building Scalable Systems with AI'",
                                            cls="feed-item"
                                        ),
                                        Li(
                                            Span("@marcus", cls="username"),
                                            " posted: 'From Junior to Senior with AI in 6 Months'",
                                            cls="feed-item"
                                        ),
                                        Li(
                                            Span("@elena", cls="username"),
                                            " wrote: 'The Ultimate Guide to AI Prompt Engineering'",
                                            cls="feed-item"
                                        ),
                                        Li(
                                            Span("📢 ANNOUNCEMENT", cls="announcement"),
                                            " New AI Pairing Features Released! 🚀",
                                            cls="feed-item announcement-item"
                                        ),
                                        Li(
                                            Span("@kai", cls="username"),
                                            " published: 'AI-First Architecture Patterns That Scale'",
                                            cls="feed-item"
                                        ),
                                        Li(
                                            Span("@zara", cls="username"),
                                            " shared: 'My Journey to 90% AI Development'",
                                            cls="feed-item"
                                        ),
                                        Li(
                                            Span("📢 ANNOUNCEMENT", cls="announcement"),
                                            " Community Milestone - 10k Members! 🎉",
                                            cls="feed-item announcement-item"
                                        ),
                                        Li(
                                            Span("@lucas", cls="username"),
                                            " wrote: 'Revolutionizing Code Reviews with AI'",
                                            cls="feed-item"
                                        ),
                                        # Duplicate items for smooth scrolling
                                        Li(
                                            Span("📢 ANNOUNCEMENT", cls="announcement"),
                                            " AI Code Challenge Week starts Monday! Get ready to compete! 🏆",
                                            cls="feed-item announcement-item"
                                        ),
                                        Li(
                                            Span("@sophia", cls="username"),
                                            " published: 'Building Scalable Systems with AI'",
                                            cls="feed-item"
                                        ),
                                        Li(
                                            Span("@marcus", cls="username"),
                                            " posted: 'From Junior to Senior with AI in 6 Months'",
                                            cls="feed-item"
                                        ),
                                        Li(
                                            Span("@elena", cls="username"),
                                            " wrote: 'The Ultimate Guide to AI Prompt Engineering'",
                                            cls="feed-item"
                                        ),
                                        Li(
                                            Span("📢 ANNOUNCEMENT", cls="announcement"),
                                            " New AI Pairing Features Released! 🚀",
                                            cls="feed-item announcement-item"
                                        ),
                                        Li(
                                            Span("@kai", cls="username"),
                                            " published: 'AI-First Architecture Patterns That Scale'",
                                            cls="feed-item"
                                        ),
                                        Li(
                                            Span("@zara", cls="username"),
                                            " shared: 'My Journey to 90% AI Development'",
                                            cls="feed-item"
                                        ),
                                        Li(
                                            Span("📢 ANNOUNCEMENT", cls="announcement"),
                                            " Community Milestone - 10k Members! 🎉",
                                            cls="feed-item announcement-item"
                                        ),
                                        Li(
                                            Span("@lucas", cls="username"),
                                            " wrote: 'Revolutionizing Code Reviews with AI'",
                                            cls="feed-item"
                                        ),
                                        cls="feed-list"
                                    ),
                                    cls="feed-scroll"
                                ),
                                cls="feed-content"
                            ),
                            cls="feed-column"
                        ),
                        cls="feeds-grid"
                    ),
                    cls="feeds-container"
                ),
                cls="community-section"
            ),

            # Call to Action
            Section(
                Div(
                    Div(
                        H2("Ready to Level Up Your Development?"),
                        P("Join a community of developers embracing AI-first workflows and build the future faster."),
                        cls="cta-text"
                    ),
                    Div(
                        Button("Get Started", cls="cta-primary large", hx_get="/signup"),
                        P("No credit card required • Free community access", cls="cta-disclaimer"),
                        cls="cta-buttons"
                    ),
                    cls="cta-grid"
                ),
                Div(
                    Pre(
                        Code("$ ai init deadDeveloper\n> AI assistant initialized\n> Creating your developer profile...\n> Welcome to the future of development ✨"),
                        cls="cta-terminal"
                    ),
                    cls="terminal-container"
                ),
                cls="bottom-cta"
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
            )
        )
    )

# No need for toast setup - we'll use the direct approach

# Run the server
serve()
