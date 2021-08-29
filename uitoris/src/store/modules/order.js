import Order from "../../apis/orderApi"

// initial state
const state = {

    orderall: [],
    order: {},
};

// getters

const getters = {

    orderListLength: (state) => {
        return state.orderall.length
    }
}

// actions

const actions = {

    getOrders: (context) => {
        Order.getAll().then((response) => {
            context.commit('setOrders', response.data)
        }).catch(error => {
            console.log(error)
        })
    },

    getOrderById: (context, id) => {
        Order.get(id).then((response) => {
            context.commit('setOrder', response.data)
        }).catch(error => {
            console.log(error)
        })
    },

    addOrder: (context, data) => {

        Order.create(data).then(response => {
            context.commit('AddOrder', response.data)
        }).catch(error => {
            console.log(error)
        })
    },
    editOrder: (context, data) => {
        // console.log("data", data);
        Order.update(data.id, data).then(response => {
            // console.log('res', response.data)
            context.commit('EditOrder', response.data)

        }).catch(error => {
            console.log(error)
        })
    },

    deleteOrder(context, id) {
        Order.delete(id).then(response => {
            console.log(response.data);
            context.commit('DeleteOrder', id);

        }).catch(error => {
            console.log(error)
        })

    },
}

// mutations
const mutations = {

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
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}