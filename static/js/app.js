"use strict";

function getAccessToken() {
    return localStorage.getItem("access_token");
}

function getAuthHeaders() {
    const token = getAccessToken();

    return {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
    };
}

async function updateNotificationCount() {
    const badge = document.getElementById(
        "notification-count"
    );

    if (!badge) {
        return;
    }

    try {
        const response = await fetch(
            "/notifications/unread/count",
            {
                headers: getAuthHeaders()
            }
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
        console.debug(
            "Notification API is unavailable."
        );
    }
}

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const likeButton =
            document.getElementById(
                "like-button"
            );

        const favoriteButton =
            document.getElementById(
                "favorite-button"
            );

        if (likeButton) {
            likeButton.addEventListener(
                "click",
                async () => {
                    if (!getAccessToken()) {
                        window.location.href =
                            "/users/login";

                        return;
                    }

                    const quoteId =
                        likeButton.dataset.quoteId;

                    const liked =
                        likeButton.dataset.liked ===
                        "true";

                    const action =
                        liked
                            ? "unlike"
                            : "like";

                    try {
                        const response =
                            await fetch(
                                `/quotes/${quoteId}/${action}`,
                                {
                                    method: "PUT",
                                    headers: getAuthHeaders()
                                }
                            );

                        if (!response.ok) {
                            throw new Error(
                                "Ошибка при изменении лайка"
                            );
                        }

                        const quote =
                            await response.json();

                        likeButton.dataset.liked =
                            String(!liked);

                        likeButton.textContent =
                            !liked
                                ? "💔 Убрать лайк"
                                : "❤️ Нравится";

                        const likesElement =
                            document.querySelector(
                                ".single-quote-stats .quote-stat:nth-child(2) strong"
                            );

                        if (likesElement) {
                            likesElement.textContent =
                                quote.likes;
                        }
                    } catch (error) {
                        console.error(error);
                    }
                }
            );
        }

        if (favoriteButton) {
            favoriteButton.addEventListener(
                "click",
                async () => {
                    if (!getAccessToken()) {
                        window.location.href =
                            "/users/login";

                        return;
                    }

                    const quoteId =
                        favoriteButton.dataset.quoteId;

                    const favorite =
                        favoriteButton.dataset.favorite ===
                        "true";

                    const action =
                        favorite
                            ? "unfavorite"
                            : "favorite";

                    try {
                        const response =
                            await fetch(
                                `/quotes/${quoteId}/${action}`,
                                {
                                    method: "PUT",
                                    headers: getAuthHeaders()
                                }
                            );

                        if (!response.ok) {
                            throw new Error(
                                "Ошибка при изменении избранного"
                            );
                        }

                        await response.json();

                        favoriteButton.dataset.favorite =
                            String(!favorite);

                        favoriteButton.textContent =
                            !favorite
                                ? "♥ В избранном"
                                : "♡ В избранное";
                    } catch (error) {
                        console.error(error);
                    }
                }
            );
        }

        loadQuoteUserStatus();
    }
);

