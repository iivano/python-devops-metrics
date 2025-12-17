# -----------------------------
# Base image
# Use slim Python image for smaller size
# -----------------------------
FROM python:3.12-slim


# -----------------------------
# Environment variables
# Prevent Python from writing .pyc files
# Ensure logs are unbuffered (stdout)
# -----------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1


# -----------------------------
# Set working directory inside container
# -----------------------------
WORKDIR /app


# -----------------------------
# Install system dependencies (minimal)
# -----------------------------
RUN apt-get update \
&& apt-get install -y --no-install-recommends \
build-essential \
&& rm -rf /var/lib/apt/lists/*


# -----------------------------
# Install Python dependencies first
# This allows Docker layer caching
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# -----------------------------
# Copy application source code
# -----------------------------
COPY app/ app/


# -----------------------------
# Expose application port
# Documentation-only (does not publish)
# -----------------------------
EXPOSE 5001


# -----------------------------
# Run the application
# -----------------------------
CMD ["python", "app/main.py"]