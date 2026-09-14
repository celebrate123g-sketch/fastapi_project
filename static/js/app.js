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

    const commentsCount =
        document.getElementById("comments-count");

    if (commentsCount) {
        commentsCount.textContent = comments.length;
    }

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
const commentForm = document.getElementById("comment-form");
const commentsList = document.getElementById("comments-list");

if (commentForm && commentsList) {

    async function loadComments() {
        const response = await fetch(
            `/quotes/${quoteId}/comments`
        );

        if (!response.ok) {
            commentsList.innerHTML =
                "<p>Не удалось загрузить комментарии.</p>";

            return;
        }

        const comments = await response.json();

        commentsList.innerHTML = "";

        if (comments.length === 0) {
            commentsList.innerHTML =
                "<p>Комментариев пока нет.</p>";

            return;
        }

comments.forEach(comment => {

    const commentElement =
        document.createElement("div");

    commentElement.className =
        "comment-item";

    commentElement.innerHTML = `
        <div class="comment-header">
            <strong>
                ${comment.author}
            </strong>

            <button
                type="button"
                class="delete-comment"
                data-comment-id="${comment.id}"
            >
                Удалить
            </button>
        </div>

    <p>
        ${comment.text}
    </p>

    <small>
        ${new Date(comment.created_at).toLocaleString("ru-RU")}
    </small>
    `;

    commentsList.appendChild(
        commentElement
    );
});

document
    .querySelectorAll(".delete-comment")
    .forEach(button => {

        button.addEventListener(
            "click",
            async function() {

                const commentId =
                    this.dataset.commentId;

                const response = await fetch(
                    `/comments/${commentId}`,
                    {
                        method: "DELETE"
                    }
                );

                if (!response.ok) {
                    return;
                }

                await loadComments();
            }
        );
    });

    commentForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const text =
                document.getElementById(
                    "comment-text"
                ).value.trim();

            if (!text) {
                return;
            }

            const author =
                prompt("Введите имя:");

            if (!author) {
                return;
            }

            const response = await fetch(
                `/quotes/${quoteId}/comments`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        author: author,
                        text: text
                    })
                }
            );

            if (!response.ok) {
                return;
            }

            document.getElementById(
                "comment-text"
            ).value = "";

            await loadComments();
        }
    );

    loadComments();
}

const ratingStars = document.getElementById("rating-stars");
const ratingInfo = document.getElementById("rating-info");

if (ratingStars && ratingInfo) {

    async function loadRating() {

        const response = await fetch(
            `/ratings/quotes/${quoteId}`
        );

        if (!response.ok) {
            ratingInfo.textContent =
                "Не удалось загрузить рейтинг.";

            return;
        }

        const data = await response.json();

        const average =
            Number(data.average_rating || 0);

        const votes =
            Number(data.votes || 0);

        ratingInfo.textContent =
            `Рейтинг: ${average.toFixed(1)} / 5 (${votes} оценок)`;

        const rounded =
            Math.round(average);

        document
            .querySelectorAll(
                "#rating-stars button"
            )
            .forEach(button => {

                const value =
                    Number(button.dataset.rating);

                if (value <= rounded) {
                    button.classList.add("active");
                } else {
                    button.classList.remove("active");
                }
            });
    }

    document
        .querySelectorAll(
            "#rating-stars button"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                async function() {

                    const rating =
                        Number(this.dataset.rating);

                    const userId =
                        prompt(
                            "Введите ID пользователя:"
                        );

                    if (!userId) {
                        return;
                    }

                    const response = await fetch(
                        `/ratings/quotes/${quoteId}`,
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                user_id:
                                    Number(userId),

                                rating: rating
                            })
                        }
                    );

                    if (!response.ok) {
                        return;
                    }

                    await loadRating();
                }
            );
        });

    loadRating();
}

const registerForm =
    document.getElementById("register-form");

if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const username =
                document.getElementById(
                    "register-username"
                ).value.trim();

            const message =
                document.getElementById(
                    "register-message"
                );

            const response = await fetch(
                "/users/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        username: username
                    })
                }
            );

            const data =
                await response.json();

            if (!response.ok) {

                message.textContent =
                    data.detail ||
                    "Ошибка регистрации.";

                return;
            }

            localStorage.setItem(
                "user_id",
                data.id
            );

            localStorage.setItem(
                "username",
                data.username
            );

            window.location.href =
                "/quotes-page";
        }
    );
}


const loginForm =
    document.getElementById("login-form");

if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const username =
                document.getElementById(
                    "login-username"
                ).value.trim();

            const message =
                document.getElementById(
                    "login-message"
                );

            const response = await fetch(
                "/users/login",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        username: username
                    })
                }
            );

            const data =
                await response.json();

            if (!response.ok) {

                message.textContent =
                    data.detail ||
                    "Ошибка входа.";

                return;
            }

            localStorage.setItem(
                "user_id",
                data.id
            );

            localStorage.setItem(
                "username",
                data.username
            );

            window.location.href =
                "/quotes-page";
        }
    );
}