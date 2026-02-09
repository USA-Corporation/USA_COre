FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/user/.local/bin:$PATH"

# Install system dependencies + curl for the healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash user
WORKDIR /home/user/app

USER user

COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY --chown=user:user . .

RUN mkdir -p /home/user/app/data

EXPOSE 10000

# Healthcheck using curl (now installed)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:10000/health || exit 1

# Scale workers to 2 to stay within memory limits while maintaining concurrency
CMD ["gunicorn", "app:app", "--workers=2", "--worker-class=uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:10000", "--timeout=120"]
