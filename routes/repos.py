from fastapi import APIRouter, Query

from services import github
from models.schemas import RepoResponse, CommitResponse

router = APIRouter(prefix="/repos", tags=["Repositories"])


@router.get(
    "",
    summary="List authenticated user's repositories",
    response_description="A list of repositories for the authenticated user",
)
async def list_repos(
    per_page: int = Query(30, ge=1, le=100, description="Results per page"),
    page: int = Query(1, ge=1, description="Page number"),
):
    """
    Fetch all repositories for the authenticated GitHub user.
    Calls `GET https://api.github.com/user/repos`.
    """
    return await github.fetch_user_repos(per_page=per_page, page=page)


@router.get(
    "/{owner}/{repo}/commits",
    summary="List commits in a repository",
    response_description="A list of recent commits",
)
async def list_commits(
    owner: str,
    repo: str,
    per_page: int = Query(30, ge=1, le=100),
    page: int = Query(1, ge=1),
):
    """
    Fetch commits from a specific repository.
    Calls `GET https://api.github.com/repos/{owner}/{repo}/commits`.
    """
    return await github.fetch_repo_commits(owner=owner, repo=repo, per_page=per_page, page=page)
