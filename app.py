import sqlite3
from flask import Flask, render_template, request, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash

conn = sqlite3.connect('dazeHotel.db')

cur = conn.cursor()

app = Flask(__name__)

@app.route("/")
def index():

    return render_template("index .html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        correo = request.form.get("correo")
        password = request.form.get("password")
        if not correo or not password:
            return render_template("login.html", message="Campos incompletos.")
        cur.execute("SELECT * FROM huesped WHERE correo = ? AND hash = ?", (correo, password))
        user = cur.fetchone()
        
        if user:
             return redirect('/')
        else:
             return render_template("login.html", message="Usuario no encontrado.")

    return redirect('/')

@app.route("/register", methods = ["GET", "POST"])
def register():
     if request.method == "GET":

          return render_template("register.html")
     
     else:
          name = request.form.get("Nombre")
          correo = request.form.get("Correo electrónico")
          password = generate_password_hash("Password")
          password2 = generate_password_hash("Confirm Password")

          if password != password2:
               return render_template("register.html", message = "Las contraseñas no coinciden")
          cur.execute("INSERT * INTO huesped (nombre, correo, password) VALUES (?, ?, ?)", (name, correo, password))
          conn.commit()
          return redirect('/')

@app.route("/employeelogin", methods = ["POST", "GET"])
def employeelogin():
     session.clear()
     if request.method == "GET":
          return render_template("employeelogin.html")
     else:
          codigo = request.form.get("Código empleado")
          correo = request.form.get("Correo")
          password = request.form.get("Contraseña")
          if not codigo or not correo or not password:
               return render_template("/employeelogin", message = "Campos incompletos.")
          cur.execute("SELECT * FROM empleados WHERE id  = ? AND correo = ? AND hash = ?", (codigo, correo, password))
          user = cur.fetchone()
          if user:
               return redirect('/')
          else:
               return render_template("employeelogin.html", message = "Campos incorrectos.")
          
     return redirect('/')
     
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
