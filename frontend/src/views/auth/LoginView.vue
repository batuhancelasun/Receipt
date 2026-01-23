<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="glass-dark dark:glass-dark glass-light w-full max-w-md p-8 rounded-2xl shadow-2xl animate-scale-in">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-white dark:text-white text-gray-900 mb-2">Receipt</h1>
        <p class="text-gray-300 dark:text-gray-300 text-gray-600">AI-Powered Expense Tracking</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-200 dark:text-gray-200 text-gray-700 mb-2">
            Username
          </label>
          <input
            v-model="username"
            type="text"
            required
            class="w-full px-4 py-3 rounded-lg bg-white/10 dark:bg-white/10 bg-gray-100 border border-white/20 dark:border-white/20 border-gray-300 text-white dark:text-white text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
            placeholder="Enter your username"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-200 dark:text-gray-200 text-gray-700 mb-2">
            Password
          </label>
          <input
            v-model="password"
            type="password"
            required
            class="w-full px-4 py-3 rounded-lg bg-white/10 dark:bg-white/10 bg-gray-100 border border-white/20 dark:border-white/20 border-gray-300 text-white dark:text-white text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
            placeholder="Enter your password"
          />
        </div>
        
        <div v-if="error" class="bg-red-500/20 border border-red-500/50 rounded-lg p-3">
          <p class="text-red-200 text-sm">{{ error }}</p>
        </div>
        
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-3 px-4 bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white font-semibold rounded-lg transition-all transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
        >
          <span v-if="!loading">Sign In</span>
          <span v-else>Signing in...</span>
        </button>
      </form>
      
      <div class="mt-6 text-center">
        <p class="text-gray-300 dark:text-gray-300 text-gray-600 text-sm">
          Don't have an account?
          <router-link to="/register" class="text-primary-400 hover:text-primary-300 font-semibold">
            Register
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  
  try {
    await authStore.login(username.value, password.value)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
