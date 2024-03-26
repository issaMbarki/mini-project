const nombre_series = document.getElementById("Nbs").getAttribute("value");
const nombre_exercices = document.getElementById("NbE").getAttribute("value");
const temps_travail_par_exercice = document
  .getElementById("TT")
  .getAttribute("value");
const temps_repos_exercices = document
  .getElementById("Tr")
  .getAttribute("value");
const temps_repos_series = document.getElementById("Trs").getAttribute("value");

let intervalId;
const nb_series_input = document.getElementById("NbsInput");
const nb_exercices_input = document.getElementById("NbEInput");
const work_pause_countdown = document.getElementById("work_pause_countdown");
const temps_restant_hms = document
  .querySelector(".TR .inHms")
  .querySelectorAll("input");
const nextEvent_hms = document
  .querySelector(".PE .inHms")
  .querySelectorAll("input");
const nextEvent_label = document.querySelector(".PE label");
let is_working = true;
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
      // console.log(jsonData);
      const {
        current_exercise,
        current_serie,
        exercise_break_countdown,
        is_in_exercise_break,
        is_in_serie_break,
        remaining_time,
        serie_break_countdown,
        worked_time,
        is_finished,
      } = jsonData;

      updateTime(temps_restant_hms, remaining_time);
      updateCurrentNumber(nb_series_input, current_serie);
      updateCurrentNumber(nb_exercices_input, current_exercise);
      if (!(is_in_exercise_break || is_in_serie_break)) {
        nextEvent_label.innerText = `temps travaillé :`;
        updateTime(nextEvent_hms, worked_time);
      }
      if (is_in_exercise_break) {
        nextEvent_label.innerText = `Prochain exercice : `;
        updateTime(nextEvent_hms, exercise_break_countdown);
      }
      if (is_in_serie_break) {
        nextEvent_label.innerText = `Prochain exercice : `;
        updateTime(nextEvent_hms, serie_break_countdown);
      }
      if (is_finished) {
        is_working = false;
        updateCurrentNumber(nb_series_input, nombre_series);
        updateCurrentNumber(nb_exercices_input, nombre_exercices);
        updateTime(nextEvent_hms, 0);
        clearInterval(intervalId);
      }
      if (remaining_time <= 0) {
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      if (intervalId) {
        clearInterval(intervalId);
      }
    });
}
updateTimerInfo();
intervalId = setInterval(updateTimerInfo, 1000);
const togle_pause_btn = document.getElementById("pause_resume_btn");
const home_btn = document.getElementById("home_btn");
const reset_btn = document.getElementById("reset_btn");
togle_pause_btn?.addEventListener("click", () => {
  if (!is_working) {
    return;
  }
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
        togle_pause_btn.value = "Continue";
      } else {
        togle_pause_btn.value = "Pause";
        updateTimerInfo();
        intervalId = setInterval(updateTimerInfo, 1000);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
reset_btn.addEventListener("click", () => {
  location.reload()
});
function updateTime(hmsArr, seconds) {
  timeInHrs = convertTime(seconds);
  hmsArr.forEach((input, index) => {
    input.value = timeInHrs[index];
  });
}

function convertTime(seconds) {
  const hours = Math.floor(seconds / 3600)
    .toString()
    .padStart(2, "0");
  const minutes = Math.floor((seconds % 3600) / 60)
    .toString()
    .padStart(2, "0");
  const remainingSeconds = (seconds % 60).toString().padStart(2, "0");

  return [hours, minutes, remainingSeconds];
}

function updateCurrentNumber(element, currentData) {
  element.value = currentData;
}
