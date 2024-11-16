import sqlite3
from flask import Flask, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

conn = sqlite3.connect('dazeHotel.db')

cur = conn.cursor()

app = Flask(__name__)

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo")
        password = request.form.get("password")
        if not correo or not password:
            return render_template("login.html", error="Campos incompletos.")
        cur.execute("SELECT * FROM huesped WHERE correo = ? AND hash = ?", (correo, password))
        user = cur.fetchone()
        conn.close()

    if user:
            session["correo"] = user["correo"]
            session["password"] = user["password"]
            return render_template("index.html", user=user)
    else:
        return render_template("login.html", error="Correo o contraseña incorrectos.")

    return render_template("login.html")