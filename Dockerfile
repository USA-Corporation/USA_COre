FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash user
WORKDIR /home/user/app

# Create data directory and set permissions
RUN mkdir -p /home/user/app/data && chown -R user:user /home/user/app

# Switch to non-root user
USER user

# Install Python dependencies
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application code
COPY --chown=user:user . .

# Expose port (Render uses 10000)
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:10000/health', timeout=2)" || exit 1

# ⭐️ CRITICAL: This CMD must exist and be correct ⭐️
# Option 1: Direct Python (for development)
CMD ["python", "app.py"]

# Option 2: Gunicorn (for production - RECOMMENDED)
# CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--workers", "4", "app:app"]
