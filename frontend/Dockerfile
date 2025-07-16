# =============================================================================
# D'Agri Talk Frontend - Multi-Stage Production Dockerfile
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Build React Application (Builder Stage)
# -----------------------------------------------------------------------------
    FROM node:18-alpine AS builder

    # Set build arguments
    ARG NODE_ENV=production
    ARG REACT_APP_API_URL
    
    # Set working directory
    WORKDIR /app
    
    # Copy package files for better layer caching
    COPY package*.json ./
    
    # Install dependencies with npm ci for faster, reliable builds
    RUN npm run build:docker
    
    # Copy source code
    COPY . .
    
    # Build the React application
    RUN npm run build
    
    # -----------------------------------------------------------------------------
    # Stage 2: Production Web Server (Final Stage)
    # -----------------------------------------------------------------------------
    FROM nginx:alpine AS production
    
    # Install curl for health checks
    RUN apk add --no-cache curl
    
    # Remove default nginx configuration
    RUN rm /etc/nginx/conf.d/default.conf
    
    # Copy custom nginx configuration
    COPY docker/nginx/nginx.conf /etc/nginx/nginx.conf
    COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf
    
    # Copy built React app from builder stage
    COPY --from=builder /app/build /usr/share/nginx/html
    
    # Create nginx user and set permissions
    RUN chown -R nginx:nginx /usr/share/nginx/html && \
        chmod -R 755 /usr/share/nginx/html
    
    # Expose port 80
    EXPOSE 80
    
    # Health check for container orchestration
    HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
        CMD curl -f http://localhost:80 || exit 1
    
    # Start nginx
    CMD ["nginx", "-g", "daemon off;"]