import { httpServices } from "@/services"
import { plantURL } from '@/services/constants';
// initial state
export const plant = {
    namespaced: true,
    state: {
        plantall: [],
    },
    getters: {
        plantAll: (state) => {
            return state.plantall
        }
    },
    actions: {

        getPlants: async(context) => {
            try {
                const response = await httpServices.getAll(plantURL)
                context.commit('setPlants', response.data)
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
        setPlants: (state, plants) => {
            state.plantall = plants;
        },
        ClearState: (state) => {
            state.plantall = [];
        },
    },
}