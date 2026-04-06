# GitHub Cloud Connector

A production-ready backend service built with **Python + FastAPI** that authenticates with GitHub and exposes clean REST API endpoints for managing repositories and issues.

---

## Features

- **Personal Access Token (PAT)** authentication — stored securely in `.env`
- Fully async API using `httpx` and FastAPI
- Interactive Swagger UI at `/docs`
- Structured error handling with meaningful HTTP status codes
- Clean, modular project structure
- Built-in logging

---

## Project Structure

```
github-connector/
├── main.py                  # FastAPI app entry point
├── config/
│   └── settings.py          # Environment variable loading & auth headers
├── routes/
│   ├── repos.py             # /repos endpoints
│   └── issues.py            # /repos/{owner}/{repo}/issues endpoints
├── services/
│   └── github.py            # All GitHub API call logic
├── models/
│   └── schemas.py           # Pydantic request/response models
├── utils/
│   └── logger.py            # Logging configuration
├── .env.example             # Template for environment variables
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Setup Instructions

### 1. Clone / Download the project

```bash
cd github-connector
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your GitHub Personal Access Token

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
GITHUB_TOKEN=ghp_your_actual_token_here
```

**How to create a PAT:**
1. Go to [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**
3. Select scopes: `repo`, `read:user`
4. Copy the token into your `.env`

> **Never commit your `.env` file.** It is listed in `.gitignore`.

### 5. Run the server

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at: `http://localhost:8000`

---

## API Endpoints

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/me` | Get authenticated GitHub user |

### Repositories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/repos` | List all repos for authenticated user |
| GET | `/repos/{owner}/{repo}/commits` | List commits in a repo |

### Issues

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/repos/{owner}/{repo}/issues` | List issues in a repo |
| POST | `/repos/{owner}/{repo}/issues` | Create a new issue |

---

## Swagger / Interactive Docs

Once the server is running, open your browser at:

```
http://localhost:8000/docs
```

---

## Example curl Requests

**Check health:**
```bash
curl http://localhost:8000/
```

**Get authenticated user:**
```bash
curl http://localhost:8000/me
```

**List your repositories:**
```bash
curl http://localhost:8000/repos
```

**List issues:**
```bash
curl http://localhost:8000/repos/octocat/Hello-World/issues
```

**Create an issue:**
```bash
curl -X POST http://localhost:8000/repos/{owner}/{repo}/issues \
  -H "Content-Type: application/json" \
  -d '{"title": "Found a bug", "body": "Description of the bug", "labels": ["bug"]}'
```

**List commits:**
```bash
curl http://localhost:8000/repos/octocat/Hello-World/commits
```

---

## Error Handling

| Status Code | Cause |
|-------------|-------|
| 401 | Invalid or missing GitHub token |
| 403 | Insufficient token permissions |
| 404 | Repository or resource not found |
| 422 | Invalid request body |
| 429 | GitHub API rate limit exceeded |
| 503 | Could not reach GitHub API |

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Language |
| FastAPI | Web framework |
| uvicorn | ASGI server |
| httpx | Async HTTP client |
| python-dotenv | Environment variable loading |
| Pydantic v2 | Request/response validation |
