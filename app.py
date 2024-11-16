import sqlite3
from flask import Flask, render_template, request, session, redirect
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
        password = generate_password_hash("password")
        if not correo or not password:
            return render_template("login.html", error="Campos incompletos.")
        cur.execute("SELECT * FROM huesped WHERE correo = ? AND hash = ?", (correo, password))
        user = cur.fetchone()
        conn.close()

    if user and check_password_hash(user["hash"], password):
            session["correo"] = user["correo"]
            return render_template("index.html", user=user)
    else:
        return render_template("login.html", error="Correo o contraseña incorrectos.")

    return redirect("/")

@app.route("/register", methods = ["GET", "POST"])
def register():
     
     if request.method == "POST":
          nombre = request.form.get("Nombre")
          apellido = request.form.get("Apellido")
          telefono = request.form.get("Numero telefónico")
          correo = request.form.get("correo")
          password = generate_password_hash("password")

          if not nombre or not apellido or not telefono or not correo or not password:
               return render_template("/register.html", error = "Campos obligatorios incompletos.")
          cur.execute("INSERT INTO huesped WHERE nombre = ? AND apellido = ? AND telefono = ? AND correo = ? AND hash = ?" (nombre, apellido, telefono, correo, password))
          user = cur.fetchone()
          conn.close()
     
     return redirect("/")

@app.route("/employeelogin", methods = ["POST", "GET"])
def employeelogin():
     if request.method == "POST":
        staffcode = request.form.get("Codigo de Staff")
        correo = request.form.get("Correo")
        password = generate_password_hash("Contraseña")

        if not staffcode or not correo or not password:
             return render_template("employeelogin", error = "Campos obligatorios incompletos.")
        cur.execute("SELECT * FROM empleados where id = ? AND correo = ? AND hash = ?" (staffcode, correo, password))
        user = cur.fetchone()
        conn.close()
        
        return redirect("/")
     
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/aboutus")
def aboutus():
     return render_template("acercade.html")

@app.route("/galery")
def galery():
     return render_template("galery.html")

app.route("/habitaciones")
def habitaciones():
     return render_template("habitaciones.html")

@app.route("/contacto")
def contacto():
     
     return render_template("contacto.html")
