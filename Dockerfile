FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash user
WORKDIR /home/user/app

# Create data directory and set permissions
RUN mkdir -p /home/user/app/data && chown -R user:user /home/user/app

# Switch to non-root user
USER user

# Add local bin to PATH for pip --user installs
ENV PATH="/home/user/.local/bin:${PATH}"
ENV PYTHONPATH="/home/user/app:${PYTHONPATH}"

# Install Python dependencies
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application code
COPY --chown=user:user . .

# Expose port (Render uses 10000)
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:10000/health || exit 1

# ⭐️⭐️⭐️ CRITICAL: Choose ONE based on your app structure ⭐️⭐️⭐️

# OPTION 1: If your FastAPI app is in main.py (root level)
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000", "--proxy-headers"]

# OPTION 2: If your FastAPI app is in app/main.py (recommended structure)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000", "--proxy-headers"]

# OPTION 3: If using gunicorn with uvicorn workers (production)
# CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:10000", "--timeout", "120"]

# OPTION 4: With auto-reload for development (don't use in production)
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000", "--reload"]
