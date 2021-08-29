import Plant from "../../apis/plantApi"

// initial state

const state = {

    plantall: [],
};

// getters

const getters = {

    plantAll: (state) => {
        return state.plantall
    }
}

// actions

const actions = {

    getPlants: ({ commit }) => {
        Plant.getAll().then((response) => {
            commit('setPlants', response.data)
        })
    },

}

// mutations

const mutations = {

    setPlants: (state, plants) => {
        state.plantall = plants;
    },

}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}