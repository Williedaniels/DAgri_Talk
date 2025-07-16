-- D'Agri Talk Database Initialization Script
-- This script sets up the initial database schema and data

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
CREATE TYPE user_type_enum AS ENUM ('farmer', 'elder', 'buyer', 'admin');
CREATE TYPE listing_status_enum AS ENUM ('active', 'sold', 'expired');

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type user_type_enum NOT NULL,
    location VARCHAR(100),
    phone VARCHAR(20),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Knowledge entries table
CREATE TABLE IF NOT EXISTS knowledge_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    language VARCHAR(50) DEFAULT 'English',
    crop_type VARCHAR(100),
    season VARCHAR(50),
    region VARCHAR(100),
    author_id UUID REFERENCES users(id) ON DELETE CASCADE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Market listings table
CREATE TABLE IF NOT EXISTS market_listings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop_name VARCHAR(100) NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    price_per_unit DECIMAL(10,2) NOT NULL,
    location VARCHAR(100) NOT NULL,
    description TEXT,
    farmer_id UUID REFERENCES users(id) ON DELETE CASCADE,
    status listing_status_enum DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_type ON users(user_type);
CREATE INDEX idx_knowledge_crop_type ON knowledge_entries(crop_type);
CREATE INDEX idx_knowledge_region ON knowledge_entries(region);
CREATE INDEX idx_listings_status ON market_listings(status);
CREATE INDEX idx_listings_location ON market_listings(location);

-- Insert sample data for development
INSERT INTO users (username, email, password_hash, user_type, location) VALUES
('elder_john', 'john@example.com', '$2b$12$sample_hash', 'elder', 'Monrovia'),
('farmer_mary', 'mary@example.com', '$2b$12$sample_hash', 'farmer', 'Bong County'),
('buyer_david', 'david@example.com', '$2b$12$sample_hash', 'buyer', 'Monrovia');

-- Sample knowledge entry
INSERT INTO knowledge_entries (title, content, crop_type, season, region, author_id) VALUES
('Traditional Rice Planting', 'Best practices for planting rice during the rainy season...', 'Rice', 'Rainy Season', 'Bong County', 
 (SELECT id FROM users WHERE username = 'elder_john'));

-- Sample market listing
INSERT INTO market_listings (crop_name, quantity, unit, price_per_unit, location, farmer_id) VALUES
('Rice', 100.00, 'kg', 2.50, 'Bong County', 
 (SELECT id FROM users WHERE username = 'farmer_mary'));