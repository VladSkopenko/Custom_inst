function validateForm(event) {
  event.preventDefault();

  const form = event.target;
  const nickname = form.nickname.value;
  const email = form.email.value;
  const password = form.password.value;
  const URL = `${BASE_URL}/api/auth/signup`;
  const data = {
    nickname: nickname,
    email: email,
    password: password,
  };

  console.log("data: ", data);

  fetchSignupData(data);
}

async function fetchSignupData(data) {
  try {
    const response = await fetch(URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    console.dir("response: ", response);

    if (!response.ok) {
      throw new Error("Failed to sign up");
    }

    const result = await response.json();
    if (response.status == 201) {
      setTimeout(() => {
        window.location = "email_sended.html";
      }, 500);
    }
    console.log("Sign up successful");
    return result;
  } catch (error) {
    console.error("Error during sign up:", error);
  }
}

document.getElementById("signup-form").addEventListener("submit", validateForm);
