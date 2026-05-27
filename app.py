from flask import Flask, render_template

# Crear aplicación Flask
app = Flask(__name__)

# Ruta principal
@app.route("/")
def inicio():

    # Mostrar index.html
    return render_template("index.html")

# Ejecutar servidor
if __name__ == "__main__":
    app.run(debug=True)
    