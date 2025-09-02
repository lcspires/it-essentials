from flask import Flask, request, render_template, redirect, url_for
import models

def setup_routes(app):
    @app.route("/", methods=["GET"])
    def index():
        produtos = models.get_produtos()
        return render_template("index.html", produtos=produtos)

    @app.route("/add", methods=["POST"])
    def add_produto():
        nome = request.form.get("nome")
        valor = request.form.get("valor")
        models.add_produto(nome, valor)
        return redirect(url_for("index"))
