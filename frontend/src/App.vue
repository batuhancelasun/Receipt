<template>
  <div :class="themeStore.theme" class="min-h-screen transition-colors duration-150">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useThemeStore } from './stores/theme'
import { useAuthStore } from './stores/auth'

const themeStore = useThemeStore()
const authStore = useAuthStore()

onMounted(async () => {
  // Fetch user if token exists
  if (authStore.isAuthenticated) {
    try {
      await authStore.fetchUser()
    } catch (error) {
      console.error('Failed to fetch user:', error)
    }
  }
})
</script>
