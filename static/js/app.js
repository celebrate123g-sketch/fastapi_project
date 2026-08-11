"use strict";


/* =========================================================
   QUOTES — MAIN JAVASCRIPT
   ========================================================= */


/* =========================
   NOTIFICATION BADGE
   ========================= */

async function updateNotificationCount() {

    const badge = document.getElementById(
        "notification-count"
    );

    if (!badge) {
        return;
    }

    try {

        /*
         * Позже здесь подключим настоящий
         * endpoint нашего Notification API.
         *
         * Например:
         *
         * /notifications/unread/count
         */

        const response = await fetch(
            "/notifications/unread/count"
        );

        if (!response.ok) {
            return;
        }

        const data = await response.json();

        const count = Number(
            data.count ?? 0
        );

        if (count > 0) {

            badge.textContent =
                count > 99
                    ? "99+"
                    : count;

            badge.hidden = false;

        } else {

            badge.hidden = true;

        }

    } catch (error) {

        /*
         * Пока API может отсутствовать,
         * поэтому не ломаем страницу.
         */

        console.debug(
            "Notification API is unavailable."
        );
    }
}


/* =========================
   FAVORITE BUTTONS
   ========================= */

function initializeFavoriteButtons() {

    const buttons = document.querySelectorAll(
        ".favorite-button"
    );

    buttons.forEach(
        (button) => {

            button.addEventListener(
                "click",
                () => {

                    const active =
                        button.classList.toggle(
                            "is-active"
                        );

                    button.textContent =
                        active
                            ? "♥"
                            : "♡";

                }
            );

        }
    );
}


/* =========================
   INITIALIZATION
   ========================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        updateNotificationCount();

        initializeFavoriteButtons();

    }
);