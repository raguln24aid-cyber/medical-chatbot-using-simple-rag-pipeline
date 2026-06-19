/* ===================================================
   MediChat — Frontend Logic
   =================================================== */

const API_URL = "http://127.0.0.1:8000";

// DOM elements
const chatArea = document.getElementById("chat");
const questionInput = document.getElementById("question");
const sendBtn = document.getElementById("sendBtn");
const welcomeScreen = document.getElementById("welcomeScreen");
const statusIndicator = document.getElementById("statusIndicator");
const sidebar = document.getElementById("sidebar");
const menuToggle = document.getElementById("menuToggle");
const themeToggle = document.getElementById("themeToggle");
const newChatBtn = document.getElementById("newChatBtn");

let isWaiting = false;

// ---------- Initialization ----------

document.addEventListener("DOMContentLoaded", () => {
    checkServerStatus();
    setInterval(checkServerStatus, 15000);
    initTheme();
    autoResizeTextarea();
});

// ---------- Server Status ----------

async function checkServerStatus() {
    const dot = statusIndicator.querySelector(".status-dot");
    const text = statusIndicator.querySelector(".status-text");
    try {
        const res = await fetch(`${API_URL}/`, { signal: AbortSignal.timeout(3000) });
        if (res.ok) {
            dot.className = "status-dot online";
            text.textContent = "Backend online";
        } else {
            dot.className = "status-dot offline";
            text.textContent = "Backend error";
        }
    } catch {
        dot.className = "status-dot offline";
        text.textContent = "Backend offline";
    }
}

// ---------- Theme Toggle ----------

function initTheme() {
    const saved = localStorage.getItem("medichat-theme");
    if (saved === "light") {
        document.documentElement.setAttribute("data-theme", "light");
        updateThemeIcons("light");
    }
}

themeToggle.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", next === "dark" ? "" : "light");
    localStorage.setItem("medichat-theme", next);
    updateThemeIcons(next);
});

function updateThemeIcons(theme) {
    const sun = themeToggle.querySelector(".sun-icon");
    const moon = themeToggle.querySelector(".moon-icon");
    if (theme === "light") {
        sun.style.display = "none";
        moon.style.display = "block";
    } else {
        sun.style.display = "block";
        moon.style.display = "none";
    }
}

// ---------- Sidebar Toggle ----------

menuToggle.addEventListener("click", () => {
    if (window.innerWidth <= 900) {
        sidebar.classList.toggle("open");
    } else {
        sidebar.classList.toggle("collapsed");
    }
});

// ---------- New Chat ----------

newChatBtn.addEventListener("click", () => {
    // Remove all messages but keep the welcome screen
    const messages = chatArea.querySelectorAll(".message, .typing-wrapper");
    messages.forEach(m => m.remove());
    // Show welcome screen again
    if (welcomeScreen) {
        welcomeScreen.style.display = "flex";
    }
    questionInput.value = "";
    questionInput.style.height = "auto";
    questionInput.focus();
});

// ---------- Auto-resize Textarea ----------

function autoResizeTextarea() {
    questionInput.addEventListener("input", () => {
        questionInput.style.height = "auto";
        questionInput.style.height = Math.min(questionInput.scrollHeight, 120) + "px";
    });

    questionInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            send();
        }
    });
}

// ---------- Quick Prompts ----------

function usePrompt(el) {
    const text = el.textContent.replace(/^[^\w]+/, "").trim();
    questionInput.value = `Tell me about ${text.toLowerCase()}`;
    questionInput.focus();
    questionInput.dispatchEvent(new Event("input"));

    // Close mobile sidebar
    if (window.innerWidth <= 900) {
        sidebar.classList.remove("open");
    }
}

function useWelcomePrompt(el) {
    const title = el.querySelector(".welcome-card-title").textContent;
    const desc = el.querySelector(".welcome-card-desc").textContent;
    questionInput.value = desc;
    questionInput.focus();
    questionInput.dispatchEvent(new Event("input"));
}

// ---------- Send Message ----------

async function send() {
    const question = questionInput.value.trim();
    if (!question || isWaiting) return;

    // Hide welcome screen
    if (welcomeScreen) {
        welcomeScreen.style.display = "none";
    }

    // Append user message
    appendMessage("user", question);
    questionInput.value = "";
    questionInput.style.height = "auto";

    // Show typing indicator
    isWaiting = true;
    sendBtn.disabled = true;
    const typingEl = showTypingIndicator();

    try {
        const res = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question }),
        });

        const data = await res.json();

        // Remove typing indicator
        typingEl.remove();

        if (res.ok) {
            appendMessage("bot", data.answer);
        } else {
            appendMessage("bot", `⚠️ Error: ${data.detail || "Something went wrong."}`);
        }
    } catch (error) {
        typingEl.remove();
        appendMessage("bot", "⚠️ Could not reach the server. Make sure the backend is running on port 8000.");
    } finally {
        isWaiting = false;
        sendBtn.disabled = false;
        questionInput.focus();
    }
}

// ---------- Append Message ----------

function appendMessage(role, text) {
    const wrapper = document.createElement("div");
    wrapper.className = `message ${role}`;

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = role === "user" ? "You" : "AI";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";

    // Simple markdown-like rendering for bot messages
    if (role === "bot") {
        bubble.innerHTML = formatBotText(text);
    } else {
        bubble.textContent = text;
    }

    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);
    chatArea.appendChild(wrapper);

    // Scroll to bottom
    chatArea.scrollTop = chatArea.scrollHeight;
}

function formatBotText(text) {
    // Basic formatting: bold, italic, line breaks, lists
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\*(.*?)\*/g, "<em>$1</em>")
        .replace(/^[-•]\s+(.+)/gm, "<li>$1</li>")
        .replace(/(<li>.*<\/li>)/gs, "<ul>$1</ul>")
        .replace(/\n/g, "<br>");
}

// ---------- Typing Indicator ----------

function showTypingIndicator() {
    const wrapper = document.createElement("div");
    wrapper.className = "message bot typing-wrapper";

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = "AI";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";

    const typing = document.createElement("div");
    typing.className = "typing-indicator";
    typing.innerHTML = "<span></span><span></span><span></span>";

    bubble.appendChild(typing);
    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);
    chatArea.appendChild(wrapper);

    chatArea.scrollTop = chatArea.scrollHeight;
    return wrapper;
}
