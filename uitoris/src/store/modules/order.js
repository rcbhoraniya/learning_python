// import { OrderService } from "@/services"
import { httpServices } from "@/services"
// import { ProductService } from "@/services"
import { orderURL } from '@/services/constants';

export const order = {
    namespaced: true,
    state: {
        orderall: [],
        order: {},
    },
    getters: {
        orderListLength: (state) => {
            return state.orderall.length
        }
    },
    actions: {
        getOrders: async(context) => {
            try {
                const response = await httpServices.getAll(orderURL)
                context.commit('setOrders', response.data)
                return await Promise.resolve(response)
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error)
            }
        },

        getOrderById: async(context, id) => {
            try {
                const response = await httpServices.get(orderURL, id)
                context.commit('setOrder', response.data)
                return await Promise.resolve(response)
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error)
            }
        },

        addOrder: async(context, data) => {

            try {
                const response = await httpServices.create(orderURL, data)
                context.commit('AddOrder', response.data)
                return await Promise.resolve(response)
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error)
            }
        },
        editOrder: async(context, data) => {
            // console.log("data", data);
            try {
                const response = await httpServices.update(orderURL, data.id, data)
                    // console.log('res', response.data)
                context.commit('EditOrder', response.data)
                return await Promise.resolve(response)
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error)
            }
        },

        async deleteOrder(context, id) {
            try {
                const response = await httpServices.delete(orderURL, id)
                console.log(response.data)
                context.commit('DeleteOrder', id)
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
    },

    mutations: {

        setOrders: (state, payload) => {
            state.orderall = payload;
        },

        setOrder: (state, payload) => {
            state.order = payload;
        },

        AddOrder: (state, payload) => {
            state.orderall.push(payload);
        },

        EditOrder: (state, payload) => {
            const index = state.orderall.findIndex(item => item.id === payload.id);
            if (index !== -1) state.orderall.splice(index, 1, payload);
        },

        DeleteOrder: (state, payload) => {
            let index = state.orderall.findIndex(item => item.id == payload)
            state.orderall.splice(index, 1)
        },
        ClearState: (state) => {
            state.orderall = [];
            state.order = {};
        },
    },
}