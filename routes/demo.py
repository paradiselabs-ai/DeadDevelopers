from fasthtml.common import *
from app import app, rt

@rt('/demo')
def get():
    return Titled(
        "See How It Works",
        Container(
            Section(
                H1("Experience AI-First Development"),
                P("Watch how AI transforms the way you code.", cls="demo-intro"),
                cls="demo-header"
            ),
            
            # Interactive Demo Section
            Section(
                H2("Live Demo", cls="section-title"),
                Card(
                    H3("AI Pair Programming"),
                    P("Type a description of what you want to build, and watch AI generate the code in real-time."),
                    Form(
                        Textarea(
                            placeholder="Example: Create a responsive navigation menu with a hamburger button for mobile",
                            rows=4,
                            cls="demo-input",
                            name="prompt"
                        ),
                        Button(
                            "Generate Code",
                            type="submit",
                            cls="demo-submit"
                        ),
                        hx_post="/demo/generate",
                        hx_target="#code-output"
                    ),
                    Div(
                        id="code-output",
                        cls="code-display"
                    ),
                    cls="demo-card"
                ),
                cls="interactive-demo"
            ),

            # How It Works Section
            Section(
                H2("How It Works", cls="section-title"),
                Grid(
                    Card(
                        H3("1. Describe Your Need"),
                        P("Use natural language to describe what you want to build - no need for technical jargon."),
                        cls="step-card"
                    ),
                    Card(
                        H3("2. AI Generates Code"),
                        P("Our AI understands your intent and generates production-ready code in seconds."),
                        cls="step-card"
                    ),
                    Card(
                        H3("3. Review & Refine"),
                        P("Review the generated code, make adjustments, and let AI handle the implementation."),
                        cls="step-card"
                    ),
                    cls="steps-grid"
                ),
                cls="how-it-works"
            ),

            # Call to Action
            Section(
                Card(
                    H2("Ready to Try It Yourself?"),
                    P("Join DeadDevelopers and start building with AI today."),
                    Button(
                        "Start Building",
                        cls="cta-primary large",
                        hx_get="/signup"
                    ),
                    cls="demo-cta-card"
                ),
                cls="demo-cta"
            )
        )
    )

@rt('/demo/generate')
def post(prompt: str, session):
    # TODO: Implement actual AI code generation
    # For now, return a sample response
    sample_code = """
    <!-- Generated Navigation Menu -->
    <nav class="nav-container">
        <div class="logo">Brand</div>
        <button class="hamburger" onclick="toggleMenu()">
            <span></span><span></span><span></span>
        </button>
        <ul class="nav-links">
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </nav>

    <style>
    .nav-container {
        display: flex;
        justify-content: space-between;
        padding: 1rem;
        background: #fff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .nav-links {
        display: flex;
        gap: 2rem;
        list-style: none;
    }

    .hamburger {
        display: none;
    }

    @media (max-width: 768px) {
        .nav-links {
            display: none;
        }
        
        .hamburger {
            display: block;
        }

        .nav-links.active {
            display: flex;
            flex-direction: column;
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: #fff;
        }
    }
    </style>

    <script>
    function toggleMenu() {
        document.querySelector('.nav-links').classList.toggle('active');
    }
    </script>
    """
    
    add_toast(session, "Code generated! Try customizing it to match your needs.", "success")
    
    return Card(
        H3("Generated Code"),
        Pre(Code(sample_code, cls="language-html")),
        Button(
            "Copy Code",
            cls="copy-btn",
            hx_post="/demo/copy",
            hx_swap="none"
        ),
        cls="code-card"
    )

@rt('/demo/copy')
def post(session):
    add_toast(session, "Code copied to clipboard!", "info")
    return ""
