const form = document.getElementById("loginForm");
const message = document.getElementById("message");

form.onsubmit = async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  try {
    const res = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (res.ok) {
      message.style.color = "green";
      message.textContent = data.message;
      setTimeout(() => {
        window.location.href = "chatbot";
      }, 1000);
    } else {
      message.style.color = "red";
      message.textContent = data.detail || "Login failed";
    }
  } catch (error) {
    message.style.color = "red";
    message.textContent = "Server error!";
  }
};

// 🔁 Password show/hide toggle
const togglePassword = document.getElementById("togglePassword");
const passwordInput = document.getElementById("password");

togglePassword.addEventListener("click", () => {
  const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
  passwordInput.setAttribute("type", type);

  // Toggle icon style
  togglePassword.classList.toggle("fa-eye");
  togglePassword.classList.toggle("fa-eye-slash");
});
