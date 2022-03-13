export const TokenService = {
    getLocalRefreshToken,
    getLocalAccessToken,
    updateLocalAccessToken,
    getUser,
    setUser,
    removeUser,
}

function getLocalRefreshToken() {
    const user = JSON.parse(localStorage.getItem("user"));
    if (user) { return user.refresh; } else { return null }
}

function getLocalAccessToken() {
    const user = JSON.parse(localStorage.getItem("user"));
    if (user) { return user.access; } else { return null }
}

function updateLocalAccessToken(token) {
    let user = JSON.parse(localStorage.getItem("user"));
    user.access = token;
    localStorage.setItem("user", JSON.stringify(user));
}

function getUser() {
    return JSON.parse(localStorage.getItem("user"));
}

function setUser(user) {

    localStorage.setItem("user", JSON.stringify(user));
}

function removeUser() {
    localStorage.removeItem("user");
}