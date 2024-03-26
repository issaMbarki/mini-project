from flask import Flask, render_template, jsonify, redirect, url_for, request
import threading
import logging
from modules.hadnle_form import handle_form_data
from modules.timer import Timer
from playsound import playsound

app = Flask(__name__)

# Disable the default Flask logger
# log = logging.getLogger("werkzeug")
# log.setLevel(logging.ERROR)

timer=None

@app.route("/",methods=["POST","GET"])
def index():
    return render_template("index.html")

@app.route("/stats", methods=["POST"])
def stats():
    (
        nombre_series,
        nombre_exercices,
        temps_travail_par_exercice,
        temps_repos_exercices,
        temps_repos_series,
    ) = handle_form_data(request.form)

    # Redirect to the index page if any essential data is missing.
    if (
        not nombre_series
        or not nombre_exercices
        or not temps_travail_par_exercice
    ):
        return redirect(url_for("index"))
    global timer
    if timer:
        timer.is_running=False
    timer = Timer(
        nombre_series,
        nombre_exercices,
        temps_travail_par_exercice,
        temps_repos_exercices,
        temps_repos_series,
    )
    timer.is_running = True
    timer.timer_thread = threading.Thread(target=timer.update_timer)
    timer.timer_thread.start()
    return render_template(
        "stats.html",
        nombre_series=nombre_series,
        nombre_exercices=nombre_exercices,
        temps_travail_par_exercice=temps_travail_par_exercice,
        temps_repos_exercices=temps_repos_exercices,
        temps_repos_series=temps_repos_series,
    )


@app.route("/get_timer_info", methods=["POST"])
def get_timer_info():
    return jsonify(
        remaining_time=timer.remaining_time,
        current_exercise=timer.current_exercise,
        current_serie=timer.current_serie,
        is_in_exercise_break=timer.is_in_exercise_break,
        is_in_serie_break=timer.is_in_serie_break,
        serie_break_countdown=timer.serie_break_countdown,
        exercise_break_countdown=timer.exercise_break_countdown,
        worked_time=timer.worked_time,
        is_finished=timer.is_finished
    )


@app.route("/stop_resume_timer", methods=["POST"])
def stop_timer():
    if hasattr(timer, "is_running"):
        if timer.is_running:
            timer.is_running = False
            return jsonify(paused=True)
        else:
            timer.is_running = True
            timer.timer_thread = threading.Thread(target=timer.update_timer)
            timer.timer_thread.start()
            return jsonify(paused=False)



if __name__ == "__main__":
    # host '0,0,0,0' so we can open the app on other devices on the same network
    app.run(debug=True, host="0.0.0.0")
