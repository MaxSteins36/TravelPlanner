document.addEventListener("DOMContentLoaded", () => {
  function createPlaceCard(place, containerId) {
    const container = document.getElementById(containerId);
    const card = document.createElement("div");
    card.classList.add("card");

    const img = document.createElement("img");
    img.src = place.photo_reference || "https://via.placeholder.com/400";
    img.alt = place.name;
    card.appendChild(img);

    const name = document.createElement("h3");
    name.textContent = place.name;
    card.appendChild(name);

    const address = document.createElement("p");
    address.textContent = place.address;
    card.appendChild(address);

    const rating = document.createElement("p");
    rating.textContent = `${place.rating} / 5 (${place.total_reviews} reviews)`;
    card.appendChild(rating);

    const open_now = document.createElement("p2");
    open_now.textContent = place.open_now ? "Open now!!" : "Closed!";
    card.appendChild(open_now);

    // Opening hours section
    const hourContainer = createHourContainer(place.weekday_text);
    card.appendChild(hourContainer);

    // Review section
    const reviewContainer = createReviewContainer(place.review_infomation);
    card.appendChild(reviewContainer);

    container.appendChild(card);
  }

  function createHourContainer(weekday_text) {
    const hourContainer = document.createElement("div");
    hourContainer.classList.add("hour-container");

    const hourText = document.createElement("p1");
    hourText.textContent =
      "Opening hours: " +
      (weekday_text && weekday_text.length > 0 ? "" : "No hours available");
    hourContainer.appendChild(hourText);

    const toggleButton = document.createElement("button");
    toggleButton.textContent = "Check hours";
    toggleButton.classList.add("toggle-button");

    const fullHours = document.createElement("p");
    fullHours.innerHTML = weekday_text
      ? weekday_text.join("<br>")
      : "No hours available";
    fullHours.style.display = "none";

    toggleButton.addEventListener("click", () => {
      fullHours.style.display =
        fullHours.style.display === "none" ? "block" : "none";
      toggleButton.textContent =
        fullHours.style.display === "none" ? "Check hours" : "Collapse";
    });

    hourContainer.appendChild(fullHours);
    hourContainer.appendChild(toggleButton);

    return hourContainer;
  }

  function createReviewContainer(review_infomation) {
    const reviewContainer = document.createElement("div");
    reviewContainer.classList.add("review-container");

    const reviewText = document.createElement("p1");
    reviewText.textContent =
      "Top review: " +
      (review_infomation && review_infomation.length > 0
        ? ""
        : "No reviews available");
    reviewContainer.appendChild(reviewText);

    const toggleButton = document.createElement("button");
    toggleButton.textContent = "Read more...";
    toggleButton.classList.add("toggle-button");

    const fullReview = document.createElement("p");
    fullReview.innerHTML =
      review_infomation && review_infomation.length > 0
        ? `${review_infomation[0].author_name} --- ${review_infomation[0].rating} stars<br>(${review_infomation[0].relative_time})<br>${review_infomation[0].text}`
        : "No full review available";
    fullReview.style.display = "none";

    toggleButton.addEventListener("click", () => {
      fullReview.style.display =
        fullReview.style.display === "none" ? "block" : "none";
      toggleButton.textContent =
        fullReview.style.display === "none" ? "Read more..." : "Show less...";
    });

    reviewContainer.appendChild(fullReview);
    reviewContainer.appendChild(toggleButton);

    return reviewContainer;
  }

  // Fetch and display data for each category
  fetch("/get_top_attractions")
    .then((response) => response.json())
    .then((data) => {
      data.forEach((place) => createPlaceCard(place, "attraction-cards"));
    })
    .catch((error) => console.error("Error fetching attractions data:", error));

  fetch("/get_top_bars")
    .then((response) => response.json())
    .then((data) => {
      data.forEach((place) => createPlaceCard(place, "bar-cards"));
    })
    .catch((error) => console.error("Error fetching bars data:", error));

  fetch("/get_top_restaurants")
    .then((response) => response.json())
    .then((data) => {
      data.forEach((place) => createPlaceCard(place, "restaurant-cards"));
    })
    .catch((error) => console.error("Error fetching restaurant data:", error));
});
