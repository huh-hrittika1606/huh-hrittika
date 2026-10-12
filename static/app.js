document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("chatForm");
  const input = document.getElementById("queryInput");
  const conversation = document.getElementById("conversation");
  const suggestions = document.getElementById("suggestions");
  const newChat = document.getElementById("newChat");

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function appendMessage(role, text) {
    const article = document.createElement("article");
    article.className = `message ${role === "user" ? "user-message" : "assistant-message"}`;

    const avatarText = role === "user" ? "JD" : "✳";
    const label = role === "user" ? "You" : "Northstar Assistant";

    article.innerHTML = `
      <div class="avatar ${role === "user" ? "user-avatar" : "bot-avatar"}">${avatarText}</div>
      <div class="message-body">
        <div class="message-meta"><strong>${label}</strong><time>${new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</time></div>
        <div class="bubble">${escapeHtml(text)}</div>
      </div>
    `;

    conversation.appendChild(article);
    conversation.scrollTop = conversation.scrollHeight;
  }

  async function sendMessage(message) {
    appendMessage("user", message);

    const thinking = document.createElement("article");
    thinking.className = "message assistant-message";
    thinking.innerHTML = `
      <div class="avatar bot-avatar">✳</div>
      <div class="message-body">
        <div class="message-meta"><strong>Northstar Assistant</strong><time>Just now</time></div>
        <div class="bubble">…thinking</div>
      </div>
    `;
    conversation.appendChild(thinking);
    conversation.scrollTop = conversation.scrollHeight;

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      const data = await response.json();
      const bubble = conversation.querySelectorAll(".assistant-message .bubble");
      const lastBubble = bubble[bubble.length - 1];

      if (lastBubble) {
        lastBubble.innerHTML = escapeHtml(data.reply || "I’m here to help.");
      } else {
        appendMessage("assistant", data.reply || "I’m here to help.");
      }
    } catch (error) {
      const bubble = conversation.querySelectorAll(".assistant-message .bubble");
      const lastBubble = bubble[bubble.length - 1];
      if (lastBubble) {
        lastBubble.innerHTML = escapeHtml("Sorry — I couldn’t reach the support service right now.");
      } else {
        appendMessage("assistant", "Sorry — I couldn’t reach the support service right now.");
      }
      console.error(error);
    }
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const value = input.value.trim();
    if (!value) return;
    input.value = "";
    sendMessage(value);
  });

  suggestions.addEventListener("click", (event) => {
    const button = event.target.closest(".suggestion");
    if (!button) return;
    const query = button.getAttribute("data-query");
    input.value = query;
    form.requestSubmit();
  });

  newChat.addEventListener("click", () => {
    conversation.querySelectorAll(".message").forEach((message) => message.remove());
    const intro = document.createElement("div");
    intro.className = "date-divider";
    intro.innerHTML = '<span></span><small>TODAY</small><span></span>';
    conversation.appendChild(intro);

    const welcome = document.createElement("article");
    welcome.className = "message assistant-message";
    welcome.innerHTML = `
      <div class="avatar bot-avatar">✳</div>
      <div class="message-body">
        <div class="message-meta"><strong>Northstar Assistant</strong><time>Just now</time></div>
        <div class="bubble">Hi Jamie! 👋 I’m your Northstar support assistant. What can I help you with today?</div>
      </div>
    `;
    conversation.appendChild(welcome);
    input.focus();
  });
});
