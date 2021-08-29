const routes = [
    {path:'/home',component:plant_production},
    {path:'/product',component:product},
    {path:'/order',component:order},
]

const router = new VueRouter({
    routes
})

const app = new Vue({
    router
}).$mount('#app')