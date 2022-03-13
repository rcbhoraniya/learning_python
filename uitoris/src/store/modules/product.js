import { httpServices } from "@/services"
// import { ProductService } from "@/services"
import { productURL } from '@/services/constants';


// initial state
export const product = {
    namespaced: true,
    state: {
        productall: [],
        product: {},
    },
    getters: {
        productListLength: (state) => {
            return state.productall.length
        }
    },
    actions: {
        getProducts: async(context) => {
            try {
                const response = await httpServices.getAll(productURL)
                context.commit('setProducts', response.data)
                return await Promise.resolve(response)
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error)
            }
        },

        getProductById: async(context, id) => {
            try {
                const response = await httpServices.get(productURL, id)
                context.commit('setProduct', response.data)
                return await Promise.resolve(response)
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error)
            }
        },

        addProduct: async(context, data) => {

            try {
                const response = await httpServices.create(productURL, data)
                context.commit('AddProduct', response.data)
                return await Promise.resolve(response)
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error)
            }
        },
        editProduct: async(context, data) => {
            // console.log("data", data);
            try {
                const response = await httpServices.update(productURL, data.id, data)
                    // console.log('res', response.data)
                context.commit('EditProduct', response.data)
                return await Promise.resolve(response)
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error)
            }
        },

        deleteProduct: async(context, id) => {
            try {
                const response = await httpServices.delete(productURL, id)
                console.log(response.data)
                context.commit('DeleteProduct', id)
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
        setProducts: (state, payload) => {
            state.productall = payload;
        },

        setProduct: (state, payload) => {
            state.product = payload;
        },

        AddProduct: (state, payload) => {
            state.productall.push(payload);
        },

        EditProduct: (state, payload) => {
            console.log(payload);
            const index = state.productall.findIndex(item => item.id === payload.id);
            if (index !== -1) state.productall.splice(index, 1, payload);
        },

        DeleteProduct: (state, payload) => {
            let index = state.productall.findIndex(item => item.id == payload)
            state.productall.splice(index, 1)
        },
        ClearState: (state) => {
            state.productall = [];
            state.product = {};
        },
    },
}