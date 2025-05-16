// Получить Telegram ID из параметров URL
function getTelegramId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("tg_id");
  }
  
  // Показываем / скрываем элементы
  function showElement(id) {
    document.getElementById(id).style.display = "block";
  }
  function hideElement(id) {
    document.getElementById(id).style.display = "none";
  }
  
  // Проверка пользователя (имитация, тут будет запрос к серверу для проверки)
  async function checkUser(tgId) {
    // Тут будет API-запрос к серверу, пока просто имитируем разрешенный ID для примера
    // Можно отправить fetch к своему API с проверкой
    return tgId && tgId.length > 0; // например, любой непустой tg_id пропускаем
  }
  
  async function initChat() {
    const tgId = getTelegramId();
  
    const authorized = await checkUser(tgId);
  
    if (!authorized) {
      showElement("auth-error");
      hideElement("chat-content");
      return;
    }
  
    showElement("chat-content");
    hideElement("auth-error");
  
    // TODO: загрузка сообщений из API (пока заглушка)
    const messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML = `<div class="msg user">Привет! Это тестовое сообщение.</div>`;
  
    // Отправка сообщения
    document.getElementById("send-btn").addEventListener("click", () => {
      const input = document.getElementById("message-input");
      const text = input.value.trim();
      if (!text) return;
  
      // TODO: отправить на сервер
  
      // Отображаем локально
      const msgDiv = document.createElement("div");
      msgDiv.className = "msg user";
      msgDiv.textContent = text;
      messagesDiv.appendChild(msgDiv);
  
      input.value = "";
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
  }
  
  window.addEventListener("DOMContentLoaded", initChat);

  const ticketId = new URLSearchParams(window.location.search).get("ticket_id");
  const tgId = new URLSearchParams(window.location.search).get("tg_id");
  
  async function checkUser() {
    // Проверка доступа к обращению
    const res = await fetch(`/api/messages/${ticketId}?tg_id=${tgId}`, { method: "GET" });
    return res.ok;
  }
  
  async function loadMessages() {
    const res = await fetch(`/api/messages/${ticketId}?tg_id=${tgId}`);
    if (!res.ok) return;
    const messages = await res.json();
    const messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML = "";
    messages.forEach(msg => {
      const div = document.createElement("div");
      div.className = msg.sender_tg_id == tgId ? "msg user" : "msg support";
      div.textContent = msg.message;
      messagesDiv.appendChild(div);
    });
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }
  
  async function sendMessage(text) {
    const res = await fetch(`/api/messages/${ticketId}?tg_id=${tgId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    return res.ok;
  }
  
  async function initChat() {
    const authorized = await checkUser();
    if (!authorized) {
      document.getElementById("auth-error").style.display = "block";
      document.getElementById("chat-content").style.display = "none";
      return;
    }
    document.getElementById("auth-error").style.display = "none";
    document.getElementById("chat-content").style.display = "block";
  
    await loadMessages();
  
    document.getElementById("send-btn").onclick = async () => {
      const input = document.getElementById("message-input");
      const text = input.value.trim();
      if (!text) return;
      const ok = await sendMessage(text);
      if (ok) {
        input.value = "";
        await loadMessages();
      } else {
        alert("Ошибка отправки сообщения");
      }
    };
  }
  
  window.addEventListener("DOMContentLoaded", initChat);
  