from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from bot.chatbot import FlightBot
from bot.storage import load_bookings
import json
import os

USERS_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

app = Flask(__name__)
app.secret_key = "final_year_project_secret"
bot = FlightBot()

@app.route("/login", methods=["GET", "POST"])
def login():
    users = load_users()

    if request.method == "POST":
        username = request.form["username"].strip().lower()
        password = request.form["password"]

        if username in users:
            if users[username]["password"] != password:
                return render_template("login.html", error="Invalid password")
        else:
            users[username] = {"password": password}
            save_users(users)

        session["user"] = username
        return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    bot.current_user = session.get("user")
    reply = bot.respond(user_message, session.get("user"))
    return jsonify({"reply": reply})

@app.route("/bookings")
def my_bookings():
    if "user" not in session:
        return redirect(url_for("login"))

    all_bookings = load_bookings()
    user = session["user"]

    user_bookings = []
    for pnr, b in all_bookings.items():
        if b.get("username") == user:
            user_bookings.append(b)

    return render_template(
        "bookings.html",
        bookings=user_bookings,
        user=user
    )


if __name__ == "__main__":
    app.run(debug=True)
