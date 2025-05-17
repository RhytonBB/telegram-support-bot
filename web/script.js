// --- КОНСТАНТЫ ---
const VALID_LOGIN = "Example";
const VALID_PASSWORD = "Example";

// --- АВТОРИЗАЦИЯ ---
const loginForm = document.getElementById("login-form");
const errorMsg = document.getElementById("error-msg");

if (loginForm) {
  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const login = document.getElementById("login").value.trim();
    const password = document.getElementById("password").value.trim();

    if (login === VALID_LOGIN && password === VALID_PASSWORD) {
      sessionStorage.setItem("operatorAuth", "true");
      window.location.href = "operators.html";
    } else {
      errorMsg.textContent = "Неверный логин или пароль";
    }
  });
}

// --- ОХРАНА ДОСТУПА НА СТРАНИЦЕ ОПЕРАТОРА ---
if (window.location.pathname.endsWith("operators.html")) {
  if (sessionStorage.getItem("operatorAuth") !== "true") {
    window.location.href = "index.html";
  }
}

// --- ЛОГАУТ ---
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    sessionStorage.removeItem("operatorAuth");
    window.location.href = "index.html";
  });
}

// --- ВКЛАДКИ ---
const tabButtons = document.querySelectorAll(".tab-btn");
const tabContents = document.querySelectorAll(".tab-content");

tabButtons.forEach(btn =>
  btn.addEventListener("click", () => {
    tabButtons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    tabContents.forEach(c => c.classList.remove("active"));
    document.getElementById(btn.dataset.tab).classList.add("active");
  })
);

// --- МОКОВЫЕ ДАННЫЕ ОБРАЩЕНИЙ ---
const tickets = {
  new: [
    {
      id: 1,
      user_id: 123,
      title: "Обращение №1",
      messages: [
        { sender: "user", type: "text", text: "Здравствуйте" },
        { sender: "user", type: "image", url: "https://via.placeholder.com/150" },
        { sender: "user", type: "video", url: "https://sample-videos.com/video123/mp4/240/big_buck_bunny_240p_1mb.mp4" }
      ]
    },
    {
      id: 2,
      user_id: 222,
      title: "Обращение №2",
      messages: [{ sender: "user", type: "text", text: "Привет" }]
    }
  ],
  active: [],
  archived: []
};

// --- СОСТОЯНИЕ ОТКРЫТЫХ ЧАТОВ ---
let openChats = [];

// --- ОТРИСОВКА СПИСКОВ ОБРАЩЕНИЙ ---
function renderTicketsList(status) {
  const listEl = document.getElementById(`${status}-tickets-list`);
  if (!listEl) return;
  listEl.innerHTML = "";

  tickets[status].forEach(ticket => {
    const li = document.createElement("li");
    li.textContent = ticket.title;
    li.dataset.id = ticket.id;
    li.addEventListener("click", () => openChat(ticket.id));
    listEl.appendChild(li);
  });
}

// --- ОТКРЫТИЕ ЧАТА ---
function openChat(id) {
  if (openChats.find(c => c.id === id)) {
    activateChat(id);
    return;
  }

  let ticket;
  ["new", "active", "archived"].some(status => {
    ticket = tickets[status].find(t => t.id === id);
    return !!ticket;
  });

  if (!ticket) return alert("Обращение не найдено");

  if (tickets.new.find(t => t.id === id)) {
    tickets.new = tickets.new.filter(t => t.id !== id);
    ticket.status = "active";
    tickets.active.push(ticket);
  }

  openChats.push({ id, minimized: false });

  renderTicketsList("new");
  renderTicketsList("active");
  renderTicketsList("archived");

  renderChatTabs();
  activateChat(id);
}

// --- АКТИВАЦИЯ ЧАТА ---
function activateChat(id) {
  document.querySelectorAll("#chat-tabs .chat-tab").forEach(tab => {
    tab.classList.toggle("active", parseInt(tab.dataset.id) === id);
  });
  document.querySelectorAll("#chat-windows .chat-window").forEach(win => {
    win.classList.toggle("active", parseInt(win.dataset.id) === id);
  });
}

// --- ОТРИСОВКА ВКЛАДОК И ОКОН ---
function renderChatTabs() {
  const tabsContainer = document.getElementById("chat-tabs");
  tabsContainer.innerHTML = "";

  openChats.forEach(({ id, minimized }) => {
    const ticket = findTicketById(id);
    if (!ticket) return;

    const tab = document.createElement("div");
    tab.className = "chat-tab" + (minimized ? " minimized" : "");
    tab.dataset.id = id;
    tab.textContent = ticket.title;
    if (id === getActiveChatId()) tab.classList.add("active");

    tab.addEventListener("click", () => activateChat(id));
    tabsContainer.appendChild(tab);
  });

  renderChatWindows();
}

