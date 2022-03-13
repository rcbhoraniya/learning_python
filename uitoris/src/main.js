import Vue from 'vue'
import App from '@/App.vue'
import router from '@/router'
import store from '@/store'
import Vuelidate from 'vuelidate';
import 'bootstrap'
import moment from 'moment'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserSecret } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import titleMixin from '@/mixins/titleMixin'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'bootstrap-vue/dist/bootstrap-vue-icons.min.css'
import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'
import { setupInterceptors } from '@/services';
import '@/assets/styles.scss'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
library.add(faUserSecret)

setupInterceptors(store);
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.component(Navbar.name, Navbar)
Vue.component(Footer.name, Footer)
Vue.use(BootstrapVue)
Vue.use(Vuelidate);
Vue.use(IconsPlugin)
Vue.filter('formatDate', function(value) {
    if (value) {
        return moment(String(value)).format('DD/MM/YYYY')
    }
});
Vue.mixin(titleMixin)

Vue.config.productionTip = false

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')