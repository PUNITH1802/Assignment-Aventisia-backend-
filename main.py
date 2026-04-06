"""
GitHub Cloud Connector — FastAPI entry point.

Run locally:
    uvicorn main:app --reload --port 8000

Swagger UI: http://localhost:8000/docs
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import APP_HOST, APP_PORT, DEBUG
from routes.repos import router as repos_router
from routes.issues import router as issues_router
from services.github import fetch_authenticated_user
from utils.logger import setup_logging

setup_logging(debug=DEBUG)

app = FastAPI(
    title="GitHub Cloud Connector",
    description=(
        "A production-ready connector that integrates with GitHub APIs. "
        "Authenticate with a Personal Access Token (PAT) to manage repositories and issues."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repos_router)
app.include_router(issues_router)


@app.get("/", tags=["Health"], summary="API root / health check")
async def root():
    """Returns API status."""
    return {"status": "ok", "message": "GitHub Cloud Connector is running."}


@app.get("/me", tags=["Auth"], summary="Get authenticated GitHub user")
async def get_me():
    """
    Returns the authenticated GitHub user profile.
    Useful to verify your Personal Access Token is working.
    """
    return await fetch_authenticated_user()


if __name__ == "__main__":
    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT, reload=True)
