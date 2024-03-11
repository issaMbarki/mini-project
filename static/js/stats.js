
// Accessing the values using data attributes
const nombre_series = document.getElementById("nombre_series").getAttribute("data-value");
const nombre_exercices = document.getElementById("nombre_exercices").getAttribute("data-value");
const temps_travail = document.getElementById("temps_travail").getAttribute("data-value");
const temps_repos_exercices = document.getElementById("temps_repos_exercices").getAttribute("data-value");
const temps_repos_series = document.getElementById("temps_repos_series").getAttribute("data-value");

console.log(nombre_series,
	nombre_exercices,
	temps_travail,
	temps_repos_exercices,
	temps_repos_series);