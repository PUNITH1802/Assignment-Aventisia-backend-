import httpx
import logging
from fastapi import HTTPException

from config.settings import GITHUB_API_BASE, get_auth_headers
from models.schemas import CreateIssueRequest

logger = logging.getLogger(__name__)


async def fetch_user_repos(per_page: int = 30, page: int = 1) -> list[dict]:
    """Fetch repositories for the authenticated GitHub user."""
    url = f"{GITHUB_API_BASE}/user/repos"
    params = {
        "per_page": per_page,
        "page": page,
        "sort": "updated",
        "direction": "desc",
    }
    return await _github_get(url, params=params)


async def fetch_repo_issues(
    owner: str, repo: str, state: str = "open", per_page: int = 30, page: int = 1
) -> list[dict]:
    """Fetch issues from a repository."""
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues"
    params = {
        "state": state,
        "per_page": per_page,
        "page": page,
    }
    return await _github_get(url, params=params)


async def create_repo_issue(
    owner: str, repo: str, payload: CreateIssueRequest
) -> dict:
    """Create a new issue in a repository."""
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues"
    body = payload.model_dump(exclude_none=True)
    return await _github_post(url, body=body)


async def fetch_repo_commits(
    owner: str, repo: str, per_page: int = 30, page: int = 1
) -> list[dict]:
    """Fetch commits from a repository."""
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/commits"
    params = {"per_page": per_page, "page": page}
    return await _github_get(url, params=params)


async def fetch_authenticated_user() -> dict:
    """Fetch the authenticated GitHub user profile."""
    url = f"{GITHUB_API_BASE}/user"
    return await _github_get(url)


# ── Internal helpers ──────────────────────────────────────────────────────────

async def _github_get(url: str, params: dict | None = None) -> dict | list:
    """Execute an authenticated GET request to the GitHub API."""
    try:
        headers = get_auth_headers()
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            return _handle_response(response)
        except httpx.RequestError as exc:
            logger.error("GitHub GET request failed: %s", exc)
            raise HTTPException(status_code=503, detail="Failed to reach GitHub API.")


async def _github_post(url: str, body: dict) -> dict:
    """Execute an authenticated POST request to the GitHub API."""
    try:
        headers = get_auth_headers()
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.post(url, headers=headers, json=body)
            return _handle_response(response)
        except httpx.RequestError as exc:
            logger.error("GitHub POST request failed: %s", exc)
            raise HTTPException(status_code=503, detail="Failed to reach GitHub API.")


def _handle_response(response: httpx.Response) -> dict | list:
    """Map GitHub API HTTP errors to FastAPI HTTPExceptions."""
    status = response.status_code

    if status == 200 or status == 201:
        return response.json()

    error_data = response.json() if response.content else {}
    message = error_data.get("message", "Unknown GitHub API error.")

    if status == 401:
        raise HTTPException(status_code=401, detail=f"Invalid or missing GitHub token: {message}")
    elif status == 403:
        raise HTTPException(status_code=403, detail=f"GitHub API access forbidden: {message}")
    elif status == 404:
        raise HTTPException(status_code=404, detail=f"Resource not found on GitHub: {message}")
    elif status == 422:
        raise HTTPException(status_code=422, detail=f"Validation error from GitHub: {message}")
    elif status == 429:
        raise HTTPException(status_code=429, detail="GitHub API rate limit exceeded. Please try again later.")
    else:
        raise HTTPException(status_code=status, detail=f"GitHub API error: {message}")
