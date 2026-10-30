"use strict";

/** Правила валидации формы обратной связи (объект тестирования ЛР №4). */
const validators = {
  name(v) {
    v = v.trim();
    if (v === "") return "Введите имя";
    if (v.length < 2) return "Имя должно содержать не менее 2 символов";
    if (!/^[A-Za-zА-Яа-яЁё\s'-]+$/.test(v)) return "Имя может содержать только буквы";
    return "";
  },
  email(v) {
    v = v.trim();
    if (v === "") return "Введите email";
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return "Введите корректный email";
    return "";
  },
  phone(v) {
    v = v.trim();
    if (v === "") return ""; // поле необязательное
    const digits = v.replace(/\D/g, "").length;
    if (!/^\+?[0-9\s()-]+$/.test(v) || digits < 10 || digits > 15) return "Введите корректный номер телефона";
    return "";
  },
  subject(v) {
    return v === "" ? "Выберите тему" : "";
  },
  message(v) {
    v = v.trim();
    if (v === "") return "Введите сообщение";
    if (v.length < 10) return "Сообщение должно содержать не менее 10 символов";
    if (v.length > 500) return "Сообщение не должно превышать 500 символов";
    return "";
  },
  consent(checked) {
    return checked ? "" : "Необходимо согласие на обработку данных";
  },
};

const form = document.getElementById("contact-form");

function validate() {
  let ok = true;
  for (const [field, check] of Object.entries(validators)) {
    const el = form.elements[field];
    const value = field === "consent" ? el.checked : el.value;
    const message = check(value);
    document.getElementById(`error-${field}`).textContent = message;
    el.classList.toggle("invalid", message !== "");
    el.setAttribute("aria-invalid", message !== "" ? "true" : "false");
    if (message) ok = false;
  }
  return ok;
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  if (validate()) {
    form.hidden = true;
    document.getElementById("success-message").hidden = false;
  }
});
