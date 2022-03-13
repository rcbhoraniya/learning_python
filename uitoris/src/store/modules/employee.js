// import { EmployeeService } from "@/services"
import { httpServices } from "@/services"
import { employeeURL, stateURL, districtsURL } from '@/services/constants';
export const employee = {
    namespaced: true,
    state: {
        employeeall: [],
        employee: {},
        count: null,
        statesall: [],
        districtsall: [],
    },
    getters: {
        employeeOperator: (state) => {
            return state.employeeall.filter(item => item.designation_name === 'operator')
        }
    },
    actions: {
        getEmployees: async(context) => {
            try {
                const response = await httpServices.getAll(employeeURL)
                context.commit('setEmployees', response.data)
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
        getEmployeeById: async(context, id) => {
            try {
                const response = await httpServices.get(employeeURL, id);
                context.commit('setEmployee', response.data);
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }
        },
        addEmployee: async(context, data) => {
            const formData = new FormData();
            for (var key in data) {
                formData.append(key, data[key]);
            }
            console.log(formData)
            try {
                const response = await httpServices.create(employeeURL, formData);
                context.commit('AddEmployee', response.data);
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }
        },
        editEmployee: async(context, data) => {
            const formdata = new FormData();
            for (var key in data) {
                formdata.append(key, data[key]);
            }
            try {
                const response = await httpServices.update(employeeURL, data.id, formdata);
                // console.log('res', response.data)
                context.commit('EditEmployee', response.data);
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }
        },
        deleteEmployee: async(context, id) => {
            try {
                const response = await httpServices.delete(employeeURL, id);
                console.log(response.data);
                context.commit('DeleteEmployee', id);
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }
        },
        getStates: async(context) => {
            try {
                const response = await httpServices.getAll(stateURL)
                context.commit('setStates', response.data)
                return await Promise.resolve(response)
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error)
            }
        },
        getDistricts: async(context, state) => {
            console.log(state);
            try {
                const response = await httpServices.get_districts(districtsURL, state)
                context.commit('setDistricts', response.data)
                return await Promise.resolve(response)
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error)
            }
        },
    },
    mutations: {
        setEmployees: (state, payload) => {
            state.employeeall = payload;
        },

        setEmployee: (state, payload) => {
            state.employee = payload;
        },

        AddEmployee: (state, payload) => {
            state.employeeall.push(payload);
        },

        EditEmployee: (state, payload) => {
            const index = state.employeeall.findIndex(item => item.id === payload.id);
            if (index !== -1) state.employeeall.splice(index, 1, payload);
        },

        DeleteEmployee: (state, payload) => {
            let index = state.employeeall.findIndex(item => item.id == payload)
            state.employeeall.splice(index, 1)
        },
        setStates: (state, payload) => {
            state.statesall = payload;
        },
        setDistricts: (state, payload) => {
            state.districtsall = payload;
        },


        ClearState: (state) => {
            state.employeeall = [];
            state.employee = {};
            state.count = null;
        },
    }
}