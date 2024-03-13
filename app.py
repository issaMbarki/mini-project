from flask import Flask, render_template, jsonify, redirect, url_for, request
import time
import threading

from modules.hadnle_form import handle_form_data

app = Flask(__name__)



class Timer:
    def __init__(
        self,
        nombre_series,
        nombre_exercices,
        temps_travail_par_exercice,
        temps_repos_exercices,
        temps_repos_series,
    ):
        self.nombre_series = nombre_series
        self.nombre_exercices = nombre_exercices
        self.temps_travail_par_exercice = temps_travail_par_exercice
        self.temps_repos_exercices = temps_repos_exercices
        self.temps_repos_series = temps_repos_series
        #####
        self.temps_total = (
            (temps_travail_par_exercice + temps_repos_exercices) * nombre_exercices
        ) * nombre_series + (nombre_series - 1) * temps_repos_series

        self.remaining_time = self.temps_total + 1
        self.is_running = False
        self.timer_thread = None
        self.notification_sound = "notification_sound.mp3"

    def update_timer(self):
        while self.is_running:
            print("remaining :", self.remaining_time)
            self.remaining_time -= 1
            time.sleep(1)
            if self.remaining_time == 0:
                # playsound(self.notification_sound)
                self.is_running = False


@app.route("/")
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
        or not temps_repos_exercices
        or not temps_repos_series
    ):
        return redirect(url_for("index"))
    global timer
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
    return jsonify(remaining_time=timer.remaining_time)


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
