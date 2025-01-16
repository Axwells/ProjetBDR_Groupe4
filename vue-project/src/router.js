import { createRouter, createWebHistory } from 'vue-router'

// Composants pour les différentes pages
import RegisterPage from './components/RegisterPage.vue'
import LoginPage from './components/LoginPage.vue'
import HomePage from './components/HomePage.vue'
import SearchPage from './components/SearchPage.vue' // Add this import
import BrandsPage from './components/BrandsPage.vue';

const routes = [
    {
        path: '/',
        name: 'Home',  // Changed path to '/' to match root
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
        component: SearchPage,  // Ensure you have a SearchPage component
    },
    {
        path: '/brands',
        name: 'Brands',
        component: BrandsPage,
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
