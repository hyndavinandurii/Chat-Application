# Stage 1: Build Stage
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Stage
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /usr/local /usr/local

# Copy application files from builder stage
COPY --from=builder /app /app

# Expose port
EXPOSE 80

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["flask", "run", "--port=80"]
