// ===============================
// BLACKONIX Login.js
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    const loginForm = document.getElementById("login-form");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const errorBox = document.getElementById("error-message");

    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        // Clear previous error
        errorBox.innerText = "";

        // Validation
        if (!validateEmail(email)) {
            showError("Please enter a valid email address.");
            return;
        }

        if (password.length < 6) {
            showError("Password must be at least 6 characters.");
            return;
        }

        // Send data to backend (Flask)
        fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = "/dashboard";
            } else {
                showError(data.message || "Invalid email or password.");
            }
        })
        .catch(error => {
            showError("Server error. Please try again.");
            console.error("Error:", error);
        });
    });

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function showError(message) {
        errorBox.innerText = message;
        errorBox.style.color = "red";
    }

});