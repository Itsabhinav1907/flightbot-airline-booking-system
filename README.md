✅ EXACT CONTENT FOR README.md
# ✈️ FlightBot – Airline Booking System

FlightBot is a state-driven airline booking chatbot developed as a **final-year project**.  
It simulates real-world airline operations such as **ticket booking, cancellation, payment handling, and refunds**, with a **web-based interface built using Flask**.

The system supports **multiple users**, ensures **secure user-level data isolation**, and follows clean software engineering practices.

---

## 🎯 Objectives

- Build an interactive airline booking chatbot
- Implement complete booking and cancellation lifecycle
- Simulate payment and refund workflows
- Support multiple users with authentication
- Provide a web-based interface using Flask
- Ensure user-specific data isolation

---

## 🧠 Features

### ✈️ Booking
- One-way flight booking
- Route, date, passengers, and class selection
- Automatic PNR generation
- Persistent booking storage

### ❌ Cancellation & Refund
- Cancel tickets using PNR
- Refund calculation based on travel date
- Prevention of double cancellation
- Refunds allowed only for paid bookings

### 💳 Payment Simulation
- Simulated payment system
- Explicit payment status tracking
- Airline-style refund rules

### 👤 User Authentication
- Login and registration system
- Session-based authentication
- Each user can access only their own bookings

### 📄 My Bookings Dashboard
- View booking history
- Shows CONFIRMED and CANCELLED bookings
- User-specific booking visibility

### 🌐 Web Interface
- Flask backend
- Chat-style UI
- Separate CSS styling
- Simple and clean user experience

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|-----------|
| Backend | Python |
| Web Framework | Flask |
| Frontend | HTML, CSS |
| Storage | JSON |
| Authentication | Flask Sessions |
| Architecture | State Machine |

---

## 🧩 System Architecture



User (Browser)
|
v
Flask Web Application
|
v
FlightBot (State Machine)
|
v
JSON Storage (Users & Bookings)


---

## 🔄 Application Flow

1. User logs in
2. Chooses BOOK or CANCEL
3. Provides trip details
4. Payment is simulated
5. Booking is confirmed with PNR
6. User can view or cancel bookings later

---

## 🔐 Security & Data Isolation

- Each booking is linked to a specific user
- Users cannot view or cancel other users’ bookings
- User context is passed per request (no shared state)

---

## ▶️ How to Run the Project

### 1️⃣ Install Dependencies
```bash
pip install flask

2️⃣ Run the Application
python web.py

3️⃣ Open in Browser
http://127.0.0.1:5000

📁 Project Structure
flightbot-airline-booking-system/
├── web.py
├── bot/
│   ├── chatbot.py
│   ├── states.py
│   ├── storage.py
│   └── utils.py
├── data/
│   ├── bookings.json
│   └── users.json
├── templates/
│   ├── index.html
│   ├── login.html
│   └── bookings.html
├── static/
│   └── style.css

🚀 Future Enhancements

NLP-based intent detection

Round-trip bookings

Database integration (SQLite / MySQL)

Cloud deployment

Admin dashboard

🎓 Academic Relevance

This project demonstrates:

State-based system design

Multi-user session handling

Secure data isolation

Realistic business logic implementation

Full-stack development skills

👨‍💻 Author

Abhinav Singh
B.Tech – Computer Science (AI & ML)
Final-Year Project