async function loadQuoteUserStatus() {
    if (!getAccessToken()) {
        return;
    }

    const likeButton =
        document.getElementById(
            "like-button"
        );

    const favoriteButton =
        document.getElementById(
            "favorite-button"
        );

    const quoteId =
        likeButton?.dataset.quoteId ||
        favoriteButton?.dataset.quoteId;

    if (!quoteId) {
        return;
    }

    try {
        const response = await fetch(
            `/quotes/${quoteId}/user-status`,
            {
                headers: getAuthHeaders()
            }
        );

        if (!response.ok) {
            return;
        }

        const data =
            await response.json();

        if (likeButton) {
            likeButton.dataset.liked =
                String(data.liked);

            likeButton.textContent =
                data.liked
                    ? "💔 Убрать лайк"
                    : "❤️ Нравится";
        }

        if (favoriteButton) {
            favoriteButton.dataset.favorite =
                String(data.favorite);

            favoriteButton.textContent =
                data.favorite
                    ? "♥ В избранном"
                    : "♡ В избранное";
        }
    } catch (error) {
        console.error(error);
    }
}

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const commentForm =
            document.getElementById(
                "comment-form"
            );

        const commentsList =
            document.getElementById(
                "comments-list"
            );

        if (!commentForm || !commentsList) {
            return;
        }

        const quoteId =
            commentForm.dataset.quoteId;

        async function loadComments() {
            const response =
                await fetch(
                    `/quotes/${quoteId}/comments`
                );

            if (!response.ok) {
                commentsList.innerHTML =
                    "<p>Не удалось загрузить комментарии.</p>";

                return;
            }

            const comments =
                await response.json();

            commentsList.innerHTML = "";

            if (comments.length === 0) {
                commentsList.innerHTML =
                    "<p>Комментариев пока нет.</p>";

                return;
            }

            comments.forEach(
                comment => {
                    const commentElement =
                        document.createElement(
                            "div"
                        );

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
                            ${new Date(
                                comment.created_at
                            ).toLocaleString("ru-RU")}
                        </small>
                    `;

                    commentsList.appendChild(
                        commentElement
                    );
                }
            );

            document
                .querySelectorAll(
                    ".delete-comment"
                )
                .forEach(
                    button => {
                        button.addEventListener(
                            "click",
                            async function() {
                                const commentId =
                                    this.dataset.commentId;

                                const response =
                                    await fetch(
                                        `/comments/${commentId}`,
                                        {
                                            method: "DELETE",
                                            headers: getAuthHeaders()
                                        }
                                    );

                                if (!response.ok) {
                                    return;
                                }

                                await loadComments();
                            }
                        );
                    }
                );
        }

        commentForm.addEventListener(
            "submit",
            async function(event) {
                event.preventDefault();

                const text =
                    document.getElementById(
                        "comment-text"
                    ).value.trim();

                const username =
                    localStorage.getItem(
                        "username"
                    );

                if (!username || !getAccessToken()) {
                    window.location.href =
                        "/users/login";

                    return;
                }

                if (!text) {
                    return;
                }

                const response =
                    await fetch(
                        `/quotes/${quoteId}/comments`,
                        {
                            method: "POST",
                            headers: getAuthHeaders(),
                            body: JSON.stringify({
                                author: username,
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
);

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const ratingStars =
            document.getElementById(
                "rating-stars"
            );

        const ratingInfo =
            document.getElementById(
                "rating-info"
            );

        if (!ratingStars || !ratingInfo) {
            return;
        }

        const quoteId =
            ratingStars.dataset.quoteId;

        async function loadRating() {
            const response =
                await fetch(
                    `/ratings/quotes/${quoteId}`
                );

            if (!response.ok) {
                ratingInfo.textContent =
                    "Не удалось загрузить рейтинг.";

                return;
            }

            const data =
                await response.json();

            const average =
                Number(
                    data.average_rating || 0
                );

            const votes =
                Number(
                    data.votes || 0
                );

            ratingInfo.textContent =
                `Рейтинг: ${average.toFixed(1)} / 5 (${votes} оценок)`;

            const rounded =
                Math.round(average);

            document
                .querySelectorAll(
                    "#rating-stars button"
                )
                .forEach(
                    button => {
                        const value =
                            Number(
                                button.dataset.rating
                            );

                        if (value <= rounded) {
                            button.classList.add(
                                "active"
                            );
                        } else {
                            button.classList.remove(
                                "active"
                            );
                        }
                    }
                );
        }

        document
            .querySelectorAll(
                "#rating-stars button"
            )
            .forEach(
                button => {
                    button.addEventListener(
                        "click",
                        async function() {
                            if (!getAccessToken()) {
                                window.location.href =
                                    "/users/login";

                                return;
                            }

                            const rating =
                                Number(
                                    this.dataset.rating
                                );

                            const response =
                                await fetch(
                                    `/ratings/quotes/${quoteId}`,
                                    {
                                        method: "POST",
                                        headers: getAuthHeaders(),
                                        body: JSON.stringify({
                                            rating: rating
                                        })
                                    }
                                );

                            if (!response.ok) {
                                return;
                            }

                            await loadRating();

                            await loadUserRating(
                                quoteId
                            );
                        }
                    );
                }
            );

        loadRating();
        loadUserRating(quoteId);
    }
);

async function loadUserRating(quoteId) {
    if (!getAccessToken()) {
        return;
    }

    const response =
        await fetch(
            `/ratings/quotes/${quoteId}/user`,
            {
                headers: getAuthHeaders()
            }
        );

    if (!response.ok) {
        return;
    }

    const data =
        await response.json();

    document
        .querySelectorAll(
            "#rating-stars button"
        )
        .forEach(
            button => {
                const value =
                    Number(
                        button.dataset.rating
                    );

                if (value <= data.rating) {
                    button.classList.add(
                        "active"
                    );
                } else {
                    button.classList.remove(
                        "active"
                    );
                }
            }
        );
}

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const registerForm =
            document.getElementById(
                "register-form"
            );

        if (!registerForm) {
            return;
        }

        registerForm.addEventListener(
            "submit",
            async function(event) {
                event.preventDefault();

                const username =
                    document.getElementById(
                        "register-username"
                    ).value.trim();

                const password =
                    document.getElementById(
                        "register-password"
                    ).value;

                const message =
                    document.getElementById(
                        "register-message"
                    );

                const response =
                    await fetch(
                        "/users/",
                        {
                            method: "POST",
                            headers: {
                                "Content-Type":
                                    "application/json"
                            },
                            body: JSON.stringify({
                                username: username,
                                password: password
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
                    "access_token",
                    data.access_token
                );

                localStorage.setItem(
                    "user_id",
                    data.user.id
                );

                localStorage.setItem(
                    "username",
                    data.user.username
                );

                window.location.href =
                    "/quotes-page";
            }
        );
    }
);

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const loginForm =
            document.getElementById(
                "login-form"
            );

        if (!loginForm) {
            return;
        }

        loginForm.addEventListener(
            "submit",
            async function(event) {
                event.preventDefault();

                const username =
                    document.getElementById(
                        "login-username"
                    ).value.trim();

                const password =
                    document.getElementById(
                        "login-password"
                    ).value;

                const message =
                    document.getElementById(
                        "login-message"
                    );

                const response =
                    await fetch(
                        "/users/login",
                        {
                            method: "POST",
                            headers: {
                                "Content-Type":
                                    "application/json"
                            },
                            body: JSON.stringify({
                                username: username,
                                password: password
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
                    "access_token",
                    data.access_token
                );

                localStorage.setItem(
                    "user_id",
                    data.user.id
                );

                localStorage.setItem(
                    "username",
                    data.user.username
                );

                window.location.href =
                    "/quotes-page";
            }
        );
    }
);

function logout() {
    localStorage.removeItem(
        "access_token"
    );

    localStorage.removeItem(
        "user_id"
    );

    localStorage.removeItem(
        "username"
    );

    window.location.href =
        "/";
}

const logoutButton =
    document.getElementById(
        "logout-button"
    );

if (logoutButton) {
    logoutButton.addEventListener(
        "click",
        logout
    );
}

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const userInfo =
            document.getElementById(
                "user-info"
            );

        const loginLink =
            document.getElementById(
                "login-link"
            );

        const logoutButton =
            document.getElementById(
                "logout-button"
            );

        const username =
            localStorage.getItem(
                "username"
            );

        if (username) {
            if (userInfo) {
                userInfo.textContent =
                    username;
            }

            if (loginLink) {
                loginLink.style.display =
                    "none";
            }

            if (logoutButton) {
                logoutButton.style.display =
                    "inline-block";
            }
        }
    }
);