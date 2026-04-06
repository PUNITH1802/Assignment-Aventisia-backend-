import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
GITHUB_API_BASE: str = "https://api.github.com"
APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"


def get_auth_headers() -> dict[str, str]:
    if not GITHUB_TOKEN:
        raise ValueError(
            "GITHUB_TOKEN is not set. Please add it to your .env file."
        )
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
