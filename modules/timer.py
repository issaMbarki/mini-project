import time
from playsound import playsound


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
        self.temps_total = self.calc_temps_total()
        self.remaining_time = self.temps_total
        self.current_serie = 1
        self.current_exercise = 1
        self.worked_time = 0
        self.exercise_break_countdown = temps_repos_exercices
        self.serie_break_countdown = temps_repos_series
        self.is_in_exercise_break = False
        self.is_in_serie_break = False
        self.is_running = False
        self.is_finished = False
        self.timer_thread = None

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

    # Method to update the timer
    def update_timer(self):
        if self.remaining_time == self.temps_total:
            playsound("./static/sounds/your_workout_starts_now.wav")
        # Track the time spent working on an exercise
        while self.is_running and self.remaining_time > 0:
            print("remaining time: ", self.remaining_time)
            # those two conditions for when the user press on resume button
            # added because if he was in break time and he toggle pause/resume then the programm will exit the function without finishing the break time (serie_break_countdown,serie_break_countdown)
            # 7ydihom w fach tkoni f repos diri pause, tsnay wahd 2s, diri resume, aybalk probleme
            if self.is_in_exercise_break:
                self.switch_to_exercise_break(from_resume_exercice=True)
            if self.is_in_serie_break:
                self.switch_to_series_break(from_resume_exercice=True)

            # if he finish one exercise
            if self.worked_time == self.temps_travail_par_exercice:
                self.worked_time = 0  # Reset the worked_time when switching between exercises or series
                if self.current_exercise < self.nombre_exercices:
                    playsound("./static/sounds/exercise_break_starts.wav")
                    self.switch_to_exercise_break()
                else:
                    playsound("./static/sounds/series_break_starts.wav")
                    self.switch_to_series_break()


            time.sleep(1)
            self.remaining_time -= 1
            self.worked_time += 1
            # If the remaining time reaches 0, stop the timer
            if self.remaining_time == 0:
                playsound("./static/sounds/you_finished_your_workout.wav")
                self.is_running = False
                self.is_finished = True

    # Function to switch to the exercise break period
    def switch_to_exercise_break(self, from_resume_exercice=False):
        if not from_resume_exercice:
            self.current_exercise += 1
            self.is_in_exercise_break = True
        # Sleep for the duration of the exercise break time
        for _ in range(self.exercise_break_countdown):
            time.sleep(1)
            self.remaining_time -= 1
            self.exercise_break_countdown -= 1
            if not self.is_running:
                break

        # to make sure he finished  his break before going back to work
        if self.exercise_break_countdown == 0:
            playsound("./static/sounds/new_exercise_starts.wav")
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
            time.sleep(1)
            self.remaining_time -= 1
            self.serie_break_countdown -= 1
            if not self.is_running:
                break

        # to make sure he finished  his break before going back to work
        if self.serie_break_countdown == 0:
            playsound("./static/sounds/new_series_start.wav")
            self.serie_break_countdown = self.temps_repos_series
            self.is_in_serie_break = False
