FROM python:3.11-slim

# ... (ENV and apt-get sections remain the same) ...

# 1. Create the user
RUN useradd --create-home --shell /bin/bash user
WORKDIR /home/user/app

# 2. Create the data directory as ROOT and set permissions
# This ensures the 'user' owns everything in the app folder
RUN mkdir -p /home/user/app/data && chown -R user:user /home/user/app

# 3. NOW switch to the non-root user
USER user

# 4. Proceed with pip and copy
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY --chown=user:user . .

# ... (Expose, Healthcheck, and CMD remain the same) ...
