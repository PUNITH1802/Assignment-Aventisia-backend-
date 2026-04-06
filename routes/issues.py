from fastapi import APIRouter, Query

from services import github
from models.schemas import CreateIssueRequest

router = APIRouter(tags=["Issues"])


@router.get(
    "/repos/{owner}/{repo}/issues",
    summary="List issues in a repository",
    response_description="A list of issues",
)
async def list_issues(
    owner: str,
    repo: str,
    state: str = Query("open", pattern="^(open|closed|all)$", description="Issue state filter"),
    per_page: int = Query(30, ge=1, le=100),
    page: int = Query(1, ge=1),
):
    """
    Fetch issues from a specific repository.
    Calls `GET https://api.github.com/repos/{owner}/{repo}/issues`.
    """
    return await github.fetch_repo_issues(
        owner=owner, repo=repo, state=state, per_page=per_page, page=page
    )


@router.post(
    "/repos/{owner}/{repo}/issues",
    status_code=201,
    summary="Create an issue in a repository",
    response_description="The newly created issue",
)
async def create_issue(owner: str, repo: str, payload: CreateIssueRequest):
    """
    Create a new issue in a repository.
    Calls `POST https://api.github.com/repos/{owner}/{repo}/issues`.

    **Request body:**
    ```json
    {
      "title": "Issue title",
      "body": "Issue description",
      "labels": ["bug"]
    }
    ```
    """
    return await github.create_repo_issue(owner=owner, repo=repo, payload=payload)
