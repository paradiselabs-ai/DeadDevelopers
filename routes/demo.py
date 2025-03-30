from fasthtml.common import *
from app import app, rt, add_toast
from routes.header import SiteHeader

@rt('/demo')
def get(session):
    # Store current path in session for active link highlighting
    session['path'] = '/demo'

    return Titled(
        "See How It Works",
        # Header/Navigation
        SiteHeader(session),

        Main(
            Section(
                H1("Experience AI-First Development"),
                P("Watch how AI transforms the way you code.", cls="demo-intro"),
                cls="demo-header"
            ),

            # Interactive Demo Section
            Section(
                Container(
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
                ),
                cls="interactive-demo"
            ),

            # How It Works Section
            Section(
                Container(
                    H2("How It Works", cls="section-title"),
                    Div(
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
                ),
                cls="how-it-works"
            ),

            # Call to Action
            Section(
                Container(
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
                ),
                cls="demo-cta"
            )
        )
    )

@rt('/demo/generate')
def post(prompt: str, session):
    # TODO: Implement actual AI code generation
    # For now, return a sample response
    sample_code = """<!-- Generated Navigation Menu -->
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
    background: #1a1a1a;
    color: #fff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    font-family: 'JetBrains Mono', monospace;
}

.logo {
    font-weight: bold;
    font-size: 1.2rem;
    color: #00ff66;
}

.nav-links {
    display: flex;
    gap: 2rem;
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav-links a {
    color: #fff;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: #00ff66;
}

.hamburger {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
}

.hamburger span {
    display: block;
    width: 25px;
    height: 3px;
    background: #00ff66;
    margin: 5px 0;
    transition: all 0.3s;
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
        background: #1a1a1a;
        padding: 1rem;
        z-index: 100;
        border-top: 1px solid #00ff66;
    }

    .hamburger.active span:nth-child(1) {
        transform: rotate(45deg) translate(5px, 5px);
    }

    .hamburger.active span:nth-child(2) {
        opacity: 0;
    }

    .hamburger.active span:nth-child(3) {
        transform: rotate(-45deg) translate(7px, -7px);
    }
}
</style>

<script>
function toggleMenu() {
    document.querySelector('.nav-links').classList.toggle('active');
    document.querySelector('.hamburger').classList.toggle('active');
}
</script>"""

    add_toast(session, "Code generated! Try customizing it to match your needs.", "success")

    return Card(
        H3("Generated Code"),
        Pre(
            Code(sample_code, cls="language-html"),
            cls="code-block"
        ),
        Button(
            "Copy Code",
            cls="copy-btn",
            hx_post="/demo/copy",
            hx_swap="none"
        ),
        Script("if (typeof Prism !== 'undefined') { Prism.highlightAll(); }"),
        cls="code-card"
    )

@rt('/demo/copy')
def post(session):
    add_toast(session, "Code copied to clipboard!", "info")
    return Script("""
        // Copy code to clipboard
        const code = document.querySelector('.code-block code').textContent;
        navigator.clipboard.writeText(code)
            .then(() => console.log('Code copied to clipboard'))
            .catch(err => console.error('Failed to copy code: ', err));
    """)


