const urlParams = new URLSearchParams(window.location.search);
const ticketId = urlParams.get("ticket_id");

// Убрали tgId, теперь не используем
// const tgId = urlParams.get("tg_id");

async function checkAccess() {
  // Проверка доступа без tg_id (можно упростить — просто проверка, что обращения есть)
  const res = await fetch(`/api/messages/${ticketId}`, { method: "GET" });
  return res.ok;
}

function renderMessage(msg) {
  const div = document.createElement("div");

  // Класс сообщения — ориентируемся на поле sender
  div.className = msg.sender === 'user' ? "msg user" : "msg support";

  // Текст сообщения
  if (msg.message) {
    const text = document.createElement("div");
    text.textContent = msg.message;
    div.appendChild(text);
  }

  // Вложения
  if (msg.attachment_url && msg.attachment_type) {
    const url = msg.attachment_url;
    const type = msg.attachment_type;

    if (type.startsWith("image/")) {
      const img = document.createElement("img");
      img.src = url;
      img.alt = "Изображение";
      img.style.maxWidth = "100%";
      div.appendChild(img);
    } else if (type.startsWith("video/")) {
      const video = document.createElement("video");
      video.src = url;
      video.controls = true;
      video.style.maxWidth = "100%";
      div.appendChild(video);
    } else {
      const link = document.createElement("a");
      link.href = url;
      link.textContent = "Скачать файл";
      link.target = "_blank";
      div.appendChild(link);
    }
  }

  return div;
}

async function loadMessages() {
  const res = await fetch(`/api/messages/${ticketId}`);
  if (!res.ok) return;

  const messages = await res.json();
  const messagesDiv = document.getElementById("messages");
  messagesDiv.innerHTML = "";

  messages.forEach(msg => {
    const messageDiv = renderMessage(msg);
    messagesDiv.appendChild(messageDiv);
  });

  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendMessage(text, file) {
  const formData = new FormData();
  if (text) formData.append("text", text);
  if (file) formData.append("file", file);

  const res = await fetch(`/api/messages/${ticketId}`, {
    method: "POST",
    body: formData
  });

  return res.ok;
}

async function initChat() {
  const authorized = await checkAccess();
  const authError = document.getElementById("auth-error");
  const chatContent = document.getElementById("chat-content");

  if (!authorized) {
    authError.style.display = "block";
    chatContent.style.display = "none";
    return;
  }

  authError.style.display = "none";
  chatContent.style.display = "block";

  await loadMessages();

  const input = document.getElementById("message-input");
  const fileInput = document.getElementById("file-input");

  document.getElementById("send-btn").addEventListener("click", async () => {
    const text = input.value.trim();
    const file = fileInput.files[0] || null;

    if (!text && !file) return;

    const ok = await sendMessage(text, file);
    if (ok) {
      input.value = "";
      fileInput.value = "";
      await loadMessages();
    } else {
      alert("Ошибка отправки сообщения");
    }
  });
}

window.addEventListener("DOMContentLoaded", initChat);
