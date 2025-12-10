# AI-Native Textbook Quickstart Guide

Welcome to the AI-Native Textbook for Physical AI & Humanoid Robotics! This guide will help you get the project up and running quickly.

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database
- Qdrant vector database
- Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hackathon-1(book)
```

### 2. Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL and other configuration
```

### 3. Frontend Setup
```bash
cd website

# Install dependencies
npm install
```

### 4. Database Configuration
```bash
# Run database migrations
cd backend
alembic upgrade head
```

### 5. Run the Applications

**Backend (in one terminal):**
```bash
cd backend
uvicorn main:app --reload
```

**Frontend (in another terminal):**
```bash
cd website
npm start
```

## Key Features

### Step-by-Step Learning
- Sequential task completion with validation
- Progress tracking with visual indicators
- Personalized learning paths based on user background

### Progress Tracking
- Chapter and step completion tracking
- Dashboard with progress visualization
- Resume functionality to continue where you left off

### Personalization
- User profiles with background information
- Adaptive content delivery
- Learning path customization

## API Endpoints

Once running, API documentation is available at:
- `http://localhost:8000/docs` - Interactive API documentation
- `http://localhost:8000/redoc` - Alternative API documentation

Key endpoints:
- `GET /api/v1/chapters` - Get all available chapters
- `GET /api/v1/steps/chapter/{chapter_id}` - Get steps for a chapter
- `GET /api/v1/progress` - Get user progress
- `POST /api/v1/progress/steps/{step_id}/complete` - Mark step as complete

## Frontend Navigation

The UI is built with Docusaurus and includes:
- Chapter listing pages
- Step-by-step learning interface
- Progress dashboard
- User profile management
- Learning path selection

## Development

### Adding New Content
1. Create chapters and steps through the API or database
2. Frontend will automatically adapt to new content structure
3. Add appropriate completion criteria for each step type

### Extending Functionality
- Backend services are located in `backend/src/services/`
- API endpoints are defined in `backend/src/api/v1/`
- Frontend components are in `website/src/components/`

## Troubleshooting

### Common Issues
- **Database migrations failing**: Ensure PostgreSQL is running and `DATABASE_URL` is correctly set
- **Frontend can't connect to backend**: Check that both servers are running and CORS is configured
- **Authentication issues**: Verify Better-Auth is properly configured

### Environment Variables
Ensure the following are set in your `.env` file:
- `DATABASE_URL` - PostgreSQL connection string
- `QDRANT_URL` - Qdrant vector database URL
- `SECRET_KEY` - JWT secret key (use a strong, random value for production)

## Next Steps

1. Add your educational content to the system
2. Customize the UI to match your branding
3. Implement specific validation logic for your step types
4. Consider adding assessment capabilities
5. Deploy to production

For detailed documentation on each feature, see the `/docs` directories in both backend and website folders.