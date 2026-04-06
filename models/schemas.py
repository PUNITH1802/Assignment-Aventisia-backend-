from pydantic import BaseModel, Field
from typing import Optional


class CreateIssueRequest(BaseModel):
    title: str = Field(..., min_length=1, description="Title of the issue")
    body: Optional[str] = Field(None, description="Body/description of the issue")
    labels: Optional[list[str]] = Field(default=[], description="List of label names")


class IssueResponse(BaseModel):
    id: int
    number: int
    title: str
    body: Optional[str]
    state: str
    html_url: str
    user: dict
    labels: list
    created_at: str
    updated_at: str


class RepoResponse(BaseModel):
    id: int
    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    private: bool
    language: Optional[str]
    stargazers_count: int
    forks_count: int
    open_issues_count: int
    updated_at: str


class CommitResponse(BaseModel):
    sha: str
    commit: dict
    author: Optional[dict]
    html_url: str


class ErrorResponse(BaseModel):
    detail: str
    status_code: int
