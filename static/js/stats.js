// Accessing the values using data attributes
const nombre_series = document
  .getElementById("nombre_series")
  .getAttribute("data-value");
const nombre_exercices = document
  .getElementById("nombre_exercices")
  .getAttribute("data-value");
const temps_travail_par_exercice = document
  .getElementById("temps_travail_par_exercice")
  .getAttribute("data-value");
const temps_repos_exercices = document
  .getElementById("temps_repos_exercices")
  .getAttribute("data-value");
const temps_repos_series = document
  .getElementById("temps_repos_series")
  .getAttribute("data-value");

// console.log(
// 	nombre_series,
// 	nombre_exercices,
// 	temps_travail_par_exercice,
// 	temps_repos_exercices,
// 	temps_repos_series
// );
let intervalId;
const temps_restant_span = document.getElementById("temps_restant");
const nb_series_div = document.getElementById("nb_series");
const nb_exercices_div = document.getElementById("nb_exercices");
const nextEventLabel = document.getElementById("nextEventLabel");
const work_pause_countdown = document.getElementById("work_pause_countdown");
function updateTimerInfo() {
  fetch("/get_timer_info", {
    method: "POST",
  })
    .then((response) => {
      if (response.ok) {
        return response.text();
      }
      throw new Error("Network response was not ok.");
    })
    .then((data) => {
      const jsonData = JSON.parse(data); // Convert data to JSON
      console.log(jsonData);
      const {
        current_exercise,
        current_serie,
        exercise_break_countdown,
        is_in_exercise_break,
        is_in_serie_break,
        remaining_time,
        serie_break_countdown,
        worked_time,
      } = jsonData;
      temps_restant_span.innerText = remaining_time+"s";

      if (!(is_in_exercise_break || is_in_serie_break)) {
        nextEventLabel.innerText = `worked time: ${worked_time}s`;
      }
      if (is_in_exercise_break ) {
        nextEventLabel.innerText = `next exercice in: ${exercise_break_countdown}s`;
      }
      if (is_in_serie_break) {
        nextEventLabel.innerText = `next exercice in: ${serie_break_countdown}s`;
      }
      //for number of exercices
      updateProgressBar(nb_exercices_div, current_exercise, nombre_exercices);

      //for number of series
      updateProgressBar(nb_series_div, current_serie, nombre_series);

      if (remaining_time <= 0) {
        clearInterval(intervalId);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      if (intervalId) {
        clearInterval(intervalId);
      }
    });
}
updateTimerInfo()
intervalId = setInterval(updateTimerInfo, 1000);
const togle_pause_btn = document.getElementById("pause_resume_btn");
togle_pause_btn?.addEventListener("click", () => {
  console.log("clicked");
  fetch("/stop_resume_timer", {
    method: "POST",
  })
    .then((response) => {
      if (response.ok) {
        return response.text();
      }
      throw new Error("Network response was not ok.");
    })
    .then((data) => {
      const jsonData = JSON.parse(data); // Convert data to JSON
      if (jsonData.paused) {
        clearInterval(intervalId);
        togle_pause_btn.innerText = "Continue";
      } else {
        togle_pause_btn.innerText = "Pause";
        updateTimerInfo();
        intervalId = setInterval(updateTimerInfo, 1000);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

function updateProgressBar(divElement, currentData, totalData) {
  divElement.classList.toggle("text-dark", currentData === 1);
  divElement.innerText = `${currentData - 1}/${totalData}`;
  divElement.style.width = `${(100 * (currentData - 1)) / totalData}%`;
}
