Community Event Planner

Project Overview
The Community Event Planner is a full-stack web application designed to connect local communities by enabling users to create, manage, and participate in events such as book clubs, clean-up drives, or workshops. Users can register, log in, create events, comment on events, and search for events by keyword. The application addresses the real-world problem of disconnected communities by providing a centralized platform for event organization and engagement.

This project showcases skills in Flask (backend) and secure authentication practices.

Features

User Management:

* Register with a username, email, and password (hashed with Flask-Bcrypt).
* Log in to receive JWT access and refresh tokens.
* View and update profile details (e.g., email).

Event Management (Full CRUD):

* Create events with title, date, description, and location.
* View a list of user-created events.
* Update or delete events (restricted to the creator).

Comment System:

* Add comments to events.
* View comments for a specific event.
* Delete comments (restricted to the author).

Search Functionality:

* Search events by keywords in title, description, or location.

Security:

* Passwords are hashed and salted using Flask-Bcrypt.
* JWT authentication for protected routes.
* Rate limiting on registration and login endpoints.

Technologies Used

Backend:

* Flask: Web framework for API development.
* Flask-SQLAlchemy: ORM for database management.
* Flask-JWT-Extended: JWT authentication.
* Flask-Bcrypt: Secure password hashing.
* Flask-Limiter: Rate limiting for security.
* Flask-CORS: Cross-origin support for frontend integration.
* Python-dotenv: Environment variable management.

Tools:

* SQLite (development), PostgreSQL (production): Database.
* Git/GitHub: Version control.
* Render: Backend deployment.
* Pytest: Backend testing.

File Structure
backend/
├── app/
│   ├── **init**.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── events.py
│   │   ├── comments.py
│   │   └── profile.py
│   ├── utils/
│   │   └── jwt.py
├── tests/
│   └── test\_auth.py
│   └── test\_events.py
├── config.py
├── app.py
├── requirements.txt
└── .env

Setup Instructions

Prerequisites:

* Python 3.8+
* Git
* PostgreSQL (for production)

Backend Setup:

1. Clone the repository:
   git clone [https://github.com/your-repo/community-event-planner.git](https://github.com/your-repo/community-event-planner.git)
   cd community-event-planner/backend

2. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Create a .env file in the backend directory:
   JWT\_SECRET\_KEY=your-secret-key  # Generate with `openssl rand -hex 32`
   DATABASE\_URI=sqlite:///events.db  # Or postgresql://user\:pass\@localhost/dbname for production

5. Run the Flask app:
   python app.py

The API will be available at [http://localhost:5000/api](http://localhost:5000/api).

Running Tests:

1. Install pytest:
   pip install pytest

2. Run tests:
   pytest tests/

API Documentation

User Management

POST /api/register
Request: { "username": "string", "email": "string", "password": "string" }
Response: 201 { "message": "User registered" } or 400 { "error": "Username exists" }

POST /api/login
Request: { "username": "string", "password": "string" }
Response: 200 { "access\_token": "string", "refresh\_token": "string" } or 401 { "error": "Invalid credentials" }

POST /api/refresh (Protected)
Response: 200 { "access\_token": "string" }

GET /api/profile (Protected)
Response: 200 { "username": "string", "email": "string" }

PUT /api/profile (Protected)
Request: { "email": "string" }
Response: 200 { "message": "Profile updated" }

Event Management

POST /api/events (Protected)
Request: { "title": "string", "description": "string", "date": "YYYY-MM-DD", "location": "string" }
Response: 201 { "message": "Event created" } or 400 { "error": "Missing title or date" }

GET /api/events (Protected)
Response: 200 \[{ "id": int, "title": "string", "description": "string", "date": "string", "location": "string", "user\_id": int }]

PUT /api/events/\:id (Protected)
Request: { "title": "string", "description": "string", "date": "YYYY-MM-DD", "location": "string" }
Response: 200 { "message": "Event updated" } or 403 { "error": "Unauthorized" }

DELETE /api/events/\:id (Protected)
Response: 200 { "message": "Event deleted" } or 403 { "error": "Unauthorized" }

Comment System

POST /api/comments (Protected)
Request: { "content": "string", "event\_id": int }
Response: 201 { "message": "Comment added" }

GET /api/comments/\:event\_id
Response: 200 \[{ "id": int, "content": "string", "user\_id": int }]

DELETE /api/comments/\:id (Protected)
Response: 200 { "message": "Comment deleted" } or 403 { "error": "Unauthorized" }

Search

GET /api/search?q=keyword
Response: 200 \[{ "id": int, "title": "string", "description": "string", "date": "string", "location": "string" }]

Deployment



Development Notes

Database: SQLite is used for development; switch to PostgreSQL for production.
Security: Passwords are hashed with Flask-Bcrypt, and JWT tokens secure protected routes.
Testing: Unit tests cover authentication and event management.
Frontend Integration: Use fetch or axios to connect to the API, with Formik for form validation.
