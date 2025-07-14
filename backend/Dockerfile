# Backend Dockerfile
FROM python:3.13-slim

# Set workdir
WORKDIR /app

# Copy backend code
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY backend .

# Copy entrypoint script and make it executable
COPY backend/scripts/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# Run database migrations
ENTRYPOINT ["/entrypoint.sh"]

# Start FastAPI app
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT"]
