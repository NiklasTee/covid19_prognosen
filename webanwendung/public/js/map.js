import { gatewayKey, gatewayUrl, mapboxKey } from "./config.js";
import { centroids } from "./centroids.js";

// Map initialization
mapboxgl.accessToken = mapboxKey;
const map = new mapboxgl.Map({
  container: "map", // ID of the HTML element to render the map
  style: "mapbox://styles/niklastee/clggaycox003701qyexn0e30q", // Map style dark
  // style: "mapbox://styles/niklastee/clgg9pmrn003b01pkehrsbt6f", // Map style light
  center: [10.4515, 51.1657], // Longitude and latitude of the initial map center (Germany)
  zoom: 5, // Initial zoom level
});

map.on("load", function () {
  // Add the municipal boundaries layer from the GeoJSON file
  map.addSource("municipal-boundaries", {
    type: "geojson",
    data: "data/municipal_boundaries.geojson", // Update this path if needed
  });
  map.addLayer({
    id: "municipal-boundaries-layer",
    type: "fill",
    source: "municipal-boundaries",
    layout: {},
    paint: {
      "fill-color": "#888", // Change the fill color as needed
      "fill-opacity": 0.4,
    },
  });
  // Create a Mapbox GL Geocoder instance
  const geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl,
    placeholder: "Suche einen Ort...",
  });

  // Add the Geocoder to the map
  map.addControl(geocoder, "top-left");
});

// Make Gateway request
const fetchData = async () => {
  try {
    const response = await fetch(gatewayUrl, {
      headers: {
        "x-api-key": gatewayKey,
      },
    });
    const data = await response.json();
    console.log("API response:", data);
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

// Create map layer with data
function displayDataOnMap(data) {
  if (!data) {
    console.error("No data available to display on the map.");
    return;
  }
  map.on("click", "municipal-boundaries-layer", function (e) {
    const id = e.features[0].properties.id;
    const municipalityData = data[id];
    if (municipalityData) {
      const { name, history, prediction } = municipalityData;

      const nameParts = name.split(" ");
      const nameTypeAbbreviation = nameParts.shift(); // Extract and remove the first part (LK or SK)
      const nameTypeFull = {
        LK: "Landkreis",
        SK: "Kreisfreie Stadt",
      }[nameTypeAbbreviation];
      const nameWithoutType = nameParts
        .join(" ")
        .replace(/(?:\s|-)Kreis\b|Kreis\b/i, "")
        .trim(); // Reconstruct the remaining name, remove "kreis" or "-Kreis" wherever it appears in the string, and trim any extra spaces

      // Create HTML content for the popup
      const htmlContent = `
      <div class="kreis-name">
      <div class="municipality-name" title="${nameWithoutType}"><h3>${nameWithoutType}</h3></div>
      <h6>${nameTypeFull}</h6>
      </div>
      <div class="kreis-info">
      <div class="kreis-historie">
      <table class="history">
        <tr>
          <th>Verlauf</th>
          <th>Fälle</th>
        </tr>
        ${history
          .map(
            (cases, i) =>
              `<tr>
                <td class="dates">${new Date(
                  Date.now() - (7 - i) * 24 * 60 * 60 * 1000
                ).toLocaleDateString()}</td>
                <td class="cases">${cases}</td>
              </tr>`
          )
          .join("")}
      </table>
      </div>
      <div class="kreis-spacer"></div>
      <div class="kreis-prognose">
      <table class="prediction">
        <tr>
          <th class="prognose">Prognose</th>
          <th>Fälle</th>
        </tr>
        ${prediction
          .map(
            (cases, i) =>
              `<tr>
                <td class="dates prognose-dates">${new Date(
                  Date.now() + i * 24 * 60 * 60 * 1000
                ).toLocaleDateString()}</td>
                <td class="cases">${cases}</td>
              </tr>`
          )
          .join("")}
      </table>
      </div>
      </div>
    `;

      // Create a popup with the HTML content
      const popup = new mapboxgl.Popup().setHTML(htmlContent);

      // Show the popup at the clicked location
      popup.setLngLat(e.lngLat).addTo(map);
    }
  });
}

// Fetch the data and display it on the map
fetchData().then((data) => {
  displayDataOnMap(data);
});
