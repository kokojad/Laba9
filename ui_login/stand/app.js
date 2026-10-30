"use strict";

// Учётные данные тестового стенда
const VALID_USER = "student";
const VALID_PASSWORD = "Test123!";

const card = document.getElementById("card");
const form = document.getElementById("login-form");
const dashboard = document.getElementById("dashboard");
const errorBox = document.getElementById("error-message");

// Нестабильный селектор: суффикс класса меняется при каждой загрузке страницы
card.classList.add("card-" + Math.random().toString(36).slice(2, 7));

function showError(text) {
  errorBox.textContent = text;
  errorBox.hidden = false;
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const user = form.elements["username"].value.trim();
  const password = form.elements["password"].value;

  if (user === "" || password === "") {
    showError("Введите имя пользователя и пароль");
    return;
  }
  if (user !== VALID_USER || password !== VALID_PASSWORD) {
    showError("Неверное имя пользователя или пароль");
    return;
  }
  errorBox.hidden = true;
  document.getElementById("welcome-name").textContent = user;
  form.hidden = true;
  dashboard.hidden = false;
});

document.getElementById("logout-btn").addEventListener("click", () => {
  dashboard.hidden = true;
  form.hidden = false;
  form.reset();
});