function findTicketById(id) {
  let ticket;
  ["new", "active", "archived"].some(status => {
    ticket = tickets[status].find(t => t.id === id);
    return !!ticket;
  });
  return ticket;
}

function renderChatWindows() {
  const container = document.getElementById("chat-windows");
  container.innerHTML = "";

  openChats.forEach(({ id, minimized }) => {
    const ticket = findTicketById(id);
    if (!ticket) return;

    const chatDiv = document.createElement("div");
    chatDiv.className = "chat-window" + (id === getActiveChatId() ? " active" : "");
    chatDiv.dataset.id = id;
    chatDiv.style.display = minimized ? "none" : "flex";

    const controls = document.createElement("div");
    controls.className = "chat-controls";

    const btnMinimize = document.createElement("button");
    btnMinimize.textContent = minimized ? "Развернуть чат" : "Временно закрыть чат";
    btnMinimize.addEventListener("click", () => toggleMinimizeChat(id));
    controls.appendChild(btnMinimize);

    const btnClose = document.createElement("button");
    btnClose.textContent = "Закрыть обращение";
    btnClose.addEventListener("click", () => closeTicket(id));
    controls.appendChild(btnClose);

    const btnTransfer = document.createElement("button");
    btnTransfer.textContent = "Передать партнеру";
    btnTransfer.disabled = true;
    controls.appendChild(btnTransfer);

    chatDiv.appendChild(controls);

    const messagesDiv = document.createElement("div");
    messagesDiv.className = "chat-messages";

    ticket.messages.forEach(msg => {
      const msgEl = document.createElement("div");
      msgEl.className = "message " + (msg.sender === "user" ? "user-msg" : "operator-msg");

      if (msg.type === "text") {
        msgEl.textContent = msg.text;
      } else if (msg.type === "image") {
        const img = document.createElement("img");
        img.src = msg.url;
        img.style.maxWidth = "150px";
        img.style.maxHeight = "150px";
        msgEl.appendChild(img);
      } else if (msg.type === "video") {
        const video = document.createElement("video");
        video.src = msg.url;
        video.controls = true;
        video.style.maxWidth = "300px";
        msgEl.appendChild(video);
      }

      messagesDiv.appendChild(msgEl);
    });

    chatDiv.appendChild(messagesDiv);

    const inputDiv = document.createElement("div");
    inputDiv.className = "chat-input";

    const textarea = document.createElement("textarea");
    textarea.rows = 2;
    inputDiv.appendChild(textarea);

    const sendBtn = document.createElement("button");
    sendBtn.textContent = "Отправить";
    sendBtn.addEventListener("click", () => sendMessage(id, textarea.value));
    inputDiv.appendChild(sendBtn);

    chatDiv.appendChild(inputDiv);
    container.appendChild(chatDiv);
  });
}

// --- УТИЛИТЫ ---
function getActiveChatId() {
  const activeTab = document.querySelector("#chat-tabs .chat-tab.active");
  return activeTab ? parseInt(activeTab.dataset.id) : null;
}

function toggleMinimizeChat(id) {
  openChats = openChats.map(c => {
    if (c.id === id) c.minimized = !c.minimized;
    return c;
  });
  renderChatTabs();
}

function closeTicket(id) {
  const idx = tickets.active.findIndex(t => t.id === id);
  if (idx === -1) return;

  const ticket = tickets.active.splice(idx, 1)[0];
  ticket.status = "archived";
  tickets.archived.push(ticket);

  openChats = openChats.filter(c => c.id !== id);

  renderTicketsList("new");
  renderTicketsList("active");
  renderTicketsList("archived");
  renderChatTabs();

  const currentActiveId = getActiveChatId();
  if (currentActiveId === id && openChats.length > 0) {
    activateChat(openChats[0].id);
  } else if (openChats.length === 0) {
    document.getElementById("chat-windows").innerHTML = "";
    document.getElementById("chat-tabs").innerHTML = "";
  }
}

function sendMessage(id, text) {
  if (!text.trim()) return;

  const ticket = findTicketById(id);
  if (!ticket) return;

  ticket.messages.push({ sender: "operator", type: "text", text: text.trim() });

  renderChatWindows();

  const chatWindow = document.querySelector(`.chat-window[data-id='${id}']`);
  if (chatWindow) {
    const textarea = chatWindow.querySelector("textarea");
    textarea.value = "";
  }
}

// --- ИНИЦИАЛИЗАЦИЯ ---
if (window.location.pathname.endsWith("operators.html")) {
  renderTicketsList("new");
  renderTicketsList("active");
  renderTicketsList("archived");
  renderChatTabs();
}
