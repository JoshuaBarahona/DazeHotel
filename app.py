import sqlite3
conn = sqlite3.connect('dazeHotel.db')

cur = conn.cursor()

cur.execute('''

CREATE TABLE IF NOT EXISTS huesped(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            cedula VARCHAR(50) NOT NULL,
            telefono VARCHAR(20) NOT NULL,
            correo VARCHAR(320) NOT NULL,
            hash VARCHAR(255)
            );


''')

cur.execute('''
        CREATE TABLE IF NOT EXISTS area(
            id INT AUTO_INCREMENT PRIMARY KEY,
            Descripcion VARCHAR(20)
            );
''')

cur.execute('''
        CREATE TABLE IF NOT EXISTS empleados(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            cedula VARCHAR(50) NOT NULL,
            telefono VARCHAR(20),
            area_id INT,
            correo VARCHAR(320) NOT NULL,
            hash VARCHAR(255),
            CONSTRAINT fk_area
                FOREIGN KEY (area_id)
                REFERENCES area(id)
            );
''')

cur.execute('''

CREATE TABLE IF NOT EXISTS categorias(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(150),
            descripcion VARCHAR(300)
            );
''')

cur.execute('''

CREATE TABLE IF NOT EXISTS habitacion(
            id INT AUTO_INCREMENT PRIMARY KEY,
            numero VARCHAR(10),
            piso VARCHAR(10),
            cantMaxHuespedes INT(5),
            disponibilidad boolean,
            costoDia FLOAT,
            detalle VARCHAR(300),
            categoria_id INT,
            CONSTRAINT fk_categorias
                FOREIGN KEY (categoria_id)
                REFERENCES categorias(id)
            );
''')

cur.execute('''

CREATE TABLE IF NOT EXISTS extras(
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100),
descripcion VARCHAR(300),
costo FLOAT
);

''')

cur.execute('''

CREATE TABLE IF NOT EXISTS paquetes(
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(200),
costo FLOAT,
estadia FLOAT,
paqueteDescripcion VARCHAR(320),
extralist_id INT,
listaHabitaciones_id INT,
CONSTRAINT fk_extralist
                FOREIGN KEY (extralist_id)
                REFERENCES extralist(id),
                CONSTRAINT fk_habitacion
                FOREIGN KEY (listaHabitaciones_id)
                REFERENCES habitacion(id)
);

''')

cur.execute('''

CREATE TABLE IF NOT EXISTS reserva(

id INT AUTO_INCREMENT PRIMARY KEY,
date TIMESTAMP,
comentario VARCHAR(300),
costo FLOAT,
huesped_id INT,
CONSTRAINT fk_huesped
                FOREIGN KEY (huesped_id)
                REFERENCES huesped(id)
);

''')

cur.execute(''' 

CREATE TABLE IF NOT EXISTS extralist(

id INT AUTO_INCREMENT PRIMARY KEY,
paquete_id INT,
reserva_id INT,
extra_id INT,
CONSTRAINT fk_paquetes
                FOREIGN KEY (paquete_id)
                REFERENCES paquetes(id),
                CONSTRAINT fk_reserva
                FOREIGN KEY (reserva_id)
                REFERENCES reserva(id),
                CONSTRAINT fk_extras
                FOREIGN KEY (extra_id)
                REFERENCES extras(id)
);
''')

cur.execute('''

CREATE TABLE IF NOT EXISTS detalleReserva(

id INT AUTO_INCREMENT PRIMARY KEY,
reserva_id INT,
habitacion_id INT,
paquete_id INT,
CONSTRAINT fk_reserva
                FOREIGN KEY (reserva_id)
                REFERENCES reserva(id),
                CONSTRAINT fk_habitacion
                FOREIGN KEY (habitacion_id)
                REFERENCES habitacion(id),
                CONSTRAINT fk_paquetes
                FOREIGN KEY (paquete_id)
                REFERENCES paquete(id)
);
''')

cur.execute('''

CREATE TABLE IF NOT EXISTS metodoPago(

id INT AUTO_INCREMENT PRIMARY KEY,
tipo VARCHAR(20)
);
''')

cur.execute('''

CREATE TABLE IF NOT EXISTS factura(

id INT AUTO_INCREMENT PRIMARY KEY,
fechaEmision TIMESTAMP,
huesped_id INT,
metodoPago_id INT,
reserva_id INT,
empleado_id INT,
CONSTRAINT fk_huesped
                FOREIGN KEY (huesped_id)
                REFERENCES huesped(id),
                CONSTRAINT fk_metodoPago
                FOREIGN KEY (metodoPago_id)
                REFERENCES metodoPago(id),
                CONSTRAINT fk_reserva
                FOREIGN KEY (reserva_id)
                REFERENCES reserva(id),
                CONSTRAINT fk_empleados
                FOREIGN KEY (empleado_id)
                REFERENCES empleados(id)
);

''')