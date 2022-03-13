import Vue from 'vue'
import Router from 'vue-router'
import Production from '@/views/Production.vue'
import Product from '@/views/Product.vue'
import Order from '@/views/Order.vue'
import About from '@/views/About.vue'
import Login from '@/views/Login.vue'
import Registration from '@/views/Registration.vue'
import AddPlantProduction from "@/components/AddPlantProduction.vue"
import EditPlantProduction from "@/components/EditPlantProduction.vue"
import AddProduct from "@/components/AddProduct.vue"
import EditProduct from "@/components/EditProduct.vue"
import AddOrder from "@/components/AddOrder.vue"
import EditOrder from "@/components/EditOrder.vue"
import Employee from "@/views/Employee"
import AddEmployee from "@/components/AddEmployee.vue"
import EditEmployee from "@/components/EditEmployee.vue"
import ProductionOrder from '@/components/table/ProductionOrder'
import NotFoundComponent from "@/components/Notfound.vue"
Vue.use(Router)

const router = new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [{
            path: '/',
            name: 'production',
            component: Production

        },
        {
            path: '/login',
            name: 'Login',
            component: Login

        },
        {
            path: '/registration',
            name: 'Registration',
            component: Registration

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
            name: 'EditProduct',
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
            path: '/employee',
            name: 'Employee',
            component: Employee
        },
        {
            path: '/employee/add',
            name: 'AddEmployee',
            component: AddEmployee
        },
        {
            path: '/employee/:id',
            name: 'EditEmployee',
            component: EditEmployee,
            props: true,
        },

        {
            path: '/about',
            name: 'About',
            component: About
        },
        {
            path: '/production_order',
            name: 'ProductionOrder',
            component: ProductionOrder

        },
        {
            path: '/:catchAll(.*)',
            component: NotFoundComponent,
            name: 'NotFound'
        }
    ]
});

router.beforeEach((to, from, next) => {
    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['/login', '/about', '/registration'];
    const authRequired = !publicPages.includes(to.path);
    const loggedIn = localStorage.getItem('user');

    if (authRequired && !loggedIn) {
        return next({ name: 'Login' });
    }

    next();
})
export default router;