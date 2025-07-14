# Dockerfile for the frontend service
FROM node:20

# Set the working directory for the frontend
WORKDIR /app

# Set the working directory for the frontend
COPY frontend/package.json frontend/package-lock.json ./

# Clean install to avoid native rollup
RUN npm install 

# Copy the rest of the frontend code
COPY . .

# Start the development server
CMD ["sh", "-c", "npm run dev -- --host 0.0.0.0 --port $FRONTEND_PORT"]
