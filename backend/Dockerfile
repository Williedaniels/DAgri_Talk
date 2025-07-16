# =============================================================================
# D'Agri Talk Backend - Multi-Stage Production Dockerfile
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Build Dependencies (Builder Stage)
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS builder

# Set build arguments for optimization
ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies needed for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies in user directory for better security
RUN pip install --user --no-cache-dir --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------------------
# Stage 2: Production Runtime (Final Stage)
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS production

# Set production environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/dagri/.local/bin:$PATH \
    FLASK_ENV=production

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r dagri && useradd -r -g dagri dagri
WORKDIR /app # Set workdir before copying

# Copy application code
COPY --chown=dagri:dagri . . 
COPY --chown=dagri:dagri gunicorn_conf.py .

# Copy Python packages from builder stage to the non-root user's home
COPY --from=builder --chown=dagri:dagri /root/.local /home/dagri/.local

# Switch to non-root user
USER dagri

# Expose port
EXPOSE 5000

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Use gunicorn for production WSGI server
CMD ["gunicorn", "-c", "gunicorn_conf.py", "run:app"]
