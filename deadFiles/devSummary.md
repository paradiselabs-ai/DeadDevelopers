# DeadDevelopers Project Status Summary

## Current Status

The DeadDevelopers platform is in early development stage. We've established the technical architecture using a hybrid approach with Django for backend functionality and FastHTML for the modern hypermedia-driven frontend experience.

### Completed Work
- Basic authentication system (Django-based)
- Project structure and directory organization
- Initial styling with terminal/code/post-punk aesthetic
- Profile page HTML structure (initial version)
- HTMX integration for dynamic content
- User model with basic AI usage tracking

### Technical Architecture
- **Backend**: Django with custom User model
- **Frontend**: FastHTML + HTMX for hypermedia-driven interface
- **Styling**: Custom CSS with terminal-inspired design system
- **Database**: Django ORM (SQLite for development)
- **Deployment**: Configured for Vercel

## Important Note About HTML Files

**CRITICAL for new developers:** The HTML files in the templates directory are NOT meant to be used directly. Instead, they serve as reference for the FastHTML components that need to be created. In the FastHTML architecture:

1. HTML is generated through Python functions that return FT components
2. No HTML templates are rendered directly
3. All HTML files should be converted to FastHTML component structures

Example: The `profile.html` file should not be used directly but serves as a reference for creating a FastHTML component-based equivalent in Python code.

## Next Steps

The following tasks need to be addressed by the next developer:

### 1. Template Conversion
- Convert all HTML templates to FastHTML component-based approach
- Migrate HTMX attributes to their FastHTML equivalents (e.g., `hx_post` instead of `hx-post`)
- Ensure all JavaScript is properly integrated with FastHTML's component system

### 2. Feature Implementation
- Complete the AI usage tracking system
- Add AI Dev Score calculation and display
- Implement community features (forums, chat)
- Create challenge system infrastructure
- Add social connectivity options
- Develop achievement tracking system

### 3. Profile Page Enhancements
- Add AI toolchain section to profile
- Implement achievement display area
- Add community rank visualization
- Create data visualization for AI usage trends
- Connect profile to the community features

### 4. Authentication
- Complete GitHub/GitLab OAuth integration
- Finalize user session management
- Implement proper security measures for AI percentage tracking

## Design Guidelines

When implementing new features, adhere to these design principles:
- Use the established color palette: acid green (#00ff66), voltage blue (#7df9ff), terminal black (#1a1a1a), dark steel (#2b2b2b)
- Maintain the terminal/code/post-punk aesthetic
- All interactive elements should have subtle animations
- Focus on a clean, minimalist interface with terminal-inspired elements

## Development Workflow

1. Use Black formatter for all Python code
2. Verify all FastHTML components follow the correct syntax
3. Ensure proper use of HTMX attributes in the FastHTML format
4. Test each component both in isolation and integrated with the system
5. Update documentation with new features as they're completed

The project is currently at a critical juncture where we need to fully transition from the traditional Django template approach to the FastHTML component-based system. This transition should be the top priority before adding significant new features.