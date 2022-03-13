import Vue from 'vue';
import Vuex from 'vuex';
import { production } from '@/store/modules/production';
import { plant } from '@/store/modules/plant';
import { product } from '@/store/modules/product';
import { order } from '@/store/modules/order';
import { employee } from '@/store/modules/employee';
import { auth } from '@/store/modules/auth'
import { alert } from '@/store/modules/alert'
import { designation } from '@/store/modules/designation'
import { production_order } from '@/store/modules/productionOrder'
Vue.use(Vuex);

export default new Vuex.Store({

    modules: {
        designation,
        production,
        plant,
        product,
        order,
        employee,
        auth,
        alert,
        production_order,
    },

})