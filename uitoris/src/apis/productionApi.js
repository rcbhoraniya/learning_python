import Api from './Api'
const END_POINT = 'production/'


export default {
    getAll(params) {
        return Api.get(END_POINT, { params });
    },
    get(id) {
        return Api.get(`${END_POINT}${id}/`);
    },
    create(data) {
        return Api.post(END_POINT, data);
    },
    update(id, data) {
        return Api.put(`${END_POINT}${id}/`, data);
    },
    delete(id) {
        return Api.delete(`${END_POINT}${id}/`);
    },
}