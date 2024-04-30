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
 const response = await fetch("/api/auth/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  const result = await response.json();
  console.log("result: ", result);
  if (result.status === "ok") {
    alert("SUPER");