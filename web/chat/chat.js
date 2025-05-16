class SupportChat {
  constructor() {
      this.ticketId = this.getTicketId();
      this.filesToUpload = [];
      this.initElements();
      this.initEventListeners();
      this.loadMessages();
      this.setupAutoRefresh();
  }

  initElements() {
      this.elements = {
          messagesContainer: document.getElementById('messages-container'),
          messageInput: document.getElementById('message-input'),
          sendBtn: document.getElementById('send-btn'),
          fileInput: document.getElementById('file-input'),
          uploadPreview: document.getElementById('upload-preview'),
          ticketIdSpan: document.getElementById('ticket-id'),
          closeChatBtn: document.getElementById('close-chat')
      };
      
      this.elements.ticketIdSpan.textContent = this.ticketId;
  }

  initEventListeners() {
      this.elements.sendBtn.addEventListener('click', () => this.sendMessage());
      
      this.elements.messageInput.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              this.sendMessage();
          }
      });
      
      this.elements.fileInput.addEventListener('change', (e) => {
          this.filesToUpload = Array.from(e.target.files);
          this.showUploadPreview();
      });
      
      this.elements.closeChatBtn.addEventListener('click', () => {
          if (confirm('Вы уверены, что хотите закрыть чат?')) {
              window.close();
          }
      });
  }

  getTicketId() {
      const params = new URLSearchParams(window.location.search);
      let ticketId = params.get('ticket_id');
      
      if (!ticketId) {
          ticketId = `anon-${Date.now()}`;
          history.replaceState({}, '', `?ticket_id=${ticketId}`);
          this.createTicket(ticketId);
      }
      
      return ticketId;
  }

  async createTicket(ticketId) {
      try {
          await fetch('/api/tickets', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ ticket_id: ticketId })
          });
      } catch (error) {
          console.error('Ошибка создания обращения:', error);
      }
  }

  async loadMessages() {
      try {
          const response = await fetch(`/api/messages/${this.ticketId}`);
          const messages = await response.json();
          
          this.elements.messagesContainer.innerHTML = '';
          
          if (messages.length === 0) {
              this.elements.messagesContainer.innerHTML = 
                  '<div class="no-messages">Нет сообщений</div>';
              return;
          }
          
          messages.forEach(msg => this.appendMessage(msg));
          this.scrollToBottom();
      } catch (error) {
          console.error('Ошибка загрузки сообщений:', error);
          this.elements.messagesContainer.innerHTML = 
              '<div class="error">Ошибка загрузки сообщений</div>';
      }
  }

  appendMessage(msg) {
      const messageEl = document.createElement('div');
      messageEl.className = `message ${msg.sender}`;
      
      const contentEl = document.createElement('div');
      contentEl.className = 'message-content';
      
      if (msg.content_type === 'text') {
          contentEl.textContent = msg.content;
      } else if (msg.content_type === 'image') {
          const img = document.createElement('img');
          img.src = msg.content_url;
          img.alt = 'Изображение';
          contentEl.appendChild(img);
      } else if (msg.content_type === 'video') {
          const video = document.createElement('video');
          video.src = msg.content_url;
          video.controls = true;
          contentEl.appendChild(video);
      }
      
      const timeEl = document.createElement('div');
      timeEl.className = 'message-time';
      timeEl.textContent = new Date(msg.timestamp).toLocaleTimeString();
      
      messageEl.appendChild(contentEl);
      messageEl.appendChild(timeEl);
      this.elements.messagesContainer.appendChild(messageEl);
  }

  async sendMessage() {
      const text = this.elements.messageInput.value.trim();
      
      if (!text && this.filesToUpload.length === 0) return;
      
      try {
          if (this.filesToUpload.length > 0) {
              await this.uploadFiles(text);
          } else {
              await this.sendTextMessage(text);
          }
          
          this.elements.messageInput.value = '';
          this.filesToUpload = [];
          this.elements.uploadPreview.innerHTML = '';
          this.elements.fileInput.value = '';
          
          // Обновляем сообщения после отправки
          setTimeout(() => this.loadMessages(), 500);
      } catch (error) {
          console.error('Ошибка отправки сообщения:', error);
          alert('Не удалось отправить сообщение');
      }
  }

  async sendTextMessage(text) {
      await fetch(`/api/messages/${this.ticketId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
      });
  }

  async uploadFiles(text) {
      const formData = new FormData();
      
      if (text) {
          formData.append('text', text);
      }
      
      this.filesToUpload.forEach(file => {
          formData.append('file', file);
      });
      
      await fetch(`/api/messages/${this.ticketId}`, {
          method: 'POST',
          body: formData
      });
  }

  showUploadPreview() {
      this.elements.uploadPreview.innerHTML = '';
      
      this.filesToUpload.forEach((file, index) => {
          const previewEl = document.createElement('div');
          previewEl.className = 'file-preview';
          
          if (file.type.startsWith('image/')) {
              const img = document.createElement('img');
              img.src = URL.createObjectURL(file);
              previewEl.appendChild(img);
          } else if (file.type.startsWith('video/')) {
              const video = document.createElement('video');
              video.src = URL.createObjectURL(file);
              video.controls = true;
              previewEl.appendChild(video);
          } else {
              previewEl.textContent = file.name;
          }
          
          const removeBtn = document.createElement('span');
          removeBtn.className = 'remove-file';
          removeBtn.innerHTML = '&times;';
          removeBtn.addEventListener('click', () => {
              this.filesToUpload.splice(index, 1);
              this.showUploadPreview();
          });
          
          previewEl.appendChild(removeBtn);
          this.elements.uploadPreview.appendChild(previewEl);
      });
  }

  scrollToBottom() {
      this.elements.messagesContainer.scrollTop = 
          this.elements.messagesContainer.scrollHeight;
  }

  setupAutoRefresh() {
      setInterval(() => this.loadMessages(), 5000);
  }
}

// Инициализация чата при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
  new SupportChat();
});