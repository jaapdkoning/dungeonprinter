# Stage 1: Build frontend
FROM node:20 AS frontend-builder
WORKDIR /app
COPY frontend/ ./frontend/
WORKDIR /app/frontend
RUN npm install && npm run build

# Stage 2: Backend + static hosting
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY api/ ./api/

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist/ ./frontend/

# Expose port
EXPOSE 8000

# Start server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]