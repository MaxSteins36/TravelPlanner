document.getElementById("submit").addEventListener("click", () => {
  const formData = {
    origin: document.getElementById("origin").value,
    destination: document.getElementById("destination").value,
    departureDate: document.getElementById("departureDate").value,
    returnDate: document.getElementById("returnDate").value,
    adults: document.getElementById("adults").value,
    city: document.getElementById("city").value,
    checkInDate: document.getElementById("checkInDate").value,
    checkOutDate: document.getElementById("checkOutDate").value,
    roomQuantity: document.getElementById("roomQuantity").value,
  };

  fetch("/api/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  })
    .then((response) => response.json())
    .then((data) => {
      // Call a function to display the data
      console.log(data);
      displayFlightData(data);
      displayHotelData(data);
    })
    .catch((error) => console.error("Error:", error));
});

function displayFlightData(flightData) {
  const resultsDiv = document.getElementById("results"); // A div in your HTML to hold the results
  resultsDiv.innerHTML = ""; // Clear any previous results

  // Assuming flightData is an object with a "flights" array
  const flights = flightData.flights; // Adjust this based on the actual structure

  flights.forEach((flight, index) => {
    const flightDiv = document.createElement("div");
    flightDiv.className = "flight-result";

    let outboundHtml =
      "<p><strong>Outbound:</strong></p><div class='flight-details'>";
    flight.outbound.forEach((outboundFlight) => {
      outboundHtml += `
    <div class="flight-detail-pair">
      <p><strong>Departure:</strong> ${outboundFlight.departure}</p>
      <p><strong>Arrival:</strong> ${outboundFlight.arrival}</p>
    </div>
    <div class="flight-detail-pair">
      <p><strong>Departure Time:</strong> ${outboundFlight.departure_time}</p>
      <p><strong>Arrival Time:</strong> ${outboundFlight.arrival_time}</p>
    </div>
    <div class="flight-detail-pair">
      <p><strong>Number of Seats:</strong> ${outboundFlight.number_of_seats}</p>
      <p><strong>Price:</strong> ${outboundFlight.price} ${outboundFlight.currency}</p>
    </div>
  `;
    });
    outboundHtml += "</div>";

    let returnHtml =
      "<p><strong>Return:</strong></p><div class='flight-details'>";
    flight.return.forEach((returnFlight) => {
      returnHtml += `
    <div class="flight-detail-pair">
      <p><strong>Departure:</strong> ${returnFlight.departure}</p>
      <p><strong>Arrival:</strong> ${returnFlight.arrival}</p>
    </div>
    <div class="flight-detail-pair">
      <p><strong>Departure Time:</strong> ${returnFlight.departure_time}</p>
      <p><strong>Arrival Time:</strong> ${returnFlight.arrival_time}</p>
    </div>
    <div class="flight-detail-pair">
      <p><strong>Price:</strong> ${returnFlight.price} ${returnFlight.currency}</p>
    </div>
  `;
    });
    returnHtml += "</div>";

    flightDiv.innerHTML = `
  <h3>Flight Option ${index + 1}</h3>
  ${outboundHtml}
  ${returnHtml}
  <button class="add-flight-button" id="add-flight-${index}">Add Trip</button>
`;

    // Append the flight div to the results container
    resultsDiv.appendChild(flightDiv);

    // Add an event listener to the "Add Trip" button
    const addButton = document.getElementById(`add-flight-${index}`);
    addButton.addEventListener("click", function () {
      console.log(`Add button clicked for Flight Option ${index + 1}`);
      console.log("Flight details:", flight);

      // Send POST request to the backend with the flight data
      fetch("/add_trip", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ flights: [flight] }), // Sending only the selected flight
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Response from server:", data);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  });
}

function displayHotelData(hotelData) {
  const resultsDiv = document.getElementById("hotel_information_container");
  if (!resultsDiv) {
    console.error("Hotel information container not found.");
    return;
  }

  resultsDiv.innerHTML = ""; // Clear previous results

  // Check if hotelData.hotels is valid
  if (!hotelData.hotels || hotelData.hotels.length === 0) {
    resultsDiv.innerHTML = "<p>No hotels found</p>";
    return;
  }

  const hotels = hotelData.hotels;

  hotels.forEach((hotel, index) => {
    const hotelDiv = document.createElement("div");
    hotelDiv.className = "hotel-result";

    hotelDiv.innerHTML = `
      <h3>Hotel Option ${index + 1}</h3>
      <p><strong>Hotel Name:</strong> ${hotel.name}</p>
      <p><strong>Room Type:</strong> ${hotel.room_type}</p>
      <p><strong>Bed Type:</strong> ${hotel.bed_type}</p>
      <p><strong>Number of Beds:</strong> ${hotel.number_of_beds}</p>
      <p><strong>Price:</strong> $${hotel.price}</p>
      <button class="add-hotel-button" id="add-hotel-${index}">Add Hotel</button>
    `;

    resultsDiv.appendChild(hotelDiv);

    // Correctly select the button after appending to the DOM
    const addButton = document.getElementById(`add-hotel-${index}`);
    addButton.addEventListener("click", function () {
      console.log(`Add button clicked for Hotel Option ${index + 1}`);
      console.log("Hotel details:", hotel);

      // Send POST request to the backend with the hotel data
      fetch("/add_hotel", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(hotel), // Sending the hotel object
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Response from server:", data);
          alert("Hotel added successfully!");
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Failed to add hotel.");
        });
    });
  });
}

function fetchOptimalMonth(month) {
  const optimalMonthData = {
    origin: document.getElementById("origin").value,
    destination: document.getElementById("destination").value,
    returnDate: document.getElementById("returnDate").value,
    departureDate: document.getElementById("departureDate").value,
    adults: document.getElementById("adults").value,
    month: month,
  };

  fetch("/get_optimal_month", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(optimalMonthData),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      displayOptimalFlights(data);
    })
    .catch((error) => {
      console.error("Error fetching optimal month data:", error);
    });
}
function displayOptimalFlights(data) {
  const flightListContainer = document.getElementById("display_optimal_month");

  flightListContainer.innerHTML = "";
  console.log("HERE");

  // Assuming the correct array is inside the "optimal_month_results" key
  const flightsToDisplay = data.optimal_month_results[0]; // Adjust based on actual structure

  if (Array.isArray(flightsToDisplay) && flightsToDisplay.length > 0) {
    flightsToDisplay.forEach((flight) => {
      const flightItem = document.createElement("div");
      flightItem.classList.add("flight-item");

      flightItem.innerHTML = `
        <p>Flight ID: ${flight.id}</p>
        <p>Airline: ${flight.airline}</p>
        <p>Price: ${flight.price} ${flight.currency}</p>
        <p>Departure Time: ${new Date(
          flight.departure_time
        ).toLocaleString()}</p>
        <p>Return Date: ${new Date(flight.return_date).toLocaleString()}</p>
        <p>Cabin: ${flight.cabin}</p>
        <hr>
        <h4>Outbound Flight</h4>
        <p>Departure Time: ${new Date(
          flight.outbound.departure_time
        ).toLocaleString()}</p>
        <p>Return Date: ${new Date(
          flight.outbound.return_date
        ).toLocaleString()}</p>
        <p>Airline: ${flight.outbound.airline}</p>
        <hr>
        <h4>Inbound Flight</h4>
        <p>Departure Time: ${new Date(
          flight.inbound.departure_time
        ).toLocaleString()}</p>
        <p>Return Date: ${new Date(
          flight.inbound.return_date
        ).toLocaleString()}</p>
        <p>Airline: ${flight.inbound.airline}</p>
      `;

      flightListContainer.appendChild(flightItem);
    });
  } else {
    flightListContainer.innerHTML = "No flights available for this month.";
  }
}
const flightDiv = document.getElementById("flights-container"); // Replace with the actual parent container ID

flightDiv.addEventListener("click", (event) => {
  if (event.target && event.target.classList.contains("add-flight-button")) {
    const index = event.target.id.split("-")[2]; // Get the index from the button ID

    console.log("in button");
    const flightData = {
      flightOption: `Flight Option ${index + 1}`,
      outbound: flight.outbound.map((outboundFlight) => ({
        departure: outboundFlight.departure,
        arrival: outboundFlight.arrival,
        departure_time: outboundFlight.departure_time,
        arrival_time: outboundFlight.arrival_time,
        number_of_seats: outboundFlight.number_of_seats,
        price: outboundFlight.price,
        currency: outboundFlight.currency,
      })),
      return: flight.return.map((returnFlight) => ({
        departure: returnFlight.departure,
        arrival: returnFlight.arrival,
        departure_time: returnFlight.departure_time,
        arrival_time: returnFlight.arrival_time,
        price: returnFlight.price,
        currency: returnFlight.currency,
      })),
    };

    // Send the data to Python (Flask example)
    fetch("/add-trip", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(flightData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Trip added successfully:", data);
      })
      .catch((error) => {
        console.error("Error adding trip:", error);
      });
  }
});
