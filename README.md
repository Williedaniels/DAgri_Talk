# D'Agri Talk - Traditional Agricultural Knowledge Platform

![D'Agri Talk Logo](docs/images/DAgri_Talk-banner.png) <!-- not available yet -->

[![CI Pipeline](https://github.com/Williedaniels/DAgri_Talk/actions/workflows/ci.yml/badge.svg)](https://github.com/Williedaniels/DAgri_Talk/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/Williedaniels/DAgri_Talk/branch/main/graph/badge.svg)](https://codecov.io/gh/Williedaniels/DAgri_Talk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌾 Project Overview

D'Agri Talk is a digital platform that preserves and shares traditional Liberian agricultural knowledge while connecting smallholder farmers with modern markets and resources. The platform bridges generational knowledge gaps by allowing elders to document traditional farming practices in local languages, while providing farmers with market access, weather information, and community support networks.

### 🎯 Problem Statement

- **Knowledge Loss**: Traditional agricultural wisdom is disappearing as elders pass away
- **Market Access**: Smallholder farmers struggle to connect with buyers and get fair prices
- **Information Gap**: Limited access to agricultural resources and modern farming techniques
- **Language Barriers**: Agricultural information often not available in local Liberian languages

### 💡 Solution

D'Agri Talk addresses these challenges by creating a comprehensive digital platform that:

- Preserves traditional knowledge through multimedia documentation
- Connects farmers directly with buyers and markets
- Provides agricultural resources and community support
- Supports multiple Liberian languages for accessibility

## ✨ Key Features

### 🏛️ Traditional Knowledge Repository

- **Multimedia Documentation**: Elders record farming wisdom with text, audio, and images
- **Multi-language Support**: Content in English and indigenous Liberian languages (Kpelle, Bassa, Gio)
- **Searchable Database**: Find knowledge by crop type, season, region, or farming technique
- **Community Validation**: Knowledge entries reviewed and validated by community experts

### 🏪 Farmer-to-Market Connection

- **Produce Listings**: Farmers list crops with quantities, prices, and availability
- **Buyer Network**: Connect with local buyers, cooperatives, and agricultural businesses
- **Real-time Pricing**: Access current market prices for various crops
- **Location-based Matching**: Find buyers and sellers in your region

### 👥 Community Support Network

- **Discussion Forums**: Ask questions and share experiences with fellow farmers
- **Expert Advice**: Access guidance from agricultural extension officers
- **Peer Learning**: Learn from successful farming practices across Liberia
- **Resource Sharing**: Information about seeds, tools, and agricultural inputs

## 🛠️ Technology Stack

### Backend

- **Framework**: Flask (Python 3.11)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **API Design**: RESTful architecture
- **Security**: CORS configuration, input validation, password hashing

### Frontend

- **Framework**: React 18 with TypeScript
- **Styling**: CSS3 with responsive design
- **State Management**: React Hooks and Context API
- **HTTP Client**: Axios for API communication
- **Mobile Optimization**: Progressive Web App (PWA) capabilities

### DevOps & Infrastructure

- **Containerization**: Docker with multi-stage builds
- **Infrastructure**: Terraform for AWS infrastructure management
- **Container Orchestration**: Amazon ECS with Fargate
- **Load Balancing**: Application Load Balancer (ALB)
- **Database**: Amazon RDS (PostgreSQL)
- **Container Registry**: Amazon ECR
- **Version Control**: Git with GitHub
- **CI/CD**: GitHub Actions
- **Testing**: pytest (backend), Jest (frontend)
- **Code Quality**: ESLint, flake8, automated testing
- **Security**: Vulnerability scanning with Trivy and Safety

## 🚀 Getting Started

### Prerequisites

- **Docker**: Docker Desktop or Docker Engine
- **Docker Compose**: Version 2.0+
- **Git**: For version control
- **AWS CLI**: For cloud deployment (optional)
- **Terraform**: For infrastructure management (optional)

### 🐳 Docker Setup (Recommended)

#### 1. Clone the Repository

```bash
git clone https://github.com/Williedaniels/DAgri_Talk.git
cd DAgri_Talk
```

#### 2. Using Docker Compose (Fastest Setup)

```bash
# Start all services with Docker Compose
docker compose up -d

# View running services
docker compose ps

# View logs
docker compose logs -f
```

#### 3. Access the Application

- **Frontend**: <http://localhost:3000>
- **Backend API**: <http://localhost:5001>
- **Database**: PostgreSQL on localhost:5432

#### 4. Stop Services

```bash
# Stop all services
docker compose down

# Stop and remove volumes (database data)
docker compose down -v
```

### 🔧 Manual Docker Setup

#### 1. Build Individual Images

```bash
# Build backend image
docker build -t dagri-talk-backend ./backend

# Build frontend image
docker build -t dagri-talk-frontend ./frontend
```

#### 2. Run with Docker Network

```bash
# Create network
docker network create dagri-talk-network

# Run PostgreSQL
docker run -d \
  --name dagri-talk-db \
  --network dagri-talk-network \
  -e POSTGRES_DB=dagri_talk_dev \
  -e POSTGRES_USER=dagri_user \
  -e POSTGRES_PASSWORD=dagri_password \
  -p 5432:5432 \
  postgres:13

# Run backend
docker run -d \
  --name dagri-talk-backend \
  --network dagri-talk-network \
  -e DATABASE_URL=postgresql://dagri_user:dagri_password@dagri-talk-db:5432/dagri_talk_dev \
  -p 5001:5001 \
  dagri-talk-backend

# Run frontend
docker run -d \
  --name dagri-talk-frontend \
  --network dagri-talk-network \
  -p 3000:80 \
  dagri-talk-frontend
```

### 🖥️ Local Development Setup (Without Docker)

#### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 12+ (optional, SQLite used for development)

#### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python run.py
```

#### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

#### 3. Access the Application

- **Frontend**: <http://localhost:3000>
- **Backend API**: <http://localhost:5001>
- **API Documentation**: <http://localhost:5001/api/docs>

### Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=sqlite:///dagri_talk_dev.db
FLASK_ENV=development
```

## 🧪 Testing

### Docker Testing

```bash
# Run backend tests in container
docker-compose exec backend pytest tests/ --cov=app --cov-report=html

# Run frontend tests in container
docker-compose exec frontend npm test -- --coverage --watchAll=false
```

### Local Testing

```bash
# Backend tests
cd backend
source venv/bin/activate
pytest tests/ --cov=app --cov-report=html

# Frontend tests
cd frontend
npm test -- --coverage
```

## 🏗️ Cloud Deployment

### AWS Infrastructure with Terraform

#### 1. Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform installed (version >= 1.0)

#### 2. Deploy Infrastructure

```bash
# Navigate to development environment
cd terraform/environments/dev

# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply the configuration
terraform apply
```

#### 3. Build and Push Container Images

```bash
# Get ECR login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
docker build -t dagri-talk-backend ./backend
docker tag dagri-talk-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/dagri-talk-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/dagri-talk-backend:latest

# Build and push frontend
docker build -t dagri-talk-frontend ./frontend
docker tag dagri-talk-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/dagri-talk-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/dagri-talk-frontend:latest
```

#### 4. Deploy to ECS

```bash
# Execute deployment script
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

## 📊 API Documentation

### Authentication Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile (requires auth)

### Knowledge Management

- `GET /api/knowledge/` - List all knowledge entries
- `POST /api/knowledge/` - Create new knowledge entry (requires auth)
- `GET /api/knowledge/{id}` - Get specific knowledge entry

### Market Listings

- `GET /api/market/` - List all market listings
- `POST /api/market/` - Create new market listing (requires auth)

### Example API Usage

#### Register a New User

```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "farmer_john",
    "email": "john@example.com",
    "password": "secure_password",
    "user_type": "farmer",
    "location": "Monrovia"
  }'
```

#### Create Knowledge Entry

```bash
curl -X POST http://localhost:5001/api/knowledge/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Traditional Rice Planting",
    "content": "Best practices for planting rice during rainy season...",
    "crop_type": "Rice",
    "season": "Rainy Season",
    "region": "Bong County",
    "language": "English"
  }'
```

## 🏗️ Project Architecture

### System Architecture

```sh
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  React Frontend │    │   Flask Backend │    │   PostgreSQL    │
│   (Port 3000)   │◄──►│   (Port 5001)   │◄──►│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └─────────────►│  GitHub Actions │◄─────────────┘
                        │  CI/CD Pipeline │
                        └─────────────────┘
```

### Container Architecture

```sh
┌──────────────—───────────────────────────────────────────────┐
│                     Docker Compose                           │
├─────────────────────────—────────────────────────────────────┤
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │  Frontend       │ │  Backend        │ │  Database       │ │
│  │  (Nginx)        │ │  (Flask/Gunicorn│ │  (PostgreSQL)   │ │
│  │  Port: 3000     │ │  Port: 5001     │ │  Port: 5432     │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└────────────────────────—─────────────────────────────────────┘
```

### Database Schema

```sql
-- Users table
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type VARCHAR(20) NOT NULL,
    location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Knowledge entries table
CREATE TABLE knowledge_entry (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    language VARCHAR(50) DEFAULT 'English',
    crop_type VARCHAR(100),
    season VARCHAR(50),
    region VARCHAR(100),
    author_id INTEGER REFERENCES user(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Market listings table
CREATE TABLE market_listing (
    id SERIAL PRIMARY KEY,
    crop_name VARCHAR(100) NOT NULL,
    quantity FLOAT NOT NULL,
    unit VARCHAR(20) NOT NULL,
    price_per_unit FLOAT NOT NULL,
    location VARCHAR(100) NOT NULL,
    description TEXT,
    farmer_id INTEGER REFERENCES user(id),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

### Pipeline Stages

1. **Code Quality**: ESLint (frontend) and flake8 (backend)
2. **Testing**: Unit tests for both frontend and backend
3. **Security**: Vulnerability scanning with Trivy and Safety
4. **Integration**: API endpoint testing
5. **Coverage**: Test coverage reporting

### Workflow Triggers

- Pull requests to `main` or `develop` branches
- Direct pushes to `main` or `develop` branches

### Quality Gates

- All tests must pass
- Code coverage must meet minimum thresholds
- No security vulnerabilities detected
- Code style guidelines enforced

## 📱 Mobile Responsiveness

D'Agri Talk is designed with mobile-first principles, considering that most Liberian farmers access the internet via smartphones:

- **Responsive Design**: Adapts to all screen sizes
- **Touch-Friendly**: Large buttons and touch targets
- **Offline Capability**: Progressive Web App features
- **Low Bandwidth**: Optimized for slower internet connections
- **Local Language Support**: UI elements in local languages

## 🌍 Impact & Future Development

### Current Impact

- **Knowledge Preservation**: Platform for documenting traditional farming practices
- **Market Access**: Direct farmer-to-buyer connections
- **Community Building**: Forums for agricultural knowledge sharing
- **Technology Adoption**: Introducing digital tools to rural farming communities

### Future Enhancements

- **Weather Integration**: Local weather forecasts and alerts
- **Mobile App**: Native iOS and Android applications
- **Payment Integration**: Mobile money integration for transactions
- **AI Features**: Crop disease identification using machine learning
- **Multilingual Expansion**: Support for all 16 Liberian languages
- **Offline Functionality**: Sync capabilities for areas with poor connectivity

## 🤝 Contributing

We welcome contributions to D'Agri Talk! Please follow these guidelines:

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`npm test` and `pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Standards

- Follow existing code style and conventions
- Write comprehensive tests for new features
- Update documentation for any API changes
- Ensure all CI checks pass

### Issue Reporting

- Use GitHub Issues for bug reports and feature requests
- Provide detailed descriptions and reproduction steps
- Include relevant system information and error messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

**Willie B. Daniels** - *Project Developer*

- GitHub: [@Williedaniels](https://github.com/Williedaniels)
- Email: <w.daniels@alustudent.com>

## 🙏 Acknowledgments

- **Liberian Farmers**: For inspiring this platform and sharing their knowledge
- **Agricultural Extension Research**: For providing technical guidance
- **Open Source Community**: For the tools and frameworks that made this possible
- **GitHub Education**: For providing student benefits and development tools

## 📞 Support

For support, email <w.daniels@alustudent.com> or create an issue in the GitHub repository.

---

**D'Agri Talk** - *Connecting farmers, preserving wisdom, building communities* 🌾
