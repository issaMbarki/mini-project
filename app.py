from flask import Flask, render_template, jsonify, redirect, url_for, request
import time
import threading
import logging
from modules.hadnle_form import handle_form_data

app = Flask(__name__)

# Disable the default Flask logger
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


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
        # Additional variables used in the update_timer function
        self.temps_total = (
            (temps_travail_par_exercice + temps_repos_exercices) * nombre_exercices
        ) * nombre_series + (nombre_series - 1) * temps_repos_series
        self.remaining_time = self.calc_temps_total()
        self.current_serie = 1
        self.current_exercise = 1
        self.worked_time = 0
        self.exercise_break_countdown = temps_repos_exercices
        self.serie_break_countdown = temps_repos_series
        self.is_in_exercise_break = False
        self.is_in_serie_break = False
        self.is_running = False
        self.timer_thread = None
        self.notification_sound = "notification_sound.mp3"

    def calc_temps_total(self):
        if self.nombre_exercices == 1:
            return (
                self.temps_repos_series * (self.nombre_series - 1)
                + self.temps_travail_par_exercice * self.nombre_series
            )

        temps_total_par_serie = (
            self.temps_travail_par_exercice * self.nombre_exercices
        ) + (self.temps_repos_exercices * (self.nombre_exercices - 1))

        temps_total_toutes_series = (temps_total_par_serie * self.nombre_series) + (
            self.temps_repos_series
        ) * (self.nombre_series - 1)
        return temps_total_toutes_series

    # Function to update the timer
    def update_timer(self):
        # Track the time spent working on an exercise
        while self.is_running and self.remaining_time > 0:
            time.sleep(1)
            self.remaining_time -= 1
            self.worked_time += 1

            # those two conditions for when the user press on resume button
            # added because if he was in break time and he toggle pause/resume then the programm will exit the function without finishing the break time (serie_break_countdown,serie_break_countdown)
            # 7ydihom w fach tkoni f repos diri pause, tsnay wahd 5s, diri resume, aybalk lfer9
            if self.is_in_exercise_break:
                self.switch_to_exercise_break(True)
                self.remaining_time += 1
            if self.is_in_serie_break:
                self.switch_to_series_break(True)
                self.remaining_time += 1

            # if he finish one exercise
            if self.worked_time == self.temps_travail_par_exercice:
                if self.current_exercise < self.nombre_exercices:
                    self.switch_to_exercise_break()
                else:
                    self.switch_to_series_break()

                self.worked_time = 0  # Reset the worked_time when switching between exercises or series

            # If the remaining time reaches 0, stop the timer
            if self.remaining_time == 0:
                self.is_running = False

    # Function to switch to the exercise break period
    def switch_to_exercise_break(self, from_resume_exercice=False):
        if not from_resume_exercice:
            self.current_exercise += 1
            self.is_in_exercise_break = True

        # Sleep for the duration of the exercise break time
        for _ in range(self.exercise_break_countdown):
            if not self.is_running:
                break
            time.sleep(1)
            self.remaining_time -= 1
            self.exercise_break_countdown -= 1

        # to make sure he finished  his break before going back to work
        if self.exercise_break_countdown == 0:
            self.exercise_break_countdown = self.temps_repos_exercices
            self.is_in_exercise_break = False

    # Function to switch to the series break period
    def switch_to_series_break(self, from_resume_exercice=False):
        if not from_resume_exercice:
            self.current_serie += 1
            self.is_in_serie_break = True
            self.current_exercise = 1

        # Sleep for the duration of the series break time
        for _ in range(self.serie_break_countdown):
            if not self.is_running:
                break
            time.sleep(1)
            self.remaining_time -= 1
            self.serie_break_countdown -= 1

        # to make sure he finished  his break before going back to work
        if self.serie_break_countdown == 0:
            self.serie_break_countdown = self.temps_repos_series
            self.is_in_serie_break = False


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
    return jsonify(
        remaining_time=timer.remaining_time,
        current_exercise=timer.current_exercise,
        current_serie=timer.current_serie,
        is_in_exercise_break=timer.is_in_exercise_break,
        is_in_serie_break=timer.is_in_serie_break,
        serie_break_countdown=timer.serie_break_countdown,
        exercise_break_countdown=timer.exercise_break_countdown,
        worked_time=timer.worked_time,
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
