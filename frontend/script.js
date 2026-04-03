// Derives base URL from the current origin — works on localhost and production without changes
const API_BASE = window.location.origin;
// GET /cities?q={query} — min 3 chars, returns [{ name, lat, lon, country, state }]
const CITIES_ENDPOINT = `${API_BASE}/cities`;
const WEATHER_ENDPOINT = `${API_BASE}/weather`;

const searchInput = document.getElementById("search-input");
const searchBtn = document.getElementById("search-btn");
const autocompleteList = document.getElementById("autocomplete-list");
const weatherInfo = document.getElementById("weather-info");
const errorMsg = document.getElementById("error-msg");
const bgVideo = document.getElementById("bg-video");
const bgVideoSrc = document.getElementById("bg-video-src");

let debounceTimer = null;
let activeIndex = -1;
let currentSuggestions = [];

// ─── Weather condition mapping ────────────────────────────────
// Uses OpenWeatherMap icon codes — language-agnostic.
// Full reference: https://openweathermap.org/weather-conditions

const VIDEO_MAP = {
  sunny: "public/videos/sunny.mp4",
  cloudy: "public/videos/cloudy.mp4",
  rainy: "public/videos/rainy.mp4",
  stormy: "public/videos/rainy.mp4", // fallback to rainy until a stormy video exists
  snowy: "public/videos/snowy.mp4",
  foggy: "public/videos/fog.mp4",
};

const WEATHER_SVG_MAP = {
  sunny: "public/svg/weather/sunny.svg",
  cloudy: "public/svg/weather/cloudy.svg",
  rainy: "public/svg/weather/rainy.svg",
  stormy: "public/svg/weather/stormy.svg",
  snowy: "public/svg/weather/snowy.svg",
  foggy: "public/svg/weather/misty.svg",
};

function getWeatherKey(icon) {
  const id = parseInt(icon, 10);
  if (id === 1) return "sunny"; // 01d/01n — clear sky
  if (id >= 2 && id <= 4) return "cloudy"; // 02–04   — few/scattered/broken clouds
  if (id >= 9 && id <= 10) return "rainy"; // 09–10   — drizzle, rain
  if (id === 11) return "stormy"; // 11d/11n — thunderstorm
  if (id === 13) return "snowy"; // 13d/13n — snow
  if (id === 50) return "foggy"; // 50d/50n — mist, fog, haze, smoke
  return "sunny";
}

function switchBackground(icon) {
  const key = getWeatherKey(icon);
  const src = VIDEO_MAP[key];

  if (bgVideoSrc.src.endsWith(src) && bgVideo.classList.contains("visible"))
    return;

  bgVideo.classList.remove("visible");

  setTimeout(() => {
    bgVideoSrc.src = src;
    bgVideo.load();
    bgVideo.play().catch(() => {});
    bgVideo.classList.add("visible");
  }, 400);
}

// ─── Autocomplete ─────────────────────────────────────────────

async function fetchSuggestions(query) {
  try {
    const res = await fetch(
      `${CITIES_ENDPOINT}?q=${encodeURIComponent(query)}`,
    );
    if (!res.ok) return [];
    return await res.json();
  } catch {
    return [];
  }
}

function renderSuggestions(cities) {
  autocompleteList.innerHTML = "";
  activeIndex = -1;
  currentSuggestions = cities;

  if (!cities.length) {
    autocompleteList.classList.add("hidden");
    return;
  }

  cities.forEach((city) => {
    const li = document.createElement("li");

    const nameSpan = document.createElement("span");
    nameSpan.textContent = city.state
      ? `${city.name}, ${city.state}`
      : city.name;

    const countrySpan = document.createElement("span");
    countrySpan.className = "city-country";
    countrySpan.textContent = city.country;

    li.appendChild(nameSpan);
    li.appendChild(countrySpan);

    li.addEventListener("mousedown", (e) => {
      e.preventDefault();
      selectCity(city.name);
    });
    autocompleteList.appendChild(li);
  });

  autocompleteList.classList.remove("hidden");
}

