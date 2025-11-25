# Document AI Platform
A local Document AI web application for creating, editing, and exporting documents and presentations. This repo contains a small Flask-style web app (server-side templates) with user/project management, document generation utilities, and integration helpers for an LLM backend.

This README is specific to the code in this repository and explains how to run and extend the project locally.

## What this project includes

- `app.py` — Application entry point and web server.
- `database.py` — MongoDB connection and helpers.
- `models/` — Mongoose/ODM-style models (e.g., `project.py`, `user.py`) used for persisting users and projects.
- `routes/` — Route handlers for authentication and app features (`auth.py`, `document.py`, `project.py`).
- `templates/` — Jinja2/Flask templates used by the server (`base.html`, `login.html`, `dashboard.html`, etc.).
- `static/` — Static assets (CSS, JS, third-party libraries).
- `utils/` — Helper utilities including `docx_generator.py`, `pptx_generator.py`, and `gemini.py` for LLM/AI integration.
- `.env` — Local environment variables (not tracked here, create your own).

## Project structure

Below is the directory structure for this repository (reflects the current workspace):

```
.
├── app.py
├── database.py
├── requirements.txt
├── .env
├── models/
│   ├── project.py
│   ├── user.py
│   └── __pycache__/
├── routes/
│   ├── auth.py
│   ├── auth.py.bak
│   ├── document.py
│   ├── project.py
│   └── __pycache__/
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   └── style.css
│   └── js/
│       ├── bootstrap.bundle.min.js
│       ├── jquery.min.js
│       └── main.js
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── editor.html
│   ├── login.html
│   ├── project_new.html
│   └── register.html
└── utils/
	├── docx_generator.py
	├── gemini.py
	├── pptx_generator.py
	└── __pycache__/
```

## Key features

- User authentication and session-backed project management.
- Document and presentation generation helpers (DOCX and PPTX exporters).
- Basic editor interface and project pages rendered via server templates.
- Integration points for an LLM (see `utils/gemini.py`) to support AI-assisted document content.

## Prerequisites

- Python 3.10 or newer
- A running MongoDB instance (Atlas or local)
- (Optional) API key for any LLM provider you integrate (stored in `.env`)

## Quickstart (Windows PowerShell)

1) Create and activate a Python virtual environment

```powershell
python -m venv venv
; .\venv\Scripts\Activate.ps1
```

2) Install dependencies

```powershell
pip install -r requirements.txt
```

3) Create a `.env` file in the project root with the required variables.

Example `.env` (DO NOT commit):

```
MONGO_URI="your-mongo-connection-string"
SECRET_KEY="a-long-secret-for-sessions"
# Optional API keys used by utils/gemini.py
GOOGLE_API_KEY="your-google-api-key-or-llm-key"
```

4) Start the application

```powershell
# From project root
python app.py
# or, if the project uses Flask app factory:
# flask run
```

5) Open `http://localhost:5000/` (or the port shown in the console)

Note: If `app.py` binds a different port, use the console output or check `app.py` for configuration.

## Development notes

- Templates are in `templates/`. Edit `base.html` to change global layout.
- Static assets are in `static/` (CSS/JS). `static/js/main.js` contains frontend behaviors.
- Routes are in `routes/`. Add or modify route handlers to extend functionality.
- Document generation code lives in `utils/docx_generator.py` and `utils/pptx_generator.py`.
- `utils/gemini.py` is a helper to call an LLM or other AI — update it with your API client and keys.
- Session and history persistence are handled via MongoDB; see `database.py` and `models/` for schema details.

## Recommended local development workflow

- Use the virtual environment to keep dependencies isolated.
- Add a `.env` file and use a library like `python-dotenv` if your app loads environment variables automatically.
- When editing templates or static assets, refresh the browser to see updates.

## Useful commands

- Create venv: `python -m venv venv`
- Activate (PowerShell): `.\venv\Scripts\Activate.ps1`
- Install: `pip install -r requirements.txt`
- Run app: `python app.py` or `flask run`

## Environment & secrets

This repository currently contains a local `.env` in your workspace. DO NOT commit real API keys or database credentials to version control. Use a `.env.example` with placeholder values to document required keys.

Required keys (example):

- `MONGO_URI` — MongoDB connection string
- `SECRET_KEY` — session secret
- `GOOGLE_API_KEY` (optional) — API key used by `utils/gemini.py`

Create `.env.example` with placeholder values and add `.env` to `.gitignore` if not already ignored.

## Docker (optional)

If you'd like a Docker setup, I can add a `Dockerfile` and `docker-compose.yml` that runs the app and a MongoDB service for local testing.

## Next steps I can help with

- Add a `.env.example` and update `.gitignore`.
- Add a `Dockerfile` + `docker-compose.yml` for local development.
- Wire `utils/gemini.py` to a real LLM client and provide example prompts.
- Create a small smoke-test script that exercises login → create project → export doc flow.

Tell me which follow-up you'd like and I will make it next.

## License

This project uses the MIT License (check `LICENSE` in the repo).

