from flask import Flask, request, render_template, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hotel_secret_key"

# Base de datos temporal
huespedes = []
usuarios = {}

def generar_factura(reserva):
    return {
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "cliente": reserva["nombre"],
        "habitacion": reserva["habitacion"],
        "tipo": reserva["tipo"],
        "dias": reserva["dias"],
        "precio": reserva["precio"],
        "total": reserva["total"]
    }

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        nombre = request.form["nombre"]
        habitacion = request.form["habitacion"]
        entrada = request.form["entrada"]
        salida = request.form["salida"]
        tipo = request.form["tipo_habitacion"]

        fecha_entrada = datetime.strptime(entrada, "%d/%m/%Y")
        fecha_salida = datetime.strptime(salida, "%d/%m/%Y")
        dias = (fecha_salida - fecha_entrada).days

        if dias <= 0: return "❌ Error: fechas inválidas"

        precio = 150 if tipo == "simple" else 250 if tipo == "doble" else 500
        total = dias * precio

        resultado = {"tipo": tipo, "dias": dias, "precio": precio, "total": total}
        
        factura_data = generar_factura({
            "nombre": nombre, "habitacion": habitacion, "tipo": tipo,
            "dias": dias, "precio": precio, "total": total
        })

        huespedes.append({
            "nombre": nombre, "habitacion": habitacion, "entrada": entrada,
            "salida": salida, "tipo": tipo, "dias": dias, "precio": precio,
            "total": total, "factura": factura_data
        })
        return redirect(url_for('index'))

    return render_template("index.html", huespedes=huespedes, resultado=resultado)

@app.route("/habitaciones")
def habitaciones():
    return render_template("habitaciones.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route("/registro")
def registro():
    return render_template("registro_lista.html", huespedes=huespedes)

@app.route("/registro_usuario", methods=["GET", "POST"])
def registro_usuario():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        if usuario in usuarios:
            return render_template("error.html", mensaje="El usuario ya existe", link="/registro_usuario")
        usuarios[usuario] = password
        return redirect(url_for('login'))
    return render_template("registro_usuario.html")

@app.route("/Iniciar Sesión", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["usuario"]
        p = request.form["password"]
        if u in usuarios and usuarios[u] == p:
            session["usuario"] = u
            return redirect(url_for('index'))
        return render_template("error.html", mensaje="Usuario o contraseña incorrectos", link="/Iniciar Sesión")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for('index'))

@app.route("/factura/<int:id>")
def factura(id):
    reserva = huespedes[id]
    return render_template("factura.html", r=reserva)

@app.route("/tarifas")
def tarifas():
    tipos = [
        {"nombre": "Habitación Económica", "precio": 100, "desc": "Ideal para viajeros individuales."},
        {"nombre": "Habitación Simple", "precio": 150, "desc": "Cama individual, TV y WiFi."},
        {"nombre": "Habitación Doble", "precio": 250, "desc": "Perfecta para parejas."},
        {"nombre": "Habitación Familiar", "precio": 350, "desc": "Capacidad para 4 personas."},
        {"nombre": "Suite Junior", "precio": 450, "desc": "Mayor espacio y comodidad."},
        {"nombre": "Suite Premium", "precio": 500, "desc": "Vista panorámica y minibar."},
        {"nombre": "Suite Presidencial", "precio": 900, "desc": "Máximo lujo y atención exclusiva."}
    ]
    return render_template("tarifas.html", habitaciones=sorted(tipos, key=lambda x: x["precio"]))

if __name__ == "__main__":
    app.run(debug=True, port=8080)