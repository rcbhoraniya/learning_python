import http from "../http-common";

class TorislDataService {
    getAll() {
        return http.get("/production");
    }

    get(id) {
        return http.get(`/production/${id}`);
    }

    create(data) {
        return http.post("/production", data);
    }

    update(id, data) {
        return http.put(`/production/${id}`, data);
    }

    delete(id) {
        return http.delete(`/production/${id}`);
    }

    deleteAll() {
        return http.delete(`/production`);
    }

    findByTitle(title) {
        return http.get(`/production?title=${title}`);
    }
}

export default new class TorislDataService();