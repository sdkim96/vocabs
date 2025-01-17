# Stage 1: Base image
FROM python:3.11.9-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

## app/ 생성
WORKDIR /app

## apt-get update 및 필요한 패키지 설치
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

## poetry 설치 및 환경설정
COPY pyproject.toml poetry.lock README.md ./
COPY app ./app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Update PATH
ENV PATH="/root/.local/bin:$PATH"

# Configure Poetry to create virtual environments inside the project directory
RUN poetry config virtualenvs.in-project true

# Install dependencies
RUN poetry install --no-interaction --no-ansi


# Node.js stage
FROM node:20 AS frontend-build


# Set working directory for frontend
WORKDIR /app/frontend

# Copy only package.json and package-lock.json (if present) for caching npm install
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend files
COPY frontend ./

# Build frontend
RUN npm run build

FROM python:3.11.9-slim AS final

# Copy built frontend
WORKDIR /app
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Copy Python dependencies and application
COPY --from=base /app /app

# Set environment variables to use virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Command to run the application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]