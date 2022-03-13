import { httpServices } from "@/services"
import { productionOrdertURL } from '@/services/constants';
// initial state
export const production_order = {
    namespaced: true,
    state: {
        production_order: [],
    },

    actions: {

        getProductionOrder: async(context) => {
            try {
                const response = await httpServices.productionReport(productionOrdertURL)
                context.commit('setProductionOrder', response.data)
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
        setProductionOrder: (state, payload) => {
            state.production_order = payload;
        },
        ClearState: (state) => {
            state.production_order = [];
        },
    },
}