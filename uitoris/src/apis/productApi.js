import Api from './Api'
const END_POINT = 'product/'


export default {
    getAll() {
        return Api.get(END_POINT);
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