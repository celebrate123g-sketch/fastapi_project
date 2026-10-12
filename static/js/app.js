"use strict";

function getAccessToken() {
    return localStorage.getItem("access_token");
}

function getAuthHeaders() {
    const headers = {
        "Content-Type": "application/json"
    };

    const token = getAccessToken();

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    return headers;
}

async function fetchJSON(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            ...getAuthHeaders(),
            ...options.headers
        }
    });

    let data = {};

    try {
        data = await response.json();
    } catch (error) {
        data = {};
    }

    return {
        response,
        data
    };
}

async function updateNotificationCount() {
    const badge = document.getElementById(
        "notification-count"
    );

    if (!badge || !getAccessToken()) {
        if (badge) {
            badge.hidden = true;
        }

        return;
    }

    try {
        const { response, data } = await fetchJSON(
            "/notifications/unread/count"
        );

        if (!response.ok) {
            return;
        }

        const count = Number(data.count ?? 0);

        badge.textContent =
            count > 99 ? "99+" : String(count);

        badge.hidden = count <= 0;
    } catch (error) {
        console.debug(
            "Notification API is unavailable."
        );
    }
}

async function loadQuoteUserStatus() {
    if (!getAccessToken()) {
        return;
    }

    const likeButton = document.getElementById(
        "like-button"
    );

    const favoriteButton = document.getElementById(
        "favorite-button"
    );

    const quoteId =
        likeButton?.dataset.quoteId ||
        favoriteButton?.dataset.quoteId;

    if (!quoteId) {
        return;
    }

    try {
        const { response, data } = await fetchJSON(
            `/quotes/${quoteId}/user-status`
        );

        if (!response.ok) {
            return;
        }

        if (likeButton) {
            likeButton.dataset.liked = String(
                data.liked
            );

            likeButton.textContent = data.liked
                ? "💔 Убрать лайк"
                : "❤️ Нравится";
        }

        if (favoriteButton) {
            favoriteButton.dataset.favorite = String(
                data.favorite
            );

            favoriteButton.textContent = data.favorite
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
        const likeButton = document.getElementById(
            "like-button"
        );

        const favoriteButton = document.getElementById(
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

                    const action = liked
                        ? "unlike"
                        : "like";

                    try {
                        const { response, data } =
                            await fetchJSON(
                                `/quotes/${quoteId}/${action}`,
                                {
                                    method: "PUT"
                                }
                            );

                        if (!response.ok) {
                            throw new Error(
                                data.detail ||
                                "Не удалось изменить лайк."
                            );
                        }

                        likeButton.dataset.liked =
                            String(!liked);

                        likeButton.textContent = !liked
                            ? "💔 Убрать лайк"
                            : "❤️ Нравится";

                        const likesElement =
                            document.querySelector(
                                ".single-quote-stats .quote-stat:nth-child(2) strong"
                            );

                        if (
                            likesElement &&
                            data.likes !== undefined
                        ) {
                            likesElement.textContent =
                                data.likes;
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

                    const action = favorite
                        ? "unfavorite"
                        : "favorite";

                    try {
                        const { response, data } =
                            await fetchJSON(
                                `/quotes/${quoteId}/${action}`,
                                {
                                    method: "PUT"
                                }
                            );

                        if (!response.ok) {
                            throw new Error(
                                data.detail ||
                                "Не удалось изменить избранное."
                            );
                        }

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
        updateNotificationCount();
    }
);

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const commentForm = document.getElementById(
            "comment-form"
        );

        const commentsList = document.getElementById(
            "comments-list"
        );

        if (!commentForm || !commentsList) {
            return;
        }

        const quoteId = commentForm.dataset.quoteId;

        async function loadComments() {
            try {
                const response = await fetch(
                    `/quotes/${quoteId}/comments`
                );

                if (!response.ok) {
                    commentsList.textContent =
                        "Не удалось загрузить комментарии.";

                    return;
                }

                const comments = await response.json();

                commentsList.replaceChildren();

                if (comments.length === 0) {
                    commentsList.textContent =
                        "Комментариев пока нет.";

                    return;
                }

                comments.forEach(comment => {
                    const commentElement =
                        document.createElement("div");

                    commentElement.className =
                        "comment-item";

                    const header =
                        document.createElement("div");

                    header.className = "comment-header";

                    const author =
                        document.createElement("strong");

                    author.textContent =
                        comment.author || "Пользователь";

                    const deleteButton =
                        document.createElement("button");

                    deleteButton.type = "button";
                    deleteButton.className =
                        "delete-comment";

                    deleteButton.dataset.commentId =
                        comment.id;

                    deleteButton.textContent = "Удалить";

                    header.append(author, deleteButton);

                    const text =
                        document.createElement("p");

                    text.textContent = comment.text;

                    const date =
                        document.createElement("small");

                    date.textContent = comment.created_at
                        ? new Date(
                            comment.created_at
                        ).toLocaleString("ru-RU")
                        : "";

                    commentElement.append(
                        header,
                        text,
                        date
                    );

                    commentsList.appendChild(
                        commentElement
                    );
                });
            } catch (error) {
                console.error(error);

                commentsList.textContent =
                    "Не удалось загрузить комментарии.";
            }
        }

        commentsList.addEventListener(
            "click",
            async event => {
                const button = event.target.closest(
                    ".delete-comment"
                );

                if (!button) {
                    return;
                }

                if (!getAccessToken()) {
                    window.location.href =
                        "/users/login";

                    return;
                }

                const commentId =
                    button.dataset.commentId;

                try {
                    const { response, data } =
                        await fetchJSON(
                            `/comments/${commentId}`,
                            {
                                method: "DELETE"
                            }
                        );

                    if (!response.ok) {
                        console.error(
                            data.detail ||
                            "Не удалось удалить комментарий."
                        );

                        return;
                    }

                    await loadComments();
                } catch (error) {
                    console.error(error);
                }
            }
        );

        commentForm.addEventListener(
            "submit",
            async event => {
                event.preventDefault();

                if (!getAccessToken()) {
                    window.location.href =
                        "/users/login";

                    return;
                }

                const textInput =
                    document.getElementById(
                        "comment-text"
                    );

                if (!textInput) {
                    return;
                }

                const text = textInput.value.trim();

                if (!text) {
                    return;
                }

                try {
                    const { response, data } =
                        await fetchJSON(
                            `/quotes/${quoteId}/comments`,
                            {
                                method: "POST",
                                body: JSON.stringify({
                                    text: text
                                })
                            }
                        );

                    if (!response.ok) {
                        console.error(
                            data.detail ||
                            "Не удалось добавить комментарий."
                        );

                        return;
                    }

                    textInput.value = "";

                    await loadComments();
                } catch (error) {
                    console.error(error);
                }
            }
        );

        loadComments();
    }
);

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const ratingStars = document.getElementById(
            "rating-stars"
        );

        const ratingInfo = document.getElementById(
            "rating-info"
        );

        if (!ratingStars || !ratingInfo) {
            return;
        }

        const quoteId = ratingStars.dataset.quoteId;

        async function loadRating() {
            try {
                const response = await fetch(
                    `/ratings/quotes/${quoteId}`
                );

                if (!response.ok) {
                    ratingInfo.textContent =
                        "Не удалось загрузить рейтинг.";

                    return;
                }

                const data = await response.json();

                const average = Number(
                    data.average_rating || 0
                );

                const votes = Number(
                    data.votes || 0
                );

                ratingInfo.textContent =
                    `Рейтинг: ${average.toFixed(1)} / 5 (${votes} оценок)`;

                const rounded = Math.round(average);

                ratingStars
                    .querySelectorAll("button")
                    .forEach(button => {
                        const value = Number(
                            button.dataset.rating
                        );

                        button.classList.toggle(
                            "active",
                            value <= rounded
                        );
                    });
            } catch (error) {
                console.error(error);
            }
        }

        ratingStars
            .querySelectorAll("button")
            .forEach(button => {
                button.addEventListener(
                    "click",
                    async () => {
                        if (!getAccessToken()) {
                            window.location.href =
                                "/users/login";

                            return;
                        }

                        const rating = Number(
                            button.dataset.rating
                        );

                        try {
                            const { response, data } =
                                await fetchJSON(
                                    `/ratings/quotes/${quoteId}`,
                                    {
                                        method: "POST",
                                        body: JSON.stringify({
                                            rating: rating
                                        })
                                    }
                                );

                            if (!response.ok) {
                                console.error(
                                    data.detail ||
                                    "Не удалось сохранить оценку."
                                );

                                return;
                            }

                            await loadRating();
                            await loadUserRating(quoteId);
                        } catch (error) {
                            console.error(error);
                        }
                    }
                );
            });

        loadRating();
        loadUserRating(quoteId);
    }
);

async function loadUserRating(quoteId) {
    if (!getAccessToken()) {
        return;
    }

    try {
        const { response, data } = await fetchJSON(
            `/ratings/quotes/${quoteId}/user`
        );

        if (!response.ok) {
            return;
        }

        document
            .querySelectorAll(
                "#rating-stars button"
            )
            .forEach(button => {
                const value = Number(
                    button.dataset.rating
                );

                button.classList.toggle(
                    "active",
                    value <= Number(data.rating || 0)
                );
            });
    } catch (error) {
        console.error(error);
    }
}

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const registerForm = document.getElementById(
            "register-form"
        );

        if (!registerForm) {
            return;
        }

        registerForm.addEventListener(
            "submit",
            async event => {
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

                try {
                    const { response, data } =
                        await fetchJSON(
                            "/users/",
                            {
                                method: "POST",
                                body: JSON.stringify({
                                    username: username,
                                    password: password
                                })
                            }
                        );

                    if (!response.ok) {
                        message.textContent =
                            data.detail ||
                            "Ошибка регистрации.";

                        return;
                    }

                    saveUserSession(data);

                    window.location.href =
                        "/quotes-page";
                } catch (error) {
                    console.error(error);

                    message.textContent =
                        "Не удалось подключиться к серверу.";
                }
            }
        );
    }
);

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const loginForm = document.getElementById(
            "login-form"
        );

        if (!loginForm) {
            return;
        }

        loginForm.addEventListener(
            "submit",
            async event => {
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

                try {
                    const { response, data } =
                        await fetchJSON(
                            "/users/login",
                            {
                                method: "POST",
                                body: JSON.stringify({
                                    username: username,
                                    password: password
                                })
                            }
                        );

                    if (!response.ok) {
                        message.textContent =
                            data.detail ||
                            "Ошибка входа.";

                        return;
                    }

                    saveUserSession(data);

                    window.location.href =
                        "/quotes-page";
                } catch (error) {
                    console.error(error);

                    message.textContent =
                        "Не удалось подключиться к серверу.";
                }
            }
        );
    }
);

function saveUserSession(data) {
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
}

function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("username");

    window.location.href = "/";
}

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const logoutButton =
            document.getElementById(
                "logout-button"
            );

        const userInfo =
            document.getElementById(
                "user-info"
            );

        const loginLink =
            document.getElementById(
                "login-link"
            );

        const username =
            localStorage.getItem("username");

        if (logoutButton) {
            logoutButton.addEventListener(
                "click",
                logout
            );
        }

        if (username && getAccessToken()) {
            if (userInfo) {
                userInfo.textContent = username;
            }

            if (loginLink) {
                loginLink.style.display = "none";
            }

            if (logoutButton) {
                logoutButton.style.display =
                    "inline-block";
            }
        } else {
            if (userInfo) {
                userInfo.textContent = "";
            }

            if (logoutButton) {
                logoutButton.style.display = "none";
            }

            if (loginLink) {
                loginLink.style.display = "inline-block";
            }
        }
    }
);