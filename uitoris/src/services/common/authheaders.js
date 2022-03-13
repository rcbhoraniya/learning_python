export default function authHeader() {
    let user = JSON.parse(localStorage.getItem('user'));
    // console.log(user.access);
    if (user && user.access) {
        return { Authorization: 'Bearer ' + user.access };
    } else {
        return {};
    }
}