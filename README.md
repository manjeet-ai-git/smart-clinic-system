🏥 Smart Clinic Management System
A simple full-stack web application built using FastAPI, MySQL, and Streamlit.
This project helps manage patient records with secure login for doctors.

🚀 Project Overview
Smart Clinic Management System is a beginner-friendly project that demonstrates how to build a full-stack application.
It allows doctors to:
Register and login securely
Add and manage patient details
Perform basic CRUD operations
The system uses JWT authentication for secure access

✨ Features
👤 Authentication
Doctor Registration
Doctor Login
JWT Token Authentication

🏥 Patient Management
Add Patient
View Patients
Update Patient Details
Delete Patient
Search Patient

🛠️ Tech Stack
Backend
FastAPI
Python
Frontend
Streamlit
Database
MySQL
Authentication
JWT
bcrypt

📁 Project Structure
Smart-Clinic-System/
│
├── backend/
│   └── main.py
│
├── frontend/
│   └── streamlit_app.py
│
├── database/
│   └── schema.sql
│
└── README.md

⚙️ Setup Instructions
1️⃣ Clone the project
git clone https://github.com/manjeet-ai-git/smart-clinic-system.git
cd smart-clinic-system
2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Setup Database
Open MySQL
Run schema.sql file

4️⃣ Run Backend
uvicorn backend.main:app --reload

5️⃣ Run Frontend
streamlit run frontend/streamlit_app.py

Authentication Flow
Doctor registers using /register
Doctor logs in using /login
JWT token is generated
Token is used to access patient APIs

📊 API Endpoints
Authentication
POST /register
POST /login
Patients
POST /patients
GET /patients
GET /patients/{id}
PUT /patients/{id}
DELETE /patients/{id}

🎯 Learning Outcomes

This project helps you learn:

REST API development with FastAPI
JWT authentication
MySQL database integration
Full-stack application structure
Basic frontend using Streamlit

👨‍💻 Author

Name: Manjeet Singh Shekhawat
Role: AI/ML & Backend Developer Intern Aspirant
Project: Smart Clinic Management System

Future Improvements
Add appointment system
Add role-based access (Admin/Doctor/Patient)
Deploy project on cloud
Add better UI design
Note
This is a beginner-level project made for learning full-stack development and backend concepts.
