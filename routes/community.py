from fasthtml.common import *
from app import rt
from routes.header import SiteHeader
from fasthtml.svg import Svg, ft_svg as tag

@rt('/community')
def get(session):
    """Community page for DeadDevelopers platform"""
    # Store current path in session for active link highlighting
    session['path'] = '/community'
    
    return Titled(
        "Join the DeadDevelopers Community",
        Div(
            # Add community-specific CSS
            Style("""
                /* Base styles */
                :root {
                  --color-background: #1a1a1a;
                  --color-card-background: #1a1a1a;
                  --color-accent: #00ff66;
                  --color-text: #ffffff;
                  --color-text-secondary: #cccccc;
                  --transition-speed: 0.3s;
                  --container-padding: 1rem;
                  --card-gap: 1.5rem;
                }

                /* Hero Section */
                .hero {
                  text-align: center;
                  margin-bottom: 3rem;
                  padding: 6rem 0 1rem 0;
                  background: none;
                }

                .hero-title {
                  font-size: clamp(1.5rem, 4vw, 2rem);
                  font-weight: bold;
                  margin-bottom: 1rem;
                  line-height: 1.2;
                  background: none;
                }

                .hero-subtitle {
                  font-size: clamp(0.875rem, 3vw, 1.125rem);
                  color: var(--color-text-secondary);
                  max-width: 600px;
                  margin: 0 auto;
                  padding: 0 1rem;
                  margin-bottom: 0rem;
                  background: none;
                }

                .highlight {
                  color: var(--color-accent);
                  transition: text-shadow var(--transition-speed);
                }

                .highlight:hover {
                  text-shadow: 0 0 8px rgba(0, 255, 102, 0.5);
                }

                /* Feature Cards */
                .cards-container {
                  display: grid;
                  grid-template-columns: 1fr;
                  gap: var(--card-gap);
                  margin-bottom: 3rem;
                  width: 100%;
                }

                .card {
                  border: 1px solid var(--color-accent);
                  border-radius: 0.5rem;
                  padding: 1.25rem;
                  background-color: var(--color-card-background);
                  transition: transform var(--transition-speed), box-shadow var(--transition-speed);
                  cursor: pointer;
                  width: 100%;
                }

                .card-active {
                  transform: translateY(-5px);
                  box-shadow: 0 10px 20px rgba(0, 255, 102, 0.1);
                }

                .card-icon {
                  width: 3rem;
                  height: 3rem;
                  background-color: rgba(0, 255, 102, 0.2);
                  border-radius: 0.375rem;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  margin-bottom: 1rem;
                  transition: background-color var(--transition-speed);
                }

                .card-active .card-icon {
                  background-color: rgba(0, 255, 102, 0.3);
                }

                .icon {
                  width: 1.5rem;
                  height: 1.5rem;
                  color: var(--color-accent);
                }

                .card-title {
                  font-size: 1.25rem;
                  font-weight: bold;
                  margin-bottom: 0.5rem;
                }

                .card-description {
                  color: var(--color-text-secondary);
                  margin-bottom: 1.5rem;
                  font-size: clamp(0.875rem, 2vw, 1rem);
                }

                .card-link {
                  color: var(--color-accent);
                  text-decoration: none;
                  position: relative;
                  transition: color var(--transition-speed);
                  font-size: clamp(0.875rem, 2vw, 1rem);
                  display: inline-block;
                  padding: 0.25rem 0;
                }

                .card-link::after {
                  content: "";
                  position: absolute;
                  width: 0;
                  height: 2px;
                  bottom: -2px;
                  left: 0;
                  background-color: var(--color-accent);
                  transition: width var(--transition-speed);
                }

                .card-link:hover::after,
                .card-active .card-link::after {
                  width: 100%;
                }

                /* Member Spotlight */
                .member-section {
                  text-align: center;
                  margin-bottom: 3rem;
                  padding: clamp(1rem, 5vw, 2rem);
                  background-color: var(--color-card-background);
                  border-radius: 0.5rem;
                  width: 100%;
                }

                .section-title {
                  font-size: clamp(1.25rem, 4vw, 1.5rem);
                  font-weight: bold;
                  margin-bottom: clamp(1.5rem, 5vw, 2rem);
                }

                .members-grid {
                  display: grid;
                  grid-template-columns: 1fr;
                  gap: 2rem;
                  width: 100%;
                }

                .member-card {
                  display: flex;
                  flex-direction: column;
                  align-items: center;
                  transition: transform var(--transition-speed);
                  cursor: pointer;
                  padding: 0.5rem;
                }

                .member-active {
                  transform: translateY(-5px);
                }

                .member-image {
                  width: clamp(60px, 15vw, 80px);
                  height: clamp(60px, 15vw, 80px);
                  border-radius: 50%;
                  border: 2px solid var(--color-accent);
                  overflow: hidden;
                  margin-bottom: 1rem;
                  transition: box-shadow var(--transition-speed);
                }

                .member-active .member-image {
                  box-shadow: 0 0 15px rgba(0, 255, 102, 0.5);
                }

                .placeholder-image {
                  width: 100%;
                  height: 100%;
                  background-color: rgba(0, 255, 102, 0.2);
                }

                .member-name {
                  color: var(--color-accent);
                  font-size: clamp(1rem, 3vw, 1.125rem);
                  margin: 0 0 0.5rem 0;
                }

                .member-contributions {
                  color: var(--color-text-secondary);
                  font-size: clamp(0.75rem, 2vw, 0.875rem);
                  margin: 0;
                }

                /* Call to Action */
                .cta-section {
                  text-align: center;
                  margin-bottom: 2rem;
                  padding: 1rem 0;
                  width: 100%;
                }

                .cta-button {
                  display: inline-block;
                  margin-left: 1.5rem;
                  background-color: transparent;
                  color: var(--color-accent);
                  border: 1px solid var(--color-accent);
                  padding: clamp(0.5rem, 3vw, 0.75rem) clamp(1.5rem, 5vw, 2rem);
                  border-radius: 0.25rem;
                  font-size: clamp(0.875rem, 3vw, 1rem);
                  cursor: pointer;
                  transition: background-color var(--transition-speed), color var(--transition-speed), transform var(--transition-speed),
                    box-shadow var(--transition-speed);
                  -webkit-tap-highlight-color: transparent;
                }

                .cta-button:hover,
                .cta-button:focus {
                  background-color: var(--color-accent);
                  color: var(--color-background);
                  transform: translateY(-2px);
                  box-shadow: 0 5px 15px rgba(0, 255, 102, 0.3);
                  outline: none;
                }

                .cta-button:active {
                  transform: translateY(0);
                  box-shadow: 0 2px 5px rgba(0, 255, 102, 0.3);
                }

                /* Responsive Design */
                @media (min-width: 480px) {
                  :root {
                    --container-padding: 1.5rem;
                  }

                  .card {
                    padding: 1.5rem;
                  }
                }

                @media (min-width: 768px) {
                  :root {
                    --container-padding: 2rem;
                    --card-gap: 2rem;
                  }

                  .cards-container {
                    grid-template-columns: repeat(2, 1fr);
                  }

                  .members-grid {
                    grid-template-columns: repeat(3, 1fr);
                  }

                  .hero {
                    margin-bottom: 4rem;
                  }

                  .member-section {
                    margin-bottom: 4rem;
                  }
                }

                @media (min-width: 1024px) {
                  .container {
                    padding: 3rem 2rem;
                  }

                  .card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 10px 20px rgba(0, 255, 102, 0.1);
                  }

                  .card:hover .card-icon {
                    background-color: rgba(0, 255, 102, 0.3);
                  }

                  .member-card:hover {
                    transform: translateY(-5px);
                  }

                  .member-card:hover .member-image {
                    box-shadow: 0 0 15px rgba(0, 255, 102, 0.5);
                  }
                }

                /* Accessibility Improvements */
                @media (prefers-reduced-motion: reduce) {
                  * {
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: 0.01ms !important;
                    scroll-behavior: auto !important;
                  }
                }

                /* Touch Device Optimizations */
                @media (hover: none) {
                  .card {
                    transition: none;
                  }

                  .card-active {
                    background-color: rgba(0, 255, 102, 0.05);
                  }

                  .member-card {
                    transition: none;
                  }

                  .cta-button:hover {
                    transform: none;
                    box-shadow: none;
                  }
                }
            """),
            
            # Header/Navigation - Using the same structure as in features.py
            
            SiteHeader(session),
            
            # Main content container
            Main(
                Div(
                    # Hero Section
                    Section(
                        H2("Join the DeadDevelopers Community", cls="hero-title"),
                        P(
                            "Connect, collaborate, and code with ", 
                            Span("fellow developers", cls="highlight"), " in our thriving ",
                            Span("community", cls="highlight"), ".",
                            cls="hero-subtitle"
                        ),
                        cls="hero"
                    ),
                    
                    # Feature Cards Section
                    Section(
                        Div(
                            # Forum Card
                            Div(
                                Div(
                                    Svg(
                                        tag("path", d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z", fill="currentColor"),
                                        viewBox="0 0 24 24", 
                                        cls="icon"
                                    ),
                                    cls="card-icon"
                                ),
                                H2("Forum", cls="card-title"),
                                P("Engage in discussions, share knowledge, and get help from the community.", cls="card-description"),
                                A("Join Discussion →", href="#", cls="card-link"),
                                id="forum-card",
                                cls="card"
                            ),
                                
                            # Live Chat Card
                            Div(
                                Div(
                                    Svg(
                                        tag("path", d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z", fill="currentColor"),
                                        viewBox="0 0 24 24", 
                                        cls="icon"
                                    ),
                                    cls="card-icon"
                                ),
                                H2("Live Chat", cls="card-title"),
                                P("Have live conversations with developers from around the world.", cls="card-description"),
                                A("Start Chatting →", href="#", cls="card-link"),
                                id="chat-card",
                                cls="card"
                            ),
                            cls="cards-container"
                        ),
                        
                        # Member Spotlight Section
                        Section(
                            H2("Member Spotlight", cls="section-title"),
                            Div(
                                # Alex Chen Member Card
                                Div(
                                    Div(
                                        Div(cls="placeholder-image"),
                                        cls="member-image"
                                    ),
                                    H3("Alex Chen", cls="member-name"),
                                    P("500+ Contributions", cls="member-contributions"),
                                    id="member-1",
                                    cls="member-card"
                                ),
                                
                                # Sarah Miller Member Card
                                Div(
                                    Div(
                                        Div(cls="placeholder-image"),
                                        cls="member-image"
                                    ),
                                    H3("Sarah Miller", cls="member-name"),
                                    P("450+ Contributions", cls="member-contributions"),
                                    id="member-2",
                                    cls="member-card"
                                ),
                                
                                # James Wilson Member Card
                                Div(
                                    Div(
                                        Div(cls="placeholder-image"),
                                        cls="member-image"
                                    ),
                                    H3("James Wilson", cls="member-name"),
                                    P("400+ Contributions", cls="member-contributions"),
                                    id="member-3",
                                    cls="member-card"
                                ),
                                cls="members-grid"
                            ),
                            cls="member-section",
                            id="member-section"
                        ),
                        
                        # Call to Action Section
                        Section(
                            H2("Ready to Join?", cls="section-title"),
                            Button("Join Now", cls="cta-button", hx_get="/signup"),
                            cls="cta-section"
                        ),
                        
                        # JavaScript for interactivity
                        Script("""
                            // Detect if the device supports touch events
                            const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
                            
                            // Card interaction
                            const forumCard = document.getElementById('forum-card');
                            const chatCard = document.getElementById('chat-card');
                            
                            // Add event listeners for forum card
                            if (!isTouchDevice) {
                                forumCard.addEventListener('mouseenter', () => {
                                    forumCard.classList.add('card-active');
                                });
                                forumCard.addEventListener('mouseleave', () => {
                                    forumCard.classList.remove('card-active');
                                });
                            } else {
                                forumCard.addEventListener('click', () => {
                                    forumCard.classList.toggle('card-active');
                                    if (chatCard.classList.contains('card-active')) {
                                        chatCard.classList.remove('card-active');
                                    }
                                });
                            }
                            
                            // Add event listeners for chat card
                            if (!isTouchDevice) {
                                chatCard.addEventListener('mouseenter', () => {
                                    chatCard.classList.add('card-active');
                                });
                                chatCard.addEventListener('mouseleave', () => {
                                    chatCard.classList.remove('card-active');
                                });
                            } else {
                                chatCard.addEventListener('click', () => {
                                    chatCard.classList.toggle('card-active');
                                    if (forumCard.classList.contains('card-active')) {
                                        forumCard.classList.remove('card-active');
                                    }
                                });
                            }
                            
                            // Member card interaction
                            const memberCards = document.querySelectorAll('.member-card');
                            
                            memberCards.forEach(card => {
                                if (!isTouchDevice) {
                                    card.addEventListener('mouseenter', () => {
                                        card.classList.add('member-active');
                                    });
                                    card.addEventListener('mouseleave', () => {
                                        card.classList.remove('member-active');
                                    });
                                } else {
                                    card.addEventListener('click', () => {
                                        // Toggle active class on clicked card
                                        card.classList.toggle('member-active');
                                        
                                        // Remove active class from other cards
                                        memberCards.forEach(otherCard => {
                                            if (otherCard !== card && otherCard.classList.contains('member-active')) {
                                                otherCard.classList.remove('member-active');
                                            }
                                        });
                                    });
                                }
                            });
                        """),
                        
                        cls="container"
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
                
                cls="community-wrapper"
            )
        )
    )
