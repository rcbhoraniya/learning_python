import Product from "../../apis/productApi"

// initial state

const state = {
    productall: [],
    product: {},
};

// getters

const getters = {

    productListLength: (state) => {
        return state.productall.length
    }
}

// actions

const actions = {

    getProducts: (context) => {
        Product.getAll().then((response) => {
            context.commit('setProducts', response.data)
        }).catch(error => {
            console.log(error)
        })
    },

    getProductById: (context, id) => {
        Product.get(id).then(response => {
            context.commit('setProduct', response.data)
        }).catch(error => {
            console.log(error)
        })
    },

    addProduct: (context, data) => {

        Product.create(data).then(response => {
            context.commit('AddProduct', response.data)
        }).catch(error => {
            console.log(error)
        })
    },
    editProduct: (context, data) => {
        // console.log("data", data);
        Product.update(data.id, data).then(response => {
            // console.log('res', response.data)
            context.commit('EditProduct', response.data)

        }).catch(error => {
            console.log(error)
        })
    },

    deleteProduct(context, id) {
        Product.delete(id).then(response => {
            console.log(response.data);
            context.commit('DeleteProduct', id);

        }).catch(error => {
            console.log(error)
        })

    },
}

// mutations

const mutations = {

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
        const index = state.productall.findIndex(item => item.id === payload.id);
        if (index !== -1) state.productall.splice(index, 1, payload);
    },

    DeleteProduct: (state, payload) => {
        let index = state.productall.findIndex(item => item.id == payload)
        state.productall.splice(index, 1)
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}