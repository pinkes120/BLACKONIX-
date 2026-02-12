// ===============================
// BLACKONIX Chat.js
// Real-time Chat with Socket.IO
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    const socket = io();

    const form = document.getElementById("chat-form");
    const input = document.getElementById("message");
    const chatContainer = document.getElementById("chat-container");

    const username = document.body.getAttribute("data-username") || "User";

    // Send Message
    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const message = input.value.trim();

        if (message === "") return;

        const messageData = {
            user: username,
            message: message,
            time: new Date().toLocaleTimeString()
        };

        socket.emit("send_message", messageData);

        addMessage(messageData, "sent");

        input.value = "";
    });

    // Receive Message
    socket.on("receive_message", function (data) {
        addMessage(data, "received");
    });

    // User Connected Notification
    socket.on("user_joined", function (data) {
        addSystemMessage(`${data} joined the chat`);
    });

    // User Left Notification
    socket.on("user_left", function (data) {
        addSystemMessage(`${data} left the chat`);
    });

    // Add Chat Message
    function addMessage(data, type) {

        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", type);

        const userSpan = document.createElement("strong");
        userSpan.innerText = data.user + ": ";

        const textSpan = document.createElement("span");
        textSpan.innerText = data.message;

        const timeDiv = document.createElement("div");
        timeDiv.style.fontSize = "10px";
        timeDiv.style.opacity = "0.7";
        timeDiv.innerText = data.time;

        messageDiv.appendChild(userSpan);
        messageDiv.appendChild(textSpan);
        messageDiv.appendChild(document.createElement("br"));
        messageDiv.appendChild(timeDiv);

        chatContainer.appendChild(messageDiv);
        scrollToBottom();
    }

    // System Messages
    function addSystemMessage(text) {
        const systemDiv = document.createElement("div");
        systemDiv.style.textAlign = "center";
        systemDiv.style.fontSize = "12px";
        systemDiv.style.opacity = "0.6";
        systemDiv.style.margin = "10px 0";
        systemDiv.innerText = text;

        chatContainer.appendChild(systemDiv);
        scrollToBottom();
    }

    // Auto Scroll
    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

});