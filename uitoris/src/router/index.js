import Vue from 'vue'
import VueRouter from 'vue-router'
import Production from '../views/Production.vue'
import Product from '../views/Product.vue'
import Order from '../views/Order.vue'
import About from '../views/About.vue'
import AddPlantProduction from "../components/AddPlantProduction.vue"
import EditPlantProduction from "../components/EditPlantProduction.vue"
import AddProduct from "../components/AddProduct.vue"
import EditProduct from "../components/EditProduct.vue"
import AddOrder from "../components/AddOrder.vue"
import EditOrder from "../components/EditOrder.vue"
Vue.use(VueRouter)

const routes = [{
        path: '/',
        name: 'Production',
        component: Production

    },
    {
        path: '/production',
        name: 'Production',
        component: Production

    },

    {
        path: '/production/add',
        name: 'ProductionAdd',
        component: AddPlantProduction
    },
    {
        path: '/production/:id',
        name: 'EditPlantProduction',
        component: EditPlantProduction,
        props: true,
    },
    {
        path: '/product',
        name: 'Product',
        component: Product
    },
    {
        path: '/product/add',
        name: 'ProductAdd',
        component: AddProduct
    },
    {
        path: '/product/:id',
        name: 'Product',
        component: EditProduct,
        props: true,
    },
    {
        path: '/order',
        name: 'Order',
        component: Order
    },
    {
        path: '/order/add',
        name: 'AddOrder',
        component: AddOrder
    },
    {
        path: '/order/:id',
        name: 'EditOrder',
        component: EditOrder,
        props: true,
    },
    {
        path: '/about',
        name: 'About',
        component: About
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router