# =============================================================================
# Dockerfile for D'Agri Talk Frontend (React Application)
# =============================================================================

# --- Stage 1: Build Stage ---
# Use a Node.js image to build the React application.
# 'alpine' is a lightweight version of the image.
# We name this stage 'build' to reference it later.
FROM node:20-alpine AS build

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to leverage Docker layer caching.
COPY package*.json ./

# Install dependencies using 'npm ci' which is faster and safer for builds
RUN npm ci

# Copy the rest of the application source code
COPY . .

# Build the application for production
RUN npm run build

# --- Stage 2: Production Stage ---
# Use a lightweight Nginx image to serve the static files.
FROM nginx:stable-alpine

# Copy the custom Nginx configuration for single-page applications
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the built static assets from the 'build' stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# Command to run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]