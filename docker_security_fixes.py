import os
import shutil
from pathlib import Path

SOURCE = "before"
DEST = "after"

# Step 1: Copy entire folder
if os.path.exists(DEST):
    shutil.rmtree(DEST)
shutil.copytree(SOURCE, DEST)
print(f"Copied {SOURCE} to {DEST}")

# Step 2: Fix app.py
app_path = os.path.join(DEST, "app.py")
with open(app_path, "r") as f:
    code = f.read()

code = code.replace('eval(expression)', 'ast.literal_eval(expression)')
code = code.replace('PASSWORD = "supersecretpassword"', 'import os\nPASSWORD = os.getenv("PASSWORD")')
code = code.replace("shell=True", "")
code = code.replace("0.0.0.0", "127.0.0.1")
if "import ast" not in code:
    code = "import ast\n" + code

with open(app_path, "w") as f:
    f.write(code)

print("✅ Updated app.py with safer eval, subprocess, and localhost binding")

# Step 3: Fix Dockerfile
dockerfile_path = os.path.join(DEST, "Dockerfile")
dockerfile = f"""
FROM python:3.13-alpine
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER appuser
HEALTHCHECK CMD curl --fail http://localhost:5000 || exit 1
"""

with open(dockerfile_path, "w") as f:
    f.write(dockerfile.strip() + "\n")

print("✅ Rewritten Dockerfile with non-root user and HEALTHCHECK")

# Step 4: Fix docker-compose.yml
compose_path = os.path.join(DEST, "docker-compose.yml")
with open(compose_path, "w") as f:
    f.write("""\
version: '3'
services:
  web:
    build: .
    ports:
      - "127.0.0.1:5050:5000"
    environment:
      - PASSWORD=${PASSWORD}
    read_only: true
    mem_limit: 256m
    pids_limit: 100
    security_opt:
      - no-new-privileges:true
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: secureuser
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    mem_limit: 256m
    pids_limit: 100
    security_opt:
      - no-new-privileges:true
""")

print(" docker-compose.yml rewritten with hardening options")

# Step 5: Create .env file
env_path = os.path.join(DEST, ".env")
with open(env_path, "w") as f:
    f.write("PASSWORD=SecurePass123\nDB_PASSWORD=SecureDBPass456\n")

print(" Created .env file with secrets")


