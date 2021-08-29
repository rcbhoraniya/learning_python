import Operator from "../../apis/operatorAPI"

// initial state

const state = {
    operatorall: [],
};

// getters

const getters = {
    operatorAll: (state) => {
        return state.operatorall
    }
}

// actions

const actions = {

    getOperators: ({ commit }) => {
        Operator.getAll().then((response) => {
            commit('setOperators', response.data)
        })
    },
}

// mutations

const mutations = {

    setOperators: (state, operators) => {
        state.operatorall = operators;
    },

}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}