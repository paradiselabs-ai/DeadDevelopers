from fasthtml.common import *
from app import rt
from starlette.responses import RedirectResponse

@rt('/about')
def get(req):
    """About page for DeadDevelopers platform"""
    
    # Define technologies data
    technologies = [
        {
            "name": "FastHTML",
            "description": "Lightning-fast rendering engine for the next generation of web applications."
        },
        {
            "name": "Django",
            "description": "Robust backend framework powering our supernatural development processes"
        },
        {
            "name": "Vercel",
            "description": "Deployment platform that brings our spectral creations to life"
        }
    ]
    
    # Create technology cards with animation delay
    tech_cards = []
    for i, tech in enumerate(technologies):
        tech_cards.append(
            Div(
                Div(
                    Span(cls="tech-indicator"),
                    H2(tech["name"], cls="technology-name"),
                    cls="technology-header"
                ),
                P(tech["description"], cls="technology-description"),
                cls="technology-card",
                style=f"animation-delay: {i * 200}ms;"
            )
        )
    
    return Titled(
        "",
        Div(
            # Updated Style
            Style("""
                /* Base styles and variables */
                :root {
                  --color-background: #1A1B1A;
                  --color-card: #2a2a2a;
                  --color-accent: #00ff66;
                  --color-text: #ffffff;
                  --color-text-secondary: #cccccc;
                  --font-main: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                  --spacing-unit: clamp(1rem, 2vw, 1.5rem);
                  --content-width: min(90%, 1200px);
                }
                
                /* Reset */
                * {
                  margin: 0;
                  padding: 0;
                  box-sizing: border-box;
                }
                
                /* Base styles */
                body {
                  background-color: var(--color-background);
                  color: var(--color-text);
                  font-family: var(--font-main);
                  line-height: 1.6;
                  -webkit-font-smoothing: antialiased;
                  -moz-osx-font-smoothing: grayscale;
                  overflow-x: hidden;
                }
                
                /* Container */
                .landing-container {
                  min-height: 100vh;
                  padding: calc(var(--spacing-unit) * 2);
                  position: relative;
                  overflow-x: hidden;
                }
                
                /* Animated content */
                .animated-content {
                  opacity: 0;
                  transform: translateY(20px);
                  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
                }
                
                .animated-content.visible {
                  opacity: 1;
                  transform: translateY(0);
                }
                
                /* Main content */
                .main-content {
                  width: var(--content-width);
                  margin: 0 auto;
                  display: flex;
                  flex-direction: column;
                  gap: calc(var(--spacing-unit) * 4);
                  margin-top: 3rem;
                  position: relative;
                  z-index: 1;
                }
                
                /* Background overlay for hero-text to cta-button */
                .main-content::before {
                  content: "";
                  position: absolute;
                  top: calc(var(--spacing-unit) * 12);
                  left: calc(-1 * var(--spacing-unit) * 2);
                  right: calc(-1 * var(--spacing-unit) * 2);
                  bottom: calc(var(--spacing-unit) * -3);
                  background-size: 200% 200%;
                  animation: gradientShift 10s ease-in-out infinite;
                  backdrop-filter: blur(4px);
                  border: 1px solid rgba(255, 255, 255, 0.08);
                  border-radius: 12px;
                  box-shadow: 
                    0 8px 20px rgba(0, 0, 0, 0.3),
                    0 0 20px rgba(0, 255, 102, 0.1);
                  z-index: -2;
                }
                
                /* Hero section */
                .hero-section {
                  text-align: left;
                  margin-top: calc(var(--spacing-unit) * 2);
                }
                
                .main-title {
                  font-size: clamp(2rem, 5vw, 3.5rem);
                  font-weight: 700;
                  line-height: 1.2;
                  margin-bottom: 2rem;
                  position: relative;
                  display: inline-block;
                }
                
                .title-underline {
                  position: absolute;
                  bottom: -10px;
                  left: 0;
                  width: 60px;
                  height: 4px;
                  background-color: var(--color-accent);
                  transform: scaleX(0);
                  transform-origin: left;
                  animation: underlineExpand 0.8s ease-out 0.5s forwards;
                }
                
                .hero-text {
                  font-size: clamp(1rem, 2vw, 1.25rem);
                  color: var(--color-text-secondary);
                  max-width: 800px;
                  margin-top: 8rem;
                  margin-bottom: -4rem;
                  position: relative;
                  z-index: 1;
                }
                
                /* Technologies section */
                .technologies-grid {
                  display: grid;
                  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                  gap: var(--spacing-unit);
                  position: relative;
                  z-index: 1;
                }
                
                .technology-card {
                  padding: calc(var(--spacing-unit) * 1.5);
                  background-color: var(--color-card);
                  border-radius: 8px;
                  opacity: 0;
                  transform: translateY(20px);
                  animation: fadeInUp 0.6s ease-out forwards;
                }
                
                .technology-header {
                  display: flex;
                  align-items: center;
                  gap: calc(var(--spacing-unit) * 0.75);
                  margin-bottom: var(--spacing-unit);
                }
                
                .tech-indicator {
                  width: 8px;
                  height: 8px;
                  background-color: var(--color-accent);
                  border-radius: 50%;
                  display: inline-block;
                  position: relative;
                }
                
                .tech-indicator::after {
                  content: "";
                  position: absolute;
                  width: 16px;
                  height: 16px;
                  background-color: var(--color-accent);
                  border-radius: 50%;
                  top: 50%;
                  left: 50%;
                  transform: translate(-50%, -50%);
                  opacity: 0.2;
                  animation: pulse 2s ease-out infinite;
                }
                
                .technology-name {
                  font-size: clamp(1.25rem, 3vw, 1.5rem);
                  font-weight: 600;
                }
                
                .technology-description {
                  color: var(--color-text-secondary);
                  font-size: clamp(0.875rem, 2vw, 1rem);
                }
                
                /* CTA section */
                .cta-section {
                  text-align: center;
                  margin: calc(var(--spacing-unit) * 3) 0;
                  margin-top: -5rem;
                  position: relative;
                  z-index: 1;
                }
                
                .cta-button {
                  background-color: transparent;
                  color: var(--color-accent);
                  border: 2px solid var(--color-accent);
                  padding: calc(var(--spacing-unit) * 0.75) calc(var(--spacing-unit) * 1.5);
                  font-size: clamp(1rem, 2vw, 1.125rem);
                  font-weight: 500;
                  border-radius: 4px;
                  cursor: pointer;
                  transition: all 0.3s ease;
                  position: relative;
                  overflow: hidden;
                }
                
                .cta-button::before {
                  content: "";
                  position: absolute;
                  top: 50%;
                  left: 50%;
                  width: 0;
                  height: 0;
                  background-color: var(--color-accent);
                  transform: translate(-50%, -50%);
                  border-radius: 50%;
                  transition: width 0.6s ease, height 0.6s ease;
                  z-index: -1;
                }
                
                .cta-button:hover {
                  color: var(--color-background);
                }
                
                .cta-button:hover::before {
                  width: 300%;
                  height: 300%;
                }
                
                /* Footer */
                .main-footer {
                  position: relative;
                  z-index: 0;
                }
                
                /* Animations */
                @keyframes underlineExpand {
                  from { transform: scaleX(0); }
                  to { transform: scaleX(1); }
                }
                
                @keyframes fadeInUp {
                  from { opacity: 0; transform: translateY(20px); }
                  to { opacity: 1; transform: translateY(0); }
                }
                
                @keyframes pulse {
                  0% { transform: translate(-50%, -50%) scale(1); opacity: 0.2; }
                  50% { transform: translate(-50%, -50%) scale(1.5); opacity: 0.1; }
                  100% { transform: translate(-50%, -50%) scale(1); opacity: 0.2; }
                }
                
                @keyframes gradientShift {
                  0% { background-position: 0% 0%; }
                  50% { background-position: 100% 100%; }
                  100% { background-position: 0% 0%; }
                }
                
                /* Responsive Design */
                @media (max-width: 768px) {
                  .landing-container { padding: var(--spacing-unit); }
                  .hero-section { margin-top: calc(var(--spacing-unit) * 2); }
                  .technologies-grid { grid-template-columns: 1fr; }
                  .main-content::before, .main-content::after { 
                    top: calc(var(--spacing-unit) * 16); 
                    left: calc(-1 * var(--spacing-unit));
                    right: calc(-1 * var(--spacing-unit));
                  }
                  .cta-section {
                  text-align: center;
                  margin: calc(var(--spacing-unit) * 3) 0;
                  margin-top: -3rem;
                  position: relative;
                  z-index: 1;
                }

                }
                
                /* Accessibility */
                @media (prefers-reduced-motion: reduce) {
                  .animated-content, .technology-card, .title-underline, 
                  .tech-indicator::after, .cta-button::before, .main-content::before {
                    animation: none;
                    transition: none;
                  }
                  .main-content::before { backdrop-filter: none; }
                }
                
                /* Focus States */
                .cta-button:focus-visible {
                  outline: 2px solid var(--color-accent);
                  outline-offset: 4px;
                }
                
                /* Print styles */
                @media print {
                  .landing-container { background: white; color: black; }
                  .technology-card { border: 1px solid #ccc; break-inside: avoid; }
                  .cta-button { display: none; }
                  .main-content::before, .main-content::after { display: none; }
                }
            """),
            
            Script("""
                document.addEventListener('DOMContentLoaded', function() {
                    setTimeout(function() {
                        document.querySelector('.animated-content').classList.add('visible');
                    }, 100);
                });
            """),
            
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
            
            Div(
                Div(
                    Section(
                        H1(
                            "Welcome to the Post-Human Coding Collective",
                            Span(cls="title-underline"),
                            cls="main-title"
                        ),
                        P(
                            "In the digital afterlife, we are the DeadDevelopers - a collective of code artisans who transcend the "
                            "traditional boundaries of software development. We exist in the liminal space between human creativity and "
                            "machine precision, pushing the boundaries of what's possible in the digital realm.",
                            cls="hero-text"
                        ),
                        cls="hero-section"
                    ),
                    Section(
                        Div(
                            *tech_cards,
                            cls="technologies-grid"
                        ),
                        cls="technologies-section"
                    ),
                    Section(
                        Button(
                            "Join Us in the Digital Afterlife",
                            cls="cta-button",
                            onclick="window.location.href = '/signup'"
                        ),
                        cls="cta-section"
                    ),
                    cls="main-content"
                ),
                cls="animated-content"
            ),
            
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
            
            cls="landing-container"
        )
    )