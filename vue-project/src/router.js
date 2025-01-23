import { createRouter, createWebHistory } from 'vue-router'

// Composants pour les différentes pages
import RegisterPage from './components/RegisterPage.vue'
import LoginPage from './components/LoginPage.vue'
import HomePage from './components/HomePage.vue'
import SearchPage from './components/SearchPage.vue'
import BrandsPage from './components/BrandsPage.vue'
import CarsPage from './components/CarsPage.vue'
import SpecsPage from './components/SpecsPage.vue'
import AdminModificationsPage from './components/AdminModifications.vue'
import AdminUsersPage from './components/AdminUsersPage.vue';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomePage,
    },
    {
        path: '/register',
        name: 'Register',
        component: RegisterPage,
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginPage,
    },
    {
        path: '/search',
        name: 'Search',
        component: SearchPage,
    },
    {
        path: '/brands',
        name: 'Brands',
        component: BrandsPage,
    },
    {
        path: "/specs/:modelName",
        name: "SpecsPage",
        component: SpecsPage,
    },
    {
        path: "/search/results",
        name: "CarsPage",
        component: CarsPage,
    },
    {
        path: '/admin/modifications',
        name: 'AdminModifications',
        component: AdminModificationsPage,
      },
      {
        path: '/admin/users',
        name: 'AdminUsers',
        component: AdminUsersPage,
      },
];

const router = createRouter({
    history: createWebHistory(),
    routes
})



export default router


