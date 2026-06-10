async function send() {
    const q = document.getElementById("question");
    const question = q.value.trim();

    if (!question) {
        return;
    }

    appendMessage("user", question);

    const res = await fetch(
        "http://127.0.0.1:8000/chat",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question
            })
        }
    );

    const data = await res.json();
    appendMessage("bot", data.answer);

    q.value = "";
}

function appendMessage(className, text) {
    const chat = document.getElementById("chat");
    const message = document.createElement("div");
    message.className = className;
    message.textContent = text;
    chat.appendChild(message);
    chat.scrollTop = chat.scrollHeight;
}
