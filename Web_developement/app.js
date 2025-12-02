// web/app.js This code is referenced from ChatGPT
document.addEventListener("DOMContentLoaded", () => {
    //CONFIG
    const API_BASE = "http://127.0.0.1:8080"; 
  
    //DOM
    const messagesEl = document.getElementById("messages");
    const formEl     = document.getElementById("chat-form");
    const inputEl    = document.getElementById("chat-input");
    const sendBtn    = document.getElementById("send-btn");
    const statusEl   = document.getElementById("status");
  
    //Quick health check
    (async () => {
      try {
        const r = await fetch(`${API_BASE}/health`);
        const ok = r.ok && (await r.json()).ok;
        if (ok) { statusEl.textContent = "online"; statusEl.classList.add("ok"); }
        else    { statusEl.textContent = "offline"; }
      } catch {
        statusEl.textContent = "offline";
      }
    })();
  
    //UI helpers
    function addBubble(role, text = "", isError = false) {
      const row = document.createElement("div");
      row.className = `row ${role}`;
  
      const bubble = document.createElement("div");
      bubble.className = `bubble ${role}` + (isError ? " error" : "");
      bubble.textContent = text;
  
      row.appendChild(bubble);
      messagesEl.appendChild(row);
      messagesEl.scrollTop = messagesEl.scrollHeight;
      return bubble;
    }
  
    function setDisabled(disabled) {
      inputEl.disabled = disabled;
      sendBtn.disabled = disabled;
    }
  
    //SSE over POST (robust parser)
    async function openSSEPost(url, body, handlers = {}) {
      const r = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
  
      if (!r.ok || !r.body) throw new Error(`HTTP ${r.status}`);
  
      const reader  = r.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer    = "";
      let eventName = null;
  
      const flush = () => {
        const lines = buffer.split(/\r?\n/);
        buffer = lines.pop() ?? "";
  
        for (const line of lines) {
          if (!line) { eventName = null; continue; } // event boundary
          if (line.startsWith("event:")) {
            eventName = line.slice(6).trim();
          } else if (line.startsWith("data:")) {
            const payload = line.slice(5);
            if (eventName === "done") {
              handlers.onDone && handlers.onDone();
            } else if (eventName) {
              try {
                const parsed = payload ? JSON.parse(payload) : {};
                handlers.onEvent && handlers.onEvent(eventName, parsed);
              } catch {
                handlers.onEvent && handlers.onEvent(eventName, payload);
              }
            } else {
              handlers.onMessage && handlers.onMessage(payload);
            }
          }
        }
      };
  
      try {
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });
          flush();
        }
        if (buffer) { buffer += "\n"; flush(); }
      } catch (err) {
        handlers.onError && handlers.onError(err);
      } finally {
        handlers.onDone && handlers.onDone();
      }
    }
  
    //Stream renderer
    function streamAnswer(body, assistantBubble) {
      let textBuffer = "";
      let flushTimer = null;
  
      const flushText = () => {
        if (!textBuffer) return;
        assistantBubble.textContent += textBuffer;
        textBuffer = "";
        messagesEl.scrollTop = messagesEl.scrollHeight;
      };
  
      const onMessage = (chunk) => {
        // append exactly what server sends 
        textBuffer += chunk;
        if (!flushTimer) {
          flushTimer = setTimeout(() => {
            flushText();
            flushTimer = null;
          }, 30);
        }
      };
  
      const onEvent = (name, data) => {
        //show meta in console for debugging
        //console.log("meta:", data);
      };
  
      const onDone = () => {
        if (flushTimer) clearTimeout(flushTimer);
        flushText();
        setDisabled(false);
      };
  
      const onError = (err) => {
        if (flushTimer) clearTimeout(flushTimer);
        flushText();
        assistantBubble.textContent += `\n[stream error: ${err}]`;
        setDisabled(false);
      };
  
      openSSEPost(`${API_BASE}/chat/stream`, body, { onMessage, onEvent, onDone, onError })
        .catch(onError);
    }
  
    //Form handler
    formEl.addEventListener("submit", (e) => {
      e.preventDefault();
      const text = (inputEl.value || "").trim();
      if (!text) return;
  
      addBubble("user", text);                    // user bubble
      const bot = addBubble("assistant", "");     // assistant bubble
      setDisabled(true);
  
      streamAnswer({ message: text, params: null }, bot);
  
      inputEl.value = "";
      inputEl.focus();
    });
  });
  