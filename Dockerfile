# Stage 1: Build Vite frontend
FROM node:20 AS frontend-builder
WORKDIR /app
COPY frontend/ ./frontend/
WORKDIR /app/frontend
RUN npm install && npm run build

# Stage 2: Build Python backend
FROM python:3.11-slim
WORKDIR /app

# Install runtime dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY api/ ./api/

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist/ ./frontend/

# Expose port for FastAPI
EXPOSE 8000

# Use environment variable for OpenAI key
ENV OPENAI_API_KEY=not-set

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
