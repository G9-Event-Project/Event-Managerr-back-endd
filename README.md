# Event-Management-Back-end
Community Event Planner
Project Overview
The Community Event Planner is a full-stack web application designed to connect local communities by enabling users to create, manage, and participate in events such as book clubs, clean-up drives, or workshops. Users can register, log in, create events, comment on events, and search for events by keyword. The application addresses the real-world problem of disconnected communities by providing a centralized platform for event organization and engagement.
This project is built as part of a Phase 4 full-stack development curriculum, showcasing skills in Flask (backend), React (frontend, planned), and secure authentication practices.
Features

User Management:
Register with a username, email, and password (hashed with Flask-Bcrypt).
Log in to receive JWT access and refresh tokens.
View and update profile details (e.g., email).


Event Management (Full CRUD):
Create events with title, date, description, and location.
View a list of user-created events.
Update or delete events (restricted to the creator).


Comment System:
Add comments to events.
View comments for a specific event.
Delete comments (restricted to the author).


Search Functionality:
Search events by keywords in title, description, or location.


Security:
Passwords are hashed and salted using Flask-Bcrypt.
JWT authentication for protected routes.
Rate limiting on registration and login endpoints.


