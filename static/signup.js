const form = document.getElementById("signupForm");
const message = document.getElementById("message");

form.onsubmit = async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const confirm_password = document.getElementById("confirm_password").value;

  if (password !== confirm_password) {
    message.style.color = "red";
    message.textContent = "Passwords do not match!";
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:8000/signup", {
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
      message.textContent = data.detail || "Signup failed";
    }
  } catch (error) {
    message.style.color = "red";
    message.textContent = "Server error!";
  }
};

// 👁️ Toggle Password Visibility
const togglePassword = document.getElementById("togglePassword");
const passwordInput = document.getElementById("password");

togglePassword.addEventListener("click", () => {
  const type = passwordInput.type === "password" ? "text" : "password";
  passwordInput.type = type;
  togglePassword.classList.toggle("fa-eye");
  togglePassword.classList.toggle("fa-eye-slash");
});

// 👁️ Toggle Confirm Password Visibility
const toggleConfirm = document.getElementById("toggleConfirmPassword");
const confirmInput = document.getElementById("confirm_password");

toggleConfirm.addEventListener("click", () => {
  const type = confirmInput.type === "password" ? "text" : "password";
  confirmInput.type = type;
  toggleConfirm.classList.toggle("fa-eye");
  toggleConfirm.classList.toggle("fa-eye-slash");
});
