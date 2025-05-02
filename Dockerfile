# Stage 1: Build frontend
FROM node:18 AS frontend-builder
WORKDIR /app
COPY frontend/ ./frontend/
WORKDIR /app/frontend
RUN npm install && npm run build

# Stage 2: Build backend
FROM python:3.11-slim
WORKDIR /app
COPY api/ ./api/
COPY --from=frontend-builder /app/frontend/dist/ ./frontend/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
