(() => {
  const urlParams = new URLSearchParams(window.location.search);
  const ticketId = urlParams.get("ticket_id");

  async function loadMessages() {
    const res = await fetch(`/api/messages/${ticketId}`);
    if (!res.ok) {
      alert("Ошибка загрузки сообщений");
      return;
    }
    const messages = await res.json();
    const messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML = "";

    messages.forEach(msg => {
      const div = document.createElement("div");
      div.className = msg.sender === "user" ? "msg user" : "msg support";
      div.textContent = msg.content;
      messagesDiv.appendChild(div);
    });

    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  async function sendMessage(text) {
    const res = await fetch(`/api/messages/${ticketId}`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ text })
    });

    if (res.ok) {
      await loadMessages();
    } else {
      alert("Ошибка отправки");
    }
  }

  window.addEventListener("DOMContentLoaded", () => {
    loadMessages();

    const sendBtn = document.getElementById("send-btn");
    if (sendBtn) {
      sendBtn.addEventListener("click", () => {
        const input = document.getElementById("message-input");
        const text = input.value.trim();
        if (!text) return;
        sendMessage(text);
        input.value = "";
      });
    }
  });
})();
