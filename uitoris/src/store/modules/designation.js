import { httpServices } from "@/services"
import { designationURL } from "@/services/constants";

export const designation = {
    namespaced: true,
    state: {
        designationall: [],
        designation: {},
        count: null,
    },
    getters: {
        designationAll: (state) => {
            return state.designationall
        }
    },
    actions: {
        getDesignations: async(context) => {
            try {
                const response = await httpServices.getAll(designationURL)
                context.commit('setDesignations', response.data)
                return await Promise.resolve(response)
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error)
            }
        },
        clearState(context) {
            context.commit('ClearState');
        },
        getDesignationById: async(context, id) => {
            try {
                const response = await httpServices.get(designationURL, id);
                context.commit('setDesignation', response.data);
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }
        },

        addDesignation: async(context, data) => {

            try {
                const response = await httpServices.create(designationURL, data);
                context.commit('AddDesignation', response.data);
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }
        },
        editDesignation: async(context, data) => {
            // console.log("data", data);
            try {
                const response = await httpServices.update(designationURL, data.id, data);
                // console.log('res', response.data)
                context.commit('EditDesignation', response.data);
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }
        },

        deleteDesignation: async(context, id) => {

            try {
                const response = await httpServices.delete(designationURL, id);
                console.log(response.data);
                context.commit('DeleteDesignation', id);
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }

        },


    },
    mutations: {
        setDesignations: (state, payload) => {
            state.designationall = payload;
        },

        setDesignation: (state, payload) => {
            state.designation = payload;
        },

        AddDesignation: (state, payload) => {
            state.designationall.push(payload);
        },

        EditDesignation: (state, payload) => {
            const index = state.designationall.findIndex(item => item.id === payload.id);
            if (index !== -1) state.designationall.splice(index, 1, payload);
        },

        DeleteDesignation: (state, payload) => {
            let index = state.designationall.findIndex(item => item.id == payload)
            state.designationall.splice(index, 1)
        },
        ClearState: (state) => {
            state.designationall = [];
            state.designation = {};
            state.count = null;
        },


    }
}