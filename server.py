from flask import Flask
import models
import routes

app = Flask(__name__)

# Inicializa DB
models.init_db()

# Configura rotas
routes.setup_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
