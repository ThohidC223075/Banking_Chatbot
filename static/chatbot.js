const chatBody = document.getElementById("chat-body");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const msg = userInput.value.trim();
  if (!msg) return;

  // Show user message instantly
  appendMessage(msg, "user");
  userInput.value = "";
  userInput.focus();

  // Disable input & button while waiting for backend response
  userInput.disabled = true;
  sendBtn.disabled = true;

  try {
    // Send to backend API (adjust URL as needed)
    const response = await fetch("http://127.0.0.1:8000/chatbot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg }),
    });

    if (!response.ok) throw new Error("Network response not ok");

    const data = await response.json();

    // Append backend reply message
    const cleanedReply = (data.reply || "Sorry, no response from server.")
    .replace(/\s+/g, ' ')   // Replace multiple spaces with single space
    .trim();                // Remove leading/trailing spaces

    appendMessage(cleanedReply, "bot");

  } catch (error) {
    appendMessage("⚠️ Server error. Please try again.", "bot");
  } finally {
    userInput.disabled = false;
    sendBtn.disabled = false;
    chatBody.scrollTop = chatBody.scrollHeight;
  }
});

// Function to append message in chat-body
function appendMessage(text, sender) {
  const div = document.createElement("div");
  div.classList.add("message", sender);
  div.innerHTML = `<p>${text}</p>`;
  chatBody.appendChild(div);
  chatBody.scrollTop = chatBody.scrollHeight;
}