function clearAutocomplete() {
  autocompleteList.innerHTML = "";
  autocompleteList.classList.add("hidden");
  activeIndex = -1;
  currentSuggestions = [];
}

function setActiveItem(index) {
  const items = autocompleteList.querySelectorAll("li");
  items.forEach((li) => li.classList.remove("active"));
  if (index >= 0 && index < items.length) {
    items[index].classList.add("active");
    searchInput.value = currentSuggestions[index].name;
  }
  activeIndex = index;
}

// ─── Weather fetch ────────────────────────────────────────────

async function fetchWeather(city) {
  hideError();

  try {
    const res = await fetch(`${WEATHER_ENDPOINT}/${encodeURIComponent(city)}`);

    if (res.status === 404) {
      showError("City not found. Please try again.");
      hideWeather();
      return;
    }

    if (!res.ok) {
      showError("Something went wrong. Please try again later.");
      hideWeather();
      return;
    }

    const data = await res.json();
    renderWeather(data);
  } catch {
    showError("Could not connect to the server.");
    hideWeather();
  }
}

// ─── Render ───────────────────────────────────────────────────

function renderWeather(data) {
  document.getElementById("city-name").textContent =
    data.city_name + (data.country_code ? `, ${data.country_code}` : "");

  document.getElementById("temperature").textContent = Math.round(
    data.temperature,
  );

  document.getElementById("description").textContent = data.weather_description;

  document.getElementById("humidity").textContent = `${data.humidity}%`;

  document.getElementById("wind").textContent = `${data.wind_speed} m/s`;

  document.getElementById("pressure").textContent = `${data.pressure} hPa`;

  const weatherIcon = document.getElementById("weather-icon");
  weatherIcon.src = WEATHER_SVG_MAP[getWeatherKey(data.icon)];
  weatherIcon.alt = data.weather_description;
  weatherIcon.classList.remove("hidden");

  switchBackground(data.icon);
  showWeather();
}

function showWeather() {
  weatherInfo.classList.remove("hidden");
  // Re-trigger animation
  weatherInfo.classList.remove("entering");
  void weatherInfo.offsetWidth; // force reflow
  weatherInfo.classList.add("entering");
}

function hideWeather() {
  weatherInfo.classList.add("hidden");
}

function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.classList.remove("hidden");
}

function hideError() {
  errorMsg.classList.add("hidden");
}

// ─── Select a city (from autocomplete or manual search) ───────

function selectCity(name) {
  searchInput.value = name;
  clearAutocomplete();
  fetchWeather(name);
}

// ─── Events ───────────────────────────────────────────────────

searchInput.addEventListener("input", () => {
  const q = searchInput.value.trim();

  clearTimeout(debounceTimer);

  if (q.length < 3) {
    clearAutocomplete();
    return;
  }

  debounceTimer = setTimeout(async () => {
    const cities = await fetchSuggestions(q);
    renderSuggestions(cities);
  }, 280);
});

searchInput.addEventListener("keydown", (e) => {
  // Save raw typed value before arrow navigation replaces it
  if (e.key !== "ArrowDown" && e.key !== "ArrowUp") {
    searchInput.dataset.raw = searchInput.value;
  }

  const items = autocompleteList.querySelectorAll("li");

  if (e.key === "ArrowDown") {
    e.preventDefault();
    setActiveItem(Math.min(activeIndex + 1, items.length - 1));
  } else if (e.key === "ArrowUp") {
    e.preventDefault();
    setActiveItem(Math.max(activeIndex - 1, -1));
    if (activeIndex === -1)
      searchInput.value = searchInput.dataset.raw || searchInput.value;
  } else if (e.key === "Enter") {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (query) {
      clearAutocomplete();
      fetchWeather(query);
    }
  } else if (e.key === "Escape") {
    clearAutocomplete();
  }
});

searchInput.addEventListener("blur", () => {
  setTimeout(clearAutocomplete, 150);
});

searchBtn.addEventListener("click", () => {
  const query = searchInput.value.trim();
  if (query) {
    clearAutocomplete();
    fetchWeather(query);
  }
});
