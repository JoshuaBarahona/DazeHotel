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
    # Esto es para meter un admin por defecto en la base de datos para testear el login de empleado
    # correo: adiliamoreno@gmail.com  contraseña: admin
    # cur.execute("INSERT INTO empleados(nombre, area_id, correo, telefono, cedula, hash) VALUES ('admin', 1, 'adiliamoreno@gmail.com', 12345678, 12345678, ?)", (generate_password_hash("admin"),))
    # conn.commit()

    # cur.execute("INSERT INTO categorias(nombre, descripcion) VALUES('Estandar', 'Habitaciones sencillas con lo básico')")
    # conn.commit()

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
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
            if user and check_password_hash(user[5], password):
                # Guarda el id del usuario en la sesión
                session["user_id"] = user[0]
                
                return redirect('/')
            else:
                return render_template("index .html", message="Usuario no encontrado.")
            
        elif user_type == "Iniciar como empleado":
            cur.execute("SELECT * FROM empleados WHERE correo = ?", (correo,))
            user = cur.fetchone()
            if user and check_password_hash(user[6], password):
                session["employee_id"] = user[0]
                return redirect('/admin')
            else:
                return render_template("index .html", message="Usuario no encontrado.")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("Register.html")
    else:
        name = request.form.get("Nombre")
        correo = request.form.get("Correo electrónico")
        password = request.form.get("Password")
        password2 = request.form.get("ConfirmPassword")
        cedula = request.form.get("cedula")
        telefono = request.form.get("telefono")

        if password != password2:
            return render_template("Register.html", message="Las contraseñas no coinciden")
        if not name or not correo or not password:
            return render_template("Register.html", message="Campos incompletos.")
        
        # Encriptar la contraseña antes de guardarla
        hashed_password = generate_password_hash(password)
        cur.execute(
            "INSERT INTO huesped(nombre, correo, cedula, telefono, hash) VALUES (?, ?, ?, ?, ?)",
            (name, correo, cedula, telefono, hashed_password)
        )
        conn.commit()
        return redirect('/')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/aboutus")
def aboutus():
    return render_template("acercade.html")

@app.route("/habitaciones", methods = ["POST", "GET"])
def habitaciones():
    if request.method == "GET":
        return render_template("habitaciones.html")
    # elif request.method == "POST":
    #     # esta ruta no deberia recibir post
    #     cur.execute("SELECT * FROM categoria WHERE nombre = ?", (categoria))
    #     categoria = cur.fetchall()
    #     return render_template("habitaciones.html")
    
@app.route("/habitaciones/<int:categoria_id>", methods = ["GET", "POST"])
def habitacionesdetalles(categoria_id):
    if request.method == "GET":
        # Muestra detalles de habitaciones de una categoría específica.
        cur.execute("SELECT * FROM habitacion WHERE categoria_id = ?", (categoria_id,))
        habitaciones = cur.fetchall()
        return render_template("habitaciones.html", categoria_id=categoria_id, habitaciones=habitaciones)
    elif request.method == "POST":
        # Procesa el formulario para agregar una habitación.
        detalle = request.form.get("Detalle")
        cur.execute("INSERT INTO habitacion(detalle) VALUES (?)", (detalle))
        conn.commit()
        return redirect("/")
    
@app.route("/admin", methods = ["GET", "POST"])
def admin():
    print(request.method)
    if request.method == "GET":
        cur.execute("SELECT * FROM reserva")
        cur.fetchall()
        cur.execute("SELECT * FROM huesped")
        cur.fetchall()
        cur.execute("SELECT * FROM habitacion")
        cur.fetchall()
        return render_template("admin.html")
    else:
        action_type = request.form.get("action_type")
        if action_type == "Nueva reserva":
            Cliente = request.form.get("Cliente")
            Habitacion = request.form.get("Habitacion")
            Fecha = request.form.get("Fecha")
            Costo = request.get.form("Costo")
            huesped_id = request.get.form("id del huesped")
            cur.execute("INSERT * INTO reserva (id, date, costo, huesped_id) VALUES (?, ?, ?, ?)", Cliente, Habitacion, Fecha, Costo, huesped_id)#insert
            conn.commit()
        elif action_type == "Crear habitación":
            try:
                numero = request.form.get("numero")
                piso = request.form.get("piso")
                categoria_map = {"Estandar": 1, "Deluxe": 2}
                categoria_id = categoria_map.get(request.form.get("categoria"))
                cantmaxhuespedes = int(request.form.get("capacidad"))
                disponibilidad = int(request.form.get("disponibilidad"))
                costonoche = float(request.form.get("costo"))
                detalle = request.form.get("detalle")

                # Validar datos antes de insertar
                if not all([numero, piso, categoria_id, cantmaxhuespedes, disponibilidad, costonoche, detalle]):
                    return "Error: Datos incompletos", 400

                # Inserción en la base de datos
                cur.execute(
                    """
                    INSERT INTO habitacion (numero, piso, cant_max_huespedes, disponibilidad, costo_dia, categoria_id, detalle)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (numero, piso, cantmaxhuespedes, disponibilidad, costonoche, categoria_id, detalle)
                )
                conn.commit()
                return "Habitación creada exitosamente", 200
            except Exception as e:
                conn.rollback()
                print("Error al crear habitación:", e)
                return "Error interno del servidor", 500

        elif action_type == "Eliminar":
            habitacion_id = request.form.get("HabitacionID")
            cur.execute("DELETE FROM habitacion WHERE id = ?", (habitacion_id,))
            conn.commit()
            
        elif action_type == "Editar":
            habitacion_id = request.form.get("HabitacionID")
            nuevo_numero = request.form.get("NuevoNumero")
            nueva_disponibilidad = request.form.get("NuevaDisponibilidad") == "True"
            nuevo_costo = request.form.get("NuevoCosto")
            cur.execute(
                "UPDATE habitacion SET numero = ?, disponibilidad = ?, costo_dia = ? WHERE id = ?",
                (nuevo_numero, nueva_disponibilidad, nuevo_costo, habitacion_id)
            )
            conn.commit()
    
@app.route("/cart")
def carrito():
    if "user_id" not in session:
        return redirect("/login")
    
    huesped_id = session["user_id"]
    return render_template("carrito.html")

@app.route("/cart/add", methods=["POST"])
def agregar_carrito():
    if "user_id" not in session:
        return redirect("/login")
    
    huesped_id = session["user_id"]
    habitacion_id = request.form.get("habitacion_id")
    paquete_id = request.form.get("paquete_id")
    cantidad = request.form.get("cantidad", 1)
    
    # Agregar al carrito
    cur.execute('''
        INSERT INTO carrito (huesped_id, habitacion_id, paquete_id, cantidad)
        VALUES (?, ?, ?, ?)
    ''', (huesped_id, habitacion_id, paquete_id, cantidad))
    conn.commit()
    #ola tia adilia
    return redirect("/cart")
#llamen a Dios
if __name__ == "__main__":
    app.run(debug=True)
