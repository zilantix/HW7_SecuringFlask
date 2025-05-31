# Use minimal base image
FROM python:3.9-alpine

# Create a non-root user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set permissions and switch to non-root user
RUN chown -R appuser:appgroup /app
USER appuser

# Define health check endpoint (adjust port/path as needed)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:5000/health || exit 1
HEALTHCHECK CMD curl --fail http://localhost:5000/ || exit 1

# Prevent container from acquiring new privileges
# (reinforced at runtime via docker-compose or run command)
CMD ["python", "app.py"]
