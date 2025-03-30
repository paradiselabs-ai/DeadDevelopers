# Development Notes

## Hero Section Implementation (LOCKED - DO NOT MODIFY)

The hero section has been perfected with the following key elements:

### Animated Code Editor
- Terminal-style window with green border accents
- Line numbers and syntax highlighting
- Animated typing effect for code appearance
- Blinking cursor effect
- Perfect timing on line-by-line reveal

### Typography & Layout
- "HUMANS (MOSTLY) NOT REQUIRED" in bold, impactful typography
- Monospace tagline: "Where AI writes 80% of your code, and you're proud of it."
- Clean button layout with "START BUILDING WITH AI" and "SEE HOW IT WORKS"

### Visual Effects
- Subtle grid background with opacity 0.1
- Gradient overlays for depth
- Terminal-style code window with perfect padding and spacing
- Syntax highlighting colors:
  - Comments: #6a9955 (green)
  - Function declarations: #dcdcaa (yellow)
  - Strings: #ce9178 (orange)
  - Keywords: #569cd6 (blue)
  - Function calls: #4ec9b0 (teal)

### Critical CSS Components
```css
/* These styles are locked and should not be modified */
.animated-editor {
    width: 600px;
    max-width: 90%;
    margin: 0 auto 3rem;
    position: relative;
}

.code-window {
    background: var(--terminal);
    border-radius: 2px;
    padding: 2.5rem 1.5rem 1.5rem;
    /* Box shadow creates the perfect terminal border effect */
    box-shadow: 
        0 2px 0 var(--primary),
        0 -2px 0 var(--primary),
        2px 0 0 var(--primary),
        -2px 0 0 var(--primary);
    border: none;
}

.code-lines > span {
    /* Animation timing is crucial for readability */
    animation: fadeInLine 0.1s ease-out forwards;
}

/* Animation delays create the perfect typing effect */
.code-lines > span:nth-child(1) { animation-delay: 0.1s; }
.code-lines > span:nth-child(2) { animation-delay: 0.3s; }
.code-lines > span:nth-child(3) { animation-delay: 0.5s; }
.code-lines > span:nth-child(4) { animation-delay: 0.7s; }
.code-lines > span:nth-child(5) { animation-delay: 0.9s; }
.code-lines > span:nth-child(6) { animation-delay: 1.1s; }
.code-lines > span:nth-child(7) { animation-delay: 1.3s; }
.code-lines > span:nth-child(8) { animation-delay: 1.5s; }
.code-lines > span:nth-child(9) { animation-delay: 1.7s; }
```

### ⚠️ IMPORTANT NOTES
1. The hero section's implementation is now LOCKED. Any proposed changes must go through thorough review.
2. The animated code effect is perfectly timed - do not modify the animation delays.
3. The color scheme and syntax highlighting create the perfect terminal feel.
4. The layout spacing and proportions are optimized for both desktop and mobile.

### Future Considerations
- The hero section should remain untouched
- Only bug fixes or critical performance improvements should be considered
- Any proposed changes must maintain the exact same visual and animated effects
- The timing of the code animation is crucial for readability and impact

## Navigation Implementation
- Logo and brand text properly styled
- Hover effects with voltage glow
- Mobile menu with backdrop blur
- Smooth transitions for all interactions

## Authentication System Implementation

The authentication system has been implemented with the following key elements:

### Terminal-Themed Login/Signup Forms
- Terminal-style cards with dot indicators in header
- Acid green and voltage blue accent colors
- Custom error handling with terminal error formatting
- Smooth transitions and hover effects
- OAuth button with GitHub styling

### Integration Architecture
- Django authentication backend with custom User model
- django-allauth integration with email verification
- FastHTML session synchronization with Django
- Security middleware properly configured
- Form validation with terminal-style error messages
- Email verification with terminal-themed confirmation pages

