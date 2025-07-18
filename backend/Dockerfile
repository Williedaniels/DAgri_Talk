# =============================================================================
# Dockerfile for D'Agri Talk Backend (Flask Application)
# =============================================================================

# --- Base Stage ---
# Use an official Python runtime as a parent image.
# 'slim' is a smaller version of the image, good for production.
FROM python:3.11-slim-bullseye

# --- Configuration ---
# Set environment variables to prevent Python from writing .pyc files to disk
# and to keep Python from buffering stdout and stderr.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container to /app
WORKDIR /app

# --- Dependency Installation ---
# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir disables the pip cache, which is not needed in a container build
RUN pip install --no-cache-dir -r requirements.txt

# --- Application Code ---
# Copy the rest of the application's source code from your host to your image filesystem.
COPY . .

# --- Security Best Practice ---
# Create a non-root user and switch to it.
RUN addgroup --system app && adduser --system --group app
USER app

# --- Execution ---
# Expose the port the app runs on for ALB target group.
EXPOSE 5000

# Run the application using Gunicorn, a production-grade WSGI server.
# This assumes your Flask application instance in `run.py` is named `app`.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]