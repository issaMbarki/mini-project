// Accessing the values using data attributes
// const nombre_series = document
// 	.getElementById("nombre_series")
// 	.getAttribute("data-value");
// const nombre_exercices = document
// 	.getElementById("nombre_exercices")
// 	.getAttribute("data-value");
// const temps_travail_par_exercice = document
// 	.getElementById("temps_travail_par_exercice")
// 	.getAttribute("data-value");
// const temps_repos_exercices = document
// 	.getElementById("temps_repos_exercices")
// 	.getAttribute("data-value");
// const temps_repos_series = document
// 	.getElementById("temps_repos_series")
// 	.getAttribute("data-value");

// console.log(
// 	nombre_series,
// 	nombre_exercices,
// 	temps_travail_par_exercice,
// 	temps_repos_exercices,
// 	temps_repos_series
// );
let intervalId;
function updateTimerInfo() {
	fetch("/get_timer_info", {
		method: 'POST'
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
			const temps_restant_span = document.getElementById("temps_restant");
			temps_restant_span.innerText = jsonData.remaining_time;
			if (jsonData.remaining_time <= 0) {
				clearInterval(intervalId);
			}
		})
		.catch(function (error) {
			console.error("Error:", error);
			if (intervalId) {
				clearInterval(intervalId)
			}
		});
}

intervalId = setInterval(updateTimerInfo, 1000);
const togle_pause_btn = document.getElementById("pause_resume_btn")
togle_pause_btn?.addEventListener('click', () => {
	console.log("clicked");
	fetch("/stop_resume_timer", {
		method: "POST"
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
				clearInterval(intervalId)
				togle_pause_btn.innerText="Continue"
			} else {
				togle_pause_btn.innerText="Pause"
				updateTimerInfo()
				intervalId = setInterval(updateTimerInfo, 1000);
			}
		})
		.catch(function (error) {
			console.error("Error:", error);
		});
})
