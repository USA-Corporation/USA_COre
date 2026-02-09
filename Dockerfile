FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/user/.local/bin:$PATH"

# Install system dependencies + curl for healthchecks
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash user
WORKDIR /home/user/app

# Switch to non-root user
USER user

# Copy requirements first for caching
COPY --chown=user:user requirements.txt .

# Install Python dependencies
# Ensure gunicorn and uvicorn are in requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application code
COPY --chown=user:user . .

# Create data directory (User already owns WORKDIR, but explicit is better)
RUN mkdir -p /home/user/app/data

# Expose port (Render uses 10000 by default, but we'll use the variable in CMD)
EXPOSE 10000

# Health check (Using python instead of curl if you don't want to install curl)
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:10000/health || exit 1

# Run the application
# Reduced workers to 2 to avoid OOM (Status 128) on smaller instances
CMD ["gunicorn", "app:app", "--workers=2", "--worker-class=uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:10000", "--timeout=120"]
