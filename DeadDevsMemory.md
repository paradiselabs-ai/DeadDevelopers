### Memory of the DeadDevelopers Web Application

#### Backend
- **Framework:** Django
  - Handles authentication, database models, and business logic.
  - Custom User model with an extended field `ai_percentage`.
  - **Settings Location:** `django_config/` directory.
  - **Tests Location:** `django_tests/` directory.

#### Frontend
- **Framework:** FastHTML
  - Provides UI and hypermedia capabilities.
  - Integrates:
    - Starlette
    - Uvicorn
    - HTMX
    - fastcore’s FT
  - Uses Pico CSS (default in FastHTML) with custom styling.
  - HTMX enables dynamic interactions without custom JavaScript.

#### Architecture
- **Hybrid Architecture:**
  - Django for backend.
  - FastHTML for frontend.

#### Project Structure
- **Well-Organized Structure:**
  - Clear separation of concerns.
  - Django configuration is isolated in the `django_config/` directory.
  - FastHTML routes are organized in the `routes/` directory with specific files for each feature.

#### Main Application Files
- **`app.py`:**
  - Sets up the FastHTML app with authentication middleware.
  - Connects to Django’s User model.
- **`main.py`:**
  - Main entry point.
  - Contains the landing page.
  - Imports all routes.

#### Routes
- **`routes/auth.py`:**
  - Manages authentication routes: login, signup, logout.
- **`routes/dashboard.py`:**
  - Manages dashboard and user-specific features.
- **`routes/demo.py`:**
  - Contains demo features.
- **`routes/features.py`:**
  - Displays feature showcase pages.
- **Additional Routes:**
  - `about.py` - About page.
  - `blog.py` - Blog functionality.
  - `community.py` - Community features.
  - `header.py` - Header component.

#### Static Files
- **Directory:** `static/`
  - Contains CSS, JS, and images used throughout the application.

#### Testing Infrastructure
- **Comprehensive Test Coverage:**
  - Separate test files for each route.
  - Both Django model tests (`tests.py`) and FastHTML application tests (`test_app.py`) are present.
  - Consistent naming convention: `test_*.py`.

#### Development Environment
- **Tools and Configuration:**
  - Uses VSCode (`.vscode/` directory present).
  - Proper environment configuration (`.env.example`).
  - Includes deployment configuration (`vercel.json`).
  - Uses Black for code formatting (`.blackboxrules`).

#### Documentation
- **Comprehensive Documentation:**
  - FastHTML documentation (`fastHTML.md`).
  - Project README (`README.md`).
  - GitHub workflow configurations (`.github/` directory).

#### Current Development Priorities
1. **Fix Failing Tests:**
   - Marked with xfail.
2. **Improve Test Coverage:**
   - Following TDD principles.
3. **Separation:**
   - Ensure proper separation between Django and FastHTML components.
4. **Authentication Flow:**
   - Resolve issues between Django and FastHTML.

#### Key Aspects of FastHTML in This Project
- **UI Elements:**
  - Created using FT components in a Pythonic way.
- **Beforeware in `app.py`:**
  - Handles authentication checks between Django and FastHTML.
- **Sessions:**
  - Used for maintaining user state.
- **Toast Notifications:**
  - Set up for user feedback.
