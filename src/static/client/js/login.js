
const form = document.forms[0];

form?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const t = e.target;
  const username = t.username.value;
  const password = t.password.value;
  const URL = `${BASE_URL}/api/auth/login`;
  await fetch(URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      username: username,
      password: password,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw "ERROR STATUS: " + response.status;
      }
      return response.json();
    })
    .then((json) => {
      console.log(json);
      if (json?.token_type == "bearer") {
        localStorage.setItem("access_token", json?.access_token);
        localStorage.setItem("refresh_token", json?.refresh_token);
        localStorage.setItem("logged", "true");
        localStorage.setItem("username", username);
        setTimeout(() => {
          window.location = "main.html";
        }, 500);
      }
    })
    .catch((err) => {
      console.log("ERROR", err);
      alert(`${err}`)
    });
});
