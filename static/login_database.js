document.getElementById("login_button").addEventListener("click", function () {
  console.log("login button clicked");

  const username_input = document.getElementById("login_username");
  const password_input = document.getElementById("login_password");
  console.log(username_input.value);

  fetch("/login_user", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: username_input.value,
      password: password_input.value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        window.location.href = "/main_page";
      } else {
        alert(data.message || "Login failed. Please try again.");
      }
    })
    .catch((error) => console.log(error));
});

document.getElementById("signup_button").addEventListener("click", function () {
  console.log("signup button clicked");
  const username_input = document.getElementById("signup_username");
  const password_input = document.getElementById("signup_password");
  const first_name_input = document.getElementById("signup_firstname");
  const last_name_input = document.getElementById("signup_lastname");
  console.log(username_input.value);

  fetch("/add_user", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: username_input.value,
      password: password_input.value,
      first_name: first_name_input.value,
      last_name: last_name_input.value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("login_form").style.display = "block";
        document.getElementById("signup_form").style.display = "none";
      } else {
        console.log("system failed to add new user");
      }
    })
    .catch((error) => console.log(error));
});
