import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Lazy load views
const LoginView = () => import('../views/auth/LoginView.vue')
const DashboardView = () => import('../views/DashboardView.vue')
const AnalyticsView = () => import('../views/AnalyticsView.vue')
const ReceiptScanView = () => import('../views/ReceiptScanView.vue')
const TransactionsView = () => import('../views/TransactionsView.vue')
const SettingsView = () => import('../views/SettingsView.vue')
const AdminUsersView = () => import('../views/admin/AdminUsersView.vue')

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: LoginView,
        meta: { guest: true }
    },
    {
        path: '/',
        name: 'Dashboard',
        component: DashboardView,
        meta: { requiresAuth: true }
    },
    {
        path: '/analytics',
        name: 'Analytics',
        component: AnalyticsView,
        meta: { requiresAuth: true }
    },
    {
        path: '/scan',
        name: 'ReceiptScan',
        component: ReceiptScanView,
        meta: { requiresAuth: true }
    },
    {
        path: '/transactions',
        name: 'Transactions',
        component: TransactionsView,
        meta: { requiresAuth: true }
    },
    {
        path: '/settings',
        name: 'Settings',
        component: SettingsView,
        meta: { requiresAuth: true }
    },
    {
        path: '/admin/users',
        name: 'AdminUsers',
        component: AdminUsersView,
        meta: { requiresAuth: true, requiresAdmin: true }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login')
    } else if (to.meta.guest && authStore.isAuthenticated) {
        next('/')
    } else if (to.meta.requiresAdmin) {
        // Check if user is admin
        if (!authStore.user) {
            await authStore.fetchUser()
        }
        if (!authStore.user?.is_admin) {
            next('/')
        } else {
            next()
        }
    } else {
        next()
    }
})

export default router
