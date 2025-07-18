from flask import Flask, render_template, request, redirect, session
from database import get_all_numbers, get_all_chats
import os

app = Flask(__name__)
app.secret_key = os.getenv("ADMIN_SECRET", "supersecret")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "Rivagpt565")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "billgatesriva")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/dashboard")
        return "Invalid credentials", 401
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/")
    numbers = get_all_numbers()
    chats = get_all_chats()
    return render_template("dashboard.html", numbers=numbers, chats=chats)

app.run(host="0.0.0.0", port=8000)