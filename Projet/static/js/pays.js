console.log("Le script JavaScript est en cours d'exécution !");
async function fetchCountries() {
  const response = await fetch("https://restcountries.com/v3.1/all");
  const data = await response.json();
  return data;
}
console.log("Le script JavaScript est en cours d'exécution !");

async function populateCountries() {
  const countries = await fetchCountries();
  const selectElement = document.getElementById("pays");
  const hiddenInput = document.getElementById("selectedCountry");

  countries.sort((a, b) => {
    if (a.name.common < b.name.common) return -1;
    if (a.name.common > b.name.common) return 1;
    return 0;
  });

  countries.forEach((country) => {
    const option = document.createElement("option");
    option.value = country.name.common;
    option.textContent = country.name.common;
    selectElement.appendChild(option);
  });

  selectElement.addEventListener("change", (event) => {
    hiddenInput.value = event.target.value;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  populateCountries();
});
