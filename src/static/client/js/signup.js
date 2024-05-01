const form = document.getElementById("signup-form");
form?.addEventListener("submit", async (e) => {
  e.preventDefault();

  // const payload = new FormData(form);
  // console.log([...payload]);

  const prePayload = new FormData(form);
  const payload = new URLSearchParams(prePayload);
  console.log("payload: ", [...payload]);

  const nickname = form.nickname.value;
  const email = form.email.value;
  const password = form.password.value;

  const data = {
    nickname: nickname,
    email: email,
    password: password,
  };
  console.log("data: ", data);


  fetch(
    "http://0.0.0.0:8000/api/auth/signup", {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    // body: payload,
  })
    .then((res) => {
      if (res.ok) {
        return res.json();
      }
      throw new Error("Network response was not ok.");
    })
    .then((data) => {
      console.log(data);
      // Redirect to email_sended.html
      window.location.href = "/static/client/email_sended.html";
    })
    .catch((err) => console.log(err));
});
