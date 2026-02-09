# ... (System deps and user creation) ...

WORKDIR /home/user/app

# 1. Create the data directory as ROOT first
RUN mkdir -p /home/user/app/data

# 2. NOW change ownership of the entire app directory recursively
RUN chown -R user:user /home/user/app

# 3. NOW switch to the non-root user
USER user

# ... (Continue with COPY and pip install) ...
