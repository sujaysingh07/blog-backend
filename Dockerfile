FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies into the container
RUN uv sync --locked --no-dev

# Copy application code
COPY src ./src

# The application listens on port 8000
EXPOSE 8000

# Start FastAPI
CMD ["uv", "run", "--no-dev", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]