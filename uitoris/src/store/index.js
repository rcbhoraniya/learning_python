import Vue from 'vue';
import Vuex from 'vuex';
import production from './modules/production';
import plant from './modules/plant';
import product from './modules/product';
import order from './modules/order';
import operator from './modules/operator';


Vue.use(Vuex);

export default new Vuex.Store({

    modules: {
        production,
        plant,
        product,
        order,
        operator,
    },

})