import { httpServices } from "@/services"
import { productionURL, lastreadingURL } from '@/services/constants';

// initial state

export const production = {
    namespaced: true,
    state: {
        productionall: [],
        production: {},
        startreadingItem: {},
        count: null,
    },
    getters: {
        productionListLength: (state) => {
            return state.productionall.length
        },
        getStartreading: (state) => {
            return state.startreadingItem.end_reading
        },
    },
    actions: {
        async getProductions(context, params) {
            try {
                const response = await httpServices.getAll(productionURL, params);
                if (response.data.results) {
                    context.commit('setProductions', response.data.results)
                    context.commit('setCount', response.data.count)
                } else { context.commit('setProductions', response.data) }
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }
        },

        getProductionById: async(context, id) => {
            try {
                const response = await httpServices.get(productionURL, id);
                context.commit('setProduction', response.data);
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }
        },

        addProduction: async(context, data) => {

            try {
                const response = await httpServices.create(productionURL, data);
                context.commit('AddProduction', response.data);
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }
        },
        editProduction: async(context, data) => {
            console.log("data", data);
            try {
                const response = await httpServices.update(productionURL, data.id, data);
                // console.log('res', response.data)
                context.commit('EditProduction', response.data);
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }
        },

        deleteProduction: async(context, id) => {

            try {
                const response = await httpServices.delete(productionURL, id);
                console.log(response.data);
                context.commit('DeleteProduction', id);
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }

        },
        clearStartReading(context) {
            context.commit('ClearStartReading');
        },
        clearState(context) {
            context.commit('ClearState');
        },
        clearStateStartReading(context) {
            context.commit('ClearStateStartReading');
        },
        getStartReading: async(context, plant) => {
            try {
                // console.log(plant);
                const response = await httpServices.start_reading(lastreadingURL, plant);
                context.commit('setStartReading', response.data);
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }
        },
    },
    mutations: {
        setCount: (state, payload) => {
            state.count = payload;
        },
        setProductions: (state, payload) => {
            state.productionall = payload;
        },

        setProduction: (state, payload) => {
            state.production = payload;
        },

        AddProduction: (state, payload) => {
            state.productionall.push(payload);
        },

        EditProduction: (state, payload) => {
            const index = state.productionall.findIndex(item => item.id === payload.id);
            if (index !== -1) state.productionall.splice(index, 1, payload);
        },

        DeleteProduction: (state, payload) => {
            let index = state.productionall.findIndex(item => item.id == payload)
            state.productionall.splice(index, 1)
        },
        ClearState: (state) => {
            state.productionall = [];
            state.production = {};
            state.startreadingItem = {};
            state.count = null;
        },
        ClearStateStartReading: (state) => {
            state.startreadingItem = {};
        },
        setStartReading: (state, payload) => {
            state.startreadingItem = payload;
        },
        ClearStartReading: (state) => {
            state.startreadingItem = {}
        }

    },
}