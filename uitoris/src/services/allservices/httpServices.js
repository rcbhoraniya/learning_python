import Axios from '@/services/Api'

import { TokenService } from "@/services";

export const httpServices = {
    getAll,
    get,
    create,
    update,
    delete: del,
    start_reading,
    login,
    logout,
    register,
    tokenrefresh,
    productionReport,
    get_districts,
}

export const setupInterceptors = (store) => {
    Axios.interceptors.request.use(
        (config) => {
            const token = TokenService.getLocalAccessToken();
            if (token) {
                config.headers["Authorization"] = 'Bearer ' + token;
            }
            return config;
        },
        (error) => {
            return Promise.reject(error);
        }
    );

    Axios.interceptors.response.use(
        (res) => {
            return res;
        },
        async(err) => {
            const originalConfig = err.config;

            if (originalConfig.url !== "api-token/" && err.response) {
                // Access Token was expired
                if (err.response.status === 401 && !originalConfig._retry) {
                    originalConfig._retry = true;
                    await store.dispatch("auth/getRefreshToken", '');
                    return Axios(originalConfig);

                }
            }

            return Promise.reject(err);
        }
    );
}

function getAll(url, params) {
    return Axios.get(url, { params, });
}

function get(url, id) {
    return Axios.get(`${url}${id}/`);
}

function create(url, data) {
    // console.log(data);
    return Axios.post(url, data);
}

function update(url, id, data) {

    return Axios.put(`${url}${id}/`, data);
}

function del(url, id) {
    return Axios.delete(`${url}${id}/`);
}

function start_reading(url, plant) {
    // console.log(plant);
    return Axios.get(`${url}${plant}`);
}

function get_districts(url, state) {
    return Axios.get(`${url}${state}`);
}

function productionReport(url) {
    return Axios.get(url)
}

function login(url, user) {
    return Axios.post(url, {
        username: user.username,
        password: user.password
    });
}

function logout() {
    TokenService.removeUser();
}

function register(url, data) {
    return Axios.post(url, data);
}

function tokenrefresh(url, token) {
    return Axios.post(url, token);

}