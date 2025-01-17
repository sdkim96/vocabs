# Base image for Python
FROM python:3.11.9-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy Python files and install dependencies
COPY pyproject.toml poetry.lock README.md ./
COPY app ./app
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi


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

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"

# Command to run the application
CMD ["python", "/app/app/main.py"]