### User Profiles
- Terminal-inspired profile layout
- AI percentage visualization with acid green progress bar
- Social links with terminal styling
- Bio section with monospace typography
- Profile editing with real-time validation

### Dashboard Implementation
- Project cards with status indicators
- Terminal-themed activity feed
- AI Assistant integration placeholder
- Stats display with acid green values
- Authorization checks on all routes

### Critical CSS Components
```css
/* Terminal-style cards for auth forms */
.terminal-card {
    background: var(--terminal);
    border: 1px solid var(--acid);
    border-radius: 4px;
    padding: 2.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.terminal-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2rem;
    background: rgba(0, 0, 0, 0.2);
    border-bottom: 1px solid var(--acid);
}

.terminal-card::after {
    content: '● ● ●';
    position: absolute;
    top: 0.5rem;
    left: 1rem;
    color: var(--smoke);
    font-size: 0.8rem;
    letter-spacing: 0.5rem;
}

/* Terminal-style buttons with hover effects */
.terminal-button {
    background: transparent;
    color: var(--acid);
    border: 1px solid var(--acid);
    padding: 0.8rem 1.5rem;
    font-weight: 700;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    position: relative;
    overflow: hidden;
}

.terminal-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 0;
    height: 100%;
    background: var(--acid);
    transition: width 0.3s ease;
    z-index: -1;
}

.terminal-button:hover {
    color: var(--terminal);
}

.terminal-button:hover::before {
    width: 100%;
}
```

### Email Verification Implementation
- Terminal-styled verification pages with consistent design language
- Custom FastHTML routes for email confirmation
- Verification status checking during login
- Automatic email sending on signup
- Error handling for expired or invalid verification links
- Responsive design for all verification pages

## Demo Page Implementation

The demo page has been implemented with the following key elements:

### Interactive Code Generation Demo
- Terminal-style code display with syntax highlighting
- Copy-to-clipboard functionality
- Responsive design for all devices
- Smooth animations and transitions
- Toast notifications for user feedback

### Syntax Highlighting with Prism.js
- Integration with Prism.js for code highlighting
- Custom theme matching our terminal aesthetic
- Support for HTML, CSS, and JavaScript highlighting
- Automatic initialization after code generation
- Mobile-optimized display with proper font sizing

### Critical CSS Components
```css
/* Code block styling with syntax highlighting */
.code-block {
    background: rgba(0, 0, 0, 0.2);
    padding: 1.5rem;
    border-radius: 4px;
    overflow-x: auto;
    max-height: 500px;
    overflow-y: auto;
    color: #d4d4d4;
    margin: 0;
    font-family: var(--font-mono);
    font-size: 0.9rem;
    line-height: 1.5;
}

/* Mobile optimization for code blocks */
@media (max-width: 768px) {
    .code-block {
        max-height: 300px;
        font-size: 0.8rem;
    }

    .copy-btn {
        top: 0.5rem;
        right: 0.5rem;
        padding: 0.3rem 0.6rem;
        font-size: 0.7rem;
    }
}
```

### Implementation Details
- Prism.js scripts and styles loaded in app.py for global availability
- Copy functionality using navigator.clipboard API
- Toast notifications for user feedback
- Responsive design with mobile-specific adjustments
- Automatic syntax highlighting initialization after code generation

### ⚠️ IMPORTANT NOTES
1. Always use Prism.js for syntax highlighting throughout the platform
2. Maintain consistent styling for code blocks across all features
3. Ensure copy functionality works across all browsers
4. Keep mobile optimization in mind for all code displays

## Next Steps
1. Complete authentication system with GitHub OAuth integration
2. Begin implementing community features with code sharing capabilities
3. Prepare for Vercel deployment
4. Focus on implementing remaining sections while maintaining the same level of polish
5. Ensure all new features maintain consistent terminal/code aesthetic
6. Document any new animations or effects in similar detail
7. Implement code sharing with syntax highlighting in community features
