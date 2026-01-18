# Practice Question App

A full-stack web application for simplifying the coding practice process.

## Repository Structure

```
├── backend/                 # FastAPI backend server
│   ├── models/             # Data models (Question, User, UserAttempt)
│   ├── schemas/            # Pydantic schemas for API validation
│   ├── services/           # Business logic and database services
│   ├── routers/            # API route handlers
│   ├── main.py             # FastAPI application entry point
│   └── requirements.txt    # Python dependencies
├── frontend/               # Static web frontend
│   ├── index.html          # Main HTML page
│   ├── index.css           # Responsive CSS styles
│   └── index.js            # JavaScript functionality
├── nginx/                  # Nginx configuration
│   └── nginx.conf          # Server blocks for frontend/backend
└── README.md               # This file
```

## Features

- **Question Practice**: Click to start leetcode practice sessions
- **Status Tracking**: Mark attempts as "Completed" or "Attempted"
- **User Management**: Persistent user IDs stored in localStorage
- **Responsive Design**: Mobile-friendly interface
- **CSV Storage**: Self-hosting friendly

## TODO Features
- **Smart Question Selection**: Algorithmic selection of questions
- **Question Preferences**: Allow users to set their own preferences for question selection algorithm

## Setup & Running

### Prerequisites

- Python 3.8+
- Modern web browser

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate venv:
   ```bash
   .\.venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Serve the static files using any web server. For example:
   ```bash
   # Using Python's built-in server
   python -m http.server 3000
   
   # Or using Node.js serve
   npx serve -p 3000
   ```

   The frontend will be available at `http://localhost:3000`

### Using Nginx (Optional)

1. Install nginx
2. Copy the configuration:
   ```bash
   cp nginx/nginx.conf /etc/nginx/sites-available/practice-app
   ```
3. Enable the site and reload nginx

## API Endpoints

- `GET /question` - Get a practice question and log attempt
- `POST /completed` - Update attempt status

Both endpoints require the `X-User-ID` header.

## Data Storage

Currently uses CSV files for data persistence:
- `questions.csv` - Practice questions
- `users.csv` - User records  
- `userAttempts.csv` - Attempt tracking

The service layer is designed for easy migration to a relational database later.

## Development

- Backend uses FastAPI with CORS enabled for development
- Frontend uses vanilla JavaScript with responsive CSS
- CSV database service provides full CRUD operations
- Modular architecture supports easy feature additions