# Full-Stack User Management System

A high-performance, containerized full-stack web application for user management with secure authentication and CRUD functionality. Built with Next.js (React), Flask, and PostgreSQL.


## Features

- 🔐 **Secure Authentication**: JWT-based authentication system
- 👥 **User Management**: Complete CRUD operations for user accounts
- 🔄 **RESTful API**: Well-structured API with Flask
- 🎨 **Modern UI**: Responsive design built with Next.js
- 🐳 **Containerized**: Easy deployment with Docker
- 🗄️ **Persistent Storage**: PostgreSQL database

## Tech Stack

- **Frontend**: Next.js (React)
- **Backend**: Flask
- **Database**: PostgreSQL
- **Containerization**: Docker

## Prerequisites

- Docker and Docker Compose
- Git

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/sdave0/Fullstack_CRUD.git
cd Fullstack_CRUD
```

### 2. Configure Environment Variables

#### Frontend (`frontend/.env`):
```ini
NEXT_PUBLIC_API_URL=http://localhost:4000
```

#### Backend (`backend/.env`):
```ini
DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
JWT_SECRET_KEY=your-secure-jwt-secret-key
```

### 3. Build & Start Containers
```bash
docker compose up --build
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:4000

## Creating an Admin User

Run the application once, then execute:

```bash
docker exec -it <backend_container_name> flask create-admin
```

Alternatively, modify `app.py` to enable automatic admin creation.

## Project Structure

```
Fullstack_CRUD/
│── frontend/           # Next.js frontend
│   ├── src/components/ # UI components
│   ├── src/pages/      # App pages
│── backend/            # Flask backend
│   ├── app.py          # Main app logic
│   ├── models.py       # Database models
│   ├── auth_routes.py  # Authentication
│   ├── user_routes.py  # User management
│── docker-compose.yml  # Container setup
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user information

### User Management
- `GET /api/users` - List all users (admin only)
- `GET /api/users/:id` - Get user details
- `PUT /api/users/:id` - Update user
- `DELETE /api/users/:id` - Delete user

## Environment Variables

### Frontend (`frontend/.env`):
- `NEXT_PUBLIC_API_URL`: Backend API endpoint

### Backend (`backend/.env`):
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT signing

## Development

### Running Frontend Separately
```bash
cd frontend
npm install
npm run dev
```

### Running Backend Separately
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run --port=4000
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contact

Project Link: [https://github.com/sdave0/Fullstack_CRUD](https://github.com/sdave0/Fullstack_CRUD)
