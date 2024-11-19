import sqlite3
from flask import Flask, render_template, request, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

conn = sqlite3.connect('dazeHotel.db', check_same_thread=False)
cur = conn.cursor()

app = Flask(__name__)

# Configuración para Flask-Session
app.config["SESSION_TYPE"] = "filesystem"  # Almacenamiento en el sistema de archivos
app.config["SESSION_PERMANENT"] = False    # La sesión no será permanente
Session(app)  # Inicializa Flask-Session

# Clave secreta para la sesión
app.secret_key = "una_clave_secreta_super_segura"

@app.route("/")
def index():
    return render_template("index .html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("index .html")
    else:
        correo = request.form.get("correo")
        password = request.form.get("password")
        user_type = request.form.get("user_type")  #Obtén el valor del rol seleccionado para iniciar sesión
        if not correo or not password:
            return render_template("index .html", message="Campos incompletos.")
        
         #Manejo de inicio de sesión para los diferentes roles
        if user_type == "Iniciar como cliente":
            # Los datos se recuperan en forma de tupla
            cur.execute("SELECT * FROM huesped WHERE correo = ?", (correo,))
            user = cur.fetchone()
            if user and check_password_hash(user[1], password):
                # Guarda el id del usuario en la sesión
                session["user_id"] = user[0]
                return redirect('/')
            else:
                return render_template("index .html", message="Usuario no encontrado.")
            
        elif user_type == "Iniciar como empleado":
            cur.execute("SELECT * FROM empleados WHERE correo = ?", (correo,))
            user = cur.fetchone()
            if user and check_password_hash(user[3], password):
                session["employee_id"] = user[0]
                return redirect('/')
            else:
                return render_template("index .html", message="Usuario no encontrado.")
        
        

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("Nombre")
        correo = request.form.get("Correo electrónico")
        password = request.form.get("Password")
        password2 = request.form.get("ConfirmPassword")
        cedula = request.form.get("cedula")
        telefono = request.form.get("telefono")

        if password != password2:
            return render_template("register.html", message="Las contraseñas no coinciden")
        if not name or not correo or not password:
            return render_template("register.html", message="Campos incompletos.")
        
        # Encriptar la contraseña antes de guardarla
        hashed_password = generate_password_hash(password)
        cur.execute(
            "INSERT INTO huesped(nombre, correo, cedula, telefono, hash) VALUES (?, ?, ?, ?, ?)",
            (name, correo, cedula, telefono, hashed_password)
        )
        conn.commit()
        return redirect('/')

@app.route("/employeelogin", methods=["POST", "GET"])
def employeelogin():
    session.clear()
    if request.method == "GET":
        return render_template("employeelogin.html")
    else:
        codigo = request.form.get("Código empleado")
        correo = request.form.get("Correo")
        password = request.form.get("Contraseña")
        if not codigo or not correo or not password:
            return render_template("employeelogin.html", message="Campos incompletos.")
        cur.execute("SELECT * FROM empleados WHERE id = ? AND correo = ?", (codigo, correo))
        user = cur.fetchone()
        if user and check_password_hash(user[3], password):  # Asegúrate que `user[3]` es el hash
            session["employee_id"] = user[0]
            return redirect('/')
        else:
            return render_template("employeelogin.html", message="Campos incorrectos.")

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

@app.route("/habitaciones")
def habitaciones():
    return render_template("habitaciones.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

if __name__ == "__main__":
    app.run(debug=True)
