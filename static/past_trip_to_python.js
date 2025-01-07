document.addEventListener("DOMContentLoaded", () => {
  fetch("/get_user_credentials", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        console.error(data.error);
        return;
      }

      // Get the first name and last name from the response
      const firstName = data.first_name;
      const lastName = data.last_name;

      // Populate the HTML elements with user data
      const firstNameElement = document.getElementById("user_first_name");
      const lastNameElement = document.getElementById("user_last_name");

      if (firstNameElement) firstNameElement.textContent = firstName;
      if (lastNameElement) lastNameElement.textContent = lastName;
    })
    .catch((error) => {
      console.error("Error fetching user credentials:", error);
    });
  fetch("/past_history", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        console.error(data.error);
        return;
      }

      const hotelsContainer = document.getElementById("hotels-list");
      const flightsContainer = document.getElementById("flights-list");

      // Display hotels
      if (data.past_hotels && data.past_hotels.length > 0) {
        data.past_hotels.forEach((hotel) => {
          const hotelDiv = document.createElement("div");
          hotelDiv.className = "hotel-item";
          hotelDiv.innerHTML = `
            <p><strong>Name:</strong> ${hotel.name}</p>
            <p><strong>Room Type:</strong> ${hotel.room_type}</p>
            <p><strong>Bed Type:</strong> ${hotel.bed_type}</p>
            <p><strong>Number of Beds:</strong> ${hotel.number_of_beds}</p>
            <p><strong>Price:</strong> $${hotel.price}</p>
          `;
          hotelsContainer.appendChild(hotelDiv);
        });
      } else {
        hotelsContainer.innerHTML = "<p>No past hotels found.</p>";
      }

      // Display flights
      if (data.past_flights && data.past_flights.length > 0) {
        data.past_flights.forEach((flight) => {
          const flightDiv = document.createElement("div");
          flightDiv.className = "flight-item";

          // Create a section for each segment of the flight
          let flightSegmentsHTML = "";
          flight.segments.forEach((segment) => {
            flightSegmentsHTML += `
              <p><strong>From:</strong> ${segment.departure} to ${segment.arrival}</p>
              <p><strong>Departure Time:</strong> ${segment.departure_time}</p>
              <p><strong>Arrival Time:</strong> ${segment.arrival_time}</p>
            `;
          });

          flightDiv.innerHTML = `
            <div>
              <p><strong>Flight ID:</strong> ${flight.flight_id}</p>
              <p><strong>Currency:</strong> ${flight.currency}</p>
              ${flightSegmentsHTML}
              <p><strong>Price:</strong> $${flight.price}</p>
              <p><strong>Seats:</strong> ${flight.number_of_seats}</p>
            </div>
          `;
          flightsContainer.appendChild(flightDiv);
        });
      } else {
        flightsContainer.innerHTML = "<p>No past flights found.</p>";
      }
    })
    .catch((error) => {
      console.error("Error fetching past history:", error);
    });
});
