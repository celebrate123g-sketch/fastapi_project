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

document.addEventListener("DOMContentLoaded", () => {

    const likeButton = document.getElementById("like-button");
    const favoriteButton = document.getElementById("favorite-button");


    // LIKE

    if (likeButton) {

        likeButton.addEventListener("click", async () => {

            const quoteId = likeButton.dataset.quoteId;
            const liked = likeButton.dataset.liked === "true";

            const action = liked ? "unlike" : "like";

            try {

                const response = await fetch(
                    `/quotes/${quoteId}/${action}`,
                    {
                        method: "PUT"
                    }
                );

                if (!response.ok) {
                    throw new Error("Ошибка при изменении лайка");
                }

                const quote = await response.json();

                likeButton.dataset.liked = String(!liked);

                if (!liked) {
                    likeButton.textContent = "💔 Убрать лайк";
                } else {
                    likeButton.textContent = "❤️ Нравится";
                }

                const likesElement = document.querySelector(
                    ".single-quote-stats .quote-stat:nth-child(2) strong"
                );

                if (likesElement) {
                    likesElement.textContent = quote.likes;
                }

            } catch (error) {

                console.error(error);

            }

        });

    }


    // FAVORITE

    if (favoriteButton) {

        favoriteButton.addEventListener("click", async () => {

            const quoteId = favoriteButton.dataset.quoteId;
            const favorite =
                favoriteButton.dataset.favorite === "true";

            const action = favorite
                ? "unfavorite"
                : "favorite";

            try {

                const response = await fetch(
                    `/quotes/${quoteId}/${action}`,
                    {
                        method: "PUT"
                    }
                );

                if (!response.ok) {
                    throw new Error(
                        "Ошибка при изменении избранного"
                    );
                }

                const quote = await response.json();

                favoriteButton.dataset.favorite =
                    String(!favorite);

                if (!favorite) {

                    favoriteButton.textContent =
                        "♥ В избранном";

                } else {

                    favoriteButton.textContent =
                        "♡ В избранное";

                }

            } catch (error) {

                console.error(error);

            }

        });

    }

});