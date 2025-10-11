# tutoring-app
Connection to MySQL using Python

### Setup

ensure you active your virtual environment

```
cp .env.example .env
uv venv #or how ever you create your venv
#activate venv, OS specific
uv pip install -r requirements.txt #uv sync
docker compose up -d
uv run main.py
```
