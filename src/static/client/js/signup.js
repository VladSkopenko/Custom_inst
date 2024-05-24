const form = document.getElementById("signup-form");
form?.addEventListener("submit", async (e) => {
  e.preventDefault();

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

  try {
    const response = await fetch("https://photo-bank-by-drujba-drujba-06de47a4.koyeb.app/api/auth/signup", {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Network response was not ok.");
    }

    const responseData = await response.json();
    console.log(responseData);
    // Redirect to email_sended.html
    window.location.href = "/static/client/email_sended.html";
  } catch (error) {
    console.error('Error:', error);
  }
});