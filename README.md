# Smart-Booking-System-API-Backend
Smart Booking System is an asynchronous FastAPI backend that manages users, properties, bookings, and payments. It includes JWT authentication, SQL + NoSQL support, clean architecture, and is ready for integrating advanced service features.
This project is a clean and extensible Basic E-commerce API built with FastAPI, designed as a backend foundation ready for future advanced service implementations.

It includes:
- User authentication with JWT tokens
- Organized project structure using routers, services, and CRUD modules
- Dependency injection for database and authentication flow
- Placeholder service modules ready for business logic expansion
- Deployment-ready configuration (Render, environment variables, etc.)

Features:
• User Authentication: Login, password hashing, and JWT-based authentication.
• Project Architecture: routers for request handling, crud for database operations, services for advanced logic.
• Database Ready: SQLAlchemy models and async sessions.
• Extensible: Includes empty service layers for real-world features.

Project Structure:

ecommerce_api/
  app/
    auth/
      jwt_handler.py
      hashing.py
      security.py
      auth_router.py
    crud/
    routers/
    services/
      booking_services.py
      payment_services.py
      notifications_service.py
    models/
    database.py
    main.py
  requirements.txt
  README.md
  render.yaml
  start.sh

Requirements:
- Python 3.10+
- FastAPI
- SQLAlchemy
- Uvicorn
- python-dotenv
- jose
- passlib

Install dependencies:
pip install -r requirements.txt

How to Run:
1. Create a virtual environment:
python -m venv venv
source venv/bin/activate  (Mac/Linux)
venv\Scripts\activate   (Windows)

2. Run the API:
uvicorn app.main:app --reload

3. Open documentation:
Swagger UI → http://localhost:8000/docs
ReDoc → http://localhost:8000/redoc

Authentication Flow:
1. User sends email and password to /auth/login
2. Server validates credentials using hashing
3. Server generates a JWT token with {"sub": user_id}
4. Client stores token and sends it in Authorization: Bearer <token>
5. Protected routes use get_current_user to verify it.

Advanced Services:
The project includes service modules prepared for:
- Payments
- Bookings
- Notifications

Deployment:
This project includes render.yaml and start.sh for deployment to Render.

GitHub Upload Instructions:
git init
git remote add origin https://github.com/your-username/ecommerce_api.git
git add .
git commit -m "Initial commit"
git push -u origin main

Author:
Backend Developer — Python & FastAPI
Project designed as a production-ready e-commerce microservice base.

