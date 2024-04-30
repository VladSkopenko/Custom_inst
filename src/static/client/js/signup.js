const form = document.forms[0];

form?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const t = e.target;
  const nickname = t.nickname.value;
  const email = t.email.value;
  const password = t.password.value;
  const data = {
    nickname: nickname,
    email: email,
    password: password,
  };
    console.log("data: ", data)
  const URL = `${BASE_URL}/api/auth/signup`;
  await fetch(URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (response.status >= 500) {
        throw "ERROR STATUS: " + response.status;
      }
      if (response.status == 201) {
        window.location = "confirm.html";
      }

      return response.json();
    })
    .then((json) => {
      console.log(json);
      detail = json?.detail;
      err = "";
      if (Array.isArray(detail)) {
        for (const d of detail) {
          const loc = d.loc[1];
          const mgs = d.msg;
          err = err + " " + loc + ": " + mgs;
          console.log(d);
        }
      } else {
        err = detail;
      }
      if (err) {
        showMessage(err);
      }
    })
    .catch((err) => {
      console.log("ERROR", err);
      showMessage(err);
    });
});

