========================================================================
TEAM TASK MANAGER - FULL-STACK APPLICATION DOCUMENTATION
========================================================================

1. PROJECT OVERVIEW
-------------------
Team Task Manager is a production-grade, highly responsive web application
engineered to streamline project distributions, team assignments, and real-time
workload tracking. Built with a monolithic runtime context, it ensures strict
role-based visibility configurations for enterprise workflow isolation.

2. PRODUCTION TECH STACK
------------------------
- Backend Core: Python 3.11 / FastAPI (Asynchronous framework pipeline)
- View Engine: Jinja2 Server-Side Rendered Templates
- Dynamic States: HTMX Dynamic Component DOM-swapping (Zero SPA bundle lag)
- Database Layer: PostgreSQL Relational Database (SQLAlchemy ORM Layer)
- UI/UX Blueprint: Tailwind CSS Engine (Mobile-First responsive grids)
- Platform Host: Railway App Container Cloud Environment

3. CORE KEY FEATURES
--------------------
- Secure Authentication: Password hashing layer paired with HTTPOnly cookie session variables.
- Multi-Tenant Access Matrix: Differentiated dashboards for Admin (write/modify paths) and Members (view/patch states).
- Project Lifecycle Orchestration: Relational isolation grouping structural tasks into individual workspaces.
- Reactive Metrics Tracking: Computational trackers evaluating dynamic progression indicators and chronological overdue violations.

4. LOCAL RUNTIME COMMANDS
-------------------------
To initialize the workspace locally, execute the following parameters:

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows

# Install application dependencies
pip install -r requirements.txt

# Run server pipeline
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

========================================================================
DEPLOYED LIVE REGISTRY BY AMALV313-PNG
========================================================================
