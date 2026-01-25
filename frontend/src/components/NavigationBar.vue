<template>
  <nav class="glass-dark dark:glass-dark glass-light border-b border-white/10 sticky top-0 z-50 backdrop-blur-xl">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <div class="flex items-center space-x-8">
          <!-- Clickable Logo -->
          <router-link to="/" class="text-2xl font-bold text-white dark:text-white text-gray-900 hover:text-primary-400 transition-colors">
            <div class="flex items-center space-x-2">
              <img src="/receipt-logo.png" alt="Receipt Logo" class="w-8 h-8 object-contain invert dark:invert-0" />
              <span class="hidden sm:block">Receipt</span>
            </div>
          </router-link>
          
          <!-- Navigation Links -->
          <div class="hidden md:flex space-x-1">
            <router-link to="/" class="nav-link">
              <svg class="w-5 h-5 inline-block mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              Dashboard
            </router-link>
            <router-link to="/scan" class="nav-link">
              <svg class="w-5 h-5 inline-block mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Scan
            </router-link>
            <router-link to="/transactions" class="nav-link">
              <svg class="w-5 h-5 inline-block mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Transactions
            </router-link>
            <router-link to="/analytics" class="nav-link">
              <svg class="w-5 h-5 inline-block mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Analytics
            </router-link>
          </div>
        </div>
        
        <!-- Right Side Actions -->
        <div class="flex items-center space-x-3">
          <!-- Notifications -->
          <button
            @click="showNotifications = !showNotifications"
            class="relative p-2 rounded-lg hover:bg-white/10 transition-colors"
            title="Notifications"
          >
            <svg class="w-6 h-6 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            <span v-if="notificationCount > 0" class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
          
          <!-- Theme Toggle -->
          <button
            @click="themeStore.toggleTheme()"
            class="p-2 rounded-lg hover:bg-white/10 transition-colors"
            title="Toggle theme"
          >
            <svg v-if="themeStore.theme === 'dark'" class="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>
          
          <!-- Settings -->
          <router-link to="/settings" class="p-2 rounded-lg hover:bg-white/10 transition-colors">
            <svg class="w-6 h-6 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </router-link>
          
          <!-- Logout -->
          <button
            @click="handleLogout"
            class="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-200 dark:text-red-200 text-red-800 rounded-lg transition-colors text-sm font-medium flex items-center space-x-1.5"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span>Logout</span>
          </button>
        </div>
        <!-- Mobile Menu Button -->
        <button
          @click="showMobileMenu = !showMobileMenu"
          class="md:hidden p-2 rounded-lg text-gray-300 hover:bg-white/10"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div v-if="showMobileMenu" class="md:hidden glass-dark dark:glass-dark glass-light border-b border-white/10 animate-slide-down">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <router-link to="/" class="mobile-nav-link" @click="showMobileMenu = false">
          Dashboard
        </router-link>
        <router-link to="/scan" class="mobile-nav-link" @click="showMobileMenu = false">
          Scan Receipt
        </router-link>
        <router-link to="/transactions" class="mobile-nav-link" @click="showMobileMenu = false">
          Transactions
        </router-link>
        <router-link to="/analytics" class="mobile-nav-link" @click="showMobileMenu = false">
          Analytics
        </router-link>
        <div class="border-t border-white/10 my-2 pt-2">
           <router-link to="/settings" class="mobile-nav-link" @click="showMobileMenu = false">
            Settings
          </router-link>
          <button @click="handleLogout" class="mobile-nav-link text-red-400 w-full text-left">
            Logout
          </button>
        </div>
      </div>
    </div>
    
    <!-- Notification Dropdown -->
    <div v-if="showNotifications" class="absolute right-4 top-16 w-80 glass-dark dark:glass-dark glass-light rounded-xl shadow-2xl p-4 animate-scale-in z-50">
      <h3 class="text-lg font-semibold text-white dark:text-white text-gray-900 mb-3">Notifications</h3>
      <div v-if="notifications.length > 0" class="space-y-2 max-h-96 overflow-y-auto">
        <div v-for="notif in notifications" :key="notif.id" class="p-3 bg-white/5 rounded-lg">
          <p class="text-sm text-white  dark:text-white text-gray-900">{{ notif.message }}</p>
          <p class="text-xs text-gray-400 mt-1">{{ notif.time }}</p>
        </div>
      </div>
      <p v-else class="text-gray-400 text-sm text-center py-4">No notifications</p>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useThemeStore } from '../stores/theme'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const showNotifications = ref(false)
const showMobileMenu = ref(false)
const notifications = ref([]) // Will be populated from API

const notificationCount = computed(() => notifications.value.length)

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.nav-link {
  @apply px-3 py-2 rounded-lg text-gray-300 dark:text-gray-300 text-gray-700 hover:bg-white/10 transition-all font-medium flex items-center;
}

.nav-link.router-link-active {
  @apply bg-primary-600 text-white shadow-lg shadow-primary-600/30;
}

.mobile-nav-link {
  @apply block px-3 py-2 rounded-md text-base font-medium text-gray-300 dark:text-gray-300 text-gray-700 hover:bg-white/10 hover:text-white transition-colors;
}

.mobile-nav-link.router-link-active {
  @apply bg-primary-600 text-white;
}
</style>
