import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
    const token = ref(localStorage.getItem('auth_token') || null)
    const user = ref(null)

    const isAuthenticated = computed(() => !!token.value)

    async function login(username, password) {
        const response = await api.post('/auth/login', { username, password })
        token.value = response.data.access_token
        localStorage.setItem('auth_token', token.value)
        await fetchUser()
    }

    async function register(username, email, password) {
        const response = await api.post('/auth/register', { username, email, password })
        token.value = response.data.access_token
        localStorage.setItem('auth_token', token.value)
        await fetchUser()
    }

    async function fetchUser() {
        if (!token.value) return
        const response = await api.get('/auth/me')
        user.value = response.data
    }

    function logout() {
        token.value = null
        user.value = null
        localStorage.removeItem('auth_token')
    }

    return {
        token,
        user,
        isAuthenticated,
        login,
        register,
        fetchUser,
        logout
    }
})
