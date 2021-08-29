import Production from "../../apis/productionApi"

// initial state

const state = {
    productionall: [],
    production: {},
    count: null,
    // next: "",
};

// getters

const getters = {
    productionListLength: (state) => {
        return state.productionall.length
    },

    getProductionByPlant: (state) => (plant) => {
        // it's an example
        // console.log(plant);
        // console.log(state.productionall);
        return state.productionall.filter((item) => item.plant === plant.plant).sort((a, b) => parseFloat(a.end_reading) - parseFloat(b.end_reading))
            .slice(-1)[0];
    }

}

// actions

const actions = {

    getProductions: (context, params) => {
        console.log(params);
        Production.getAll(params).then(response => {
            if (response.data.results) {
                context.commit('setProductions', response.data.results)
                context.commit('setCount', response.data.count)
            } else {
                context.commit('setProductions', response.data)
                    // context.commit('setCount', response.data.length)
            }

        }).catch(error => {
            console.log(error)
        })
    },

    getProductionById: (context, id) => {
        Production.get(id).then(response => {
            context.commit('setProduction', response.data)
        }).catch(error => {
            console.log(error)
        })
    },

    addProduction: (context, data) => {

        Production.create(data).then(response => {
            context.commit('AddProduction', response.data)
        }).catch(error => {
            console.log(error)
        })
    },
    editProduction: (context, data) => {
        // console.log("data", data);
        Production.update(data.id, data).then(response => {
            // console.log('res', response.data)
            context.commit('EditProduction', response.data)

        }).catch(error => {
            console.log(error)
        })
    },

    deleteProduction(context, id) {
        console.log(id);
        Production.delete(id).then(response => {
            console.log(response.data);
            context.commit('DeleteProduction', id);

        }).catch(error => {
            console.log(error)
        })

    },
}

// mutations

const mutations = {
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
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}