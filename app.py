from flask import Flask, render_template, jsonify, redirect, url_for, request
import time
import threading

from modules.hadnle_form import handle_form_data

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stats", methods=["POST"])
def stats():

    (
        nombre_series,
        nombre_exercices,
        temps_travail,
        temps_repos_exercices,
        temps_repos_series,
    ) = handle_form_data(request.form)
    
    # Redirect to the index page if any essential data is missing.
    if (
        not nombre_series
        or not nombre_exercices
        or not temps_travail
        or not temps_repos_exercices
        or not temps_repos_series
    ):
        return redirect(url_for("index"))

    return render_template(
        "stats.html",
        nombre_series=nombre_series,
        nombre_exercices=nombre_exercices,
        temps_travail=temps_travail,
        temps_repos_exercices=temps_repos_exercices,
        temps_repos_series=temps_repos_series,
    )


if __name__ == "__main__":
    # host '0,0,0,0' so we can open the app on other devices on the same network
    app.run(debug=True, host="0.0.0.0")
