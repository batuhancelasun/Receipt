<template>
  <div class="min-h-screen">
    <NavigationBar />
    
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-3xl font-bold text-white dark:text-white text-gray-900 mb-8">Settings</h1>
      
      <!-- Settings Navigation Tabs -->
      <div class="flex space-x-2 mb-8 overflow-x-auto">
        <button
          @click="activeTab = 'general'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-all flex items-center space-x-2',
            activeTab === 'general'
              ? 'bg-primary-600 text-white'
              : 'bg-white/10 text-gray-300 hover:bg-white/20'
          ]"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span>General</span>
        </button>
        <button
          v-if="authStore.user?.is_admin"
          @click="activeTab = 'users'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-all flex items-center space-x-2',
            activeTab === 'users'
              ? 'bg-primary-600 text-white'
              : 'bg-white/10 text-gray-300 hover:bg-white/20'
          ]"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <span>Users</span>
        </button>
      </div>
      
      <!-- General Settings Tab -->
      <div v-if="activeTab === 'general'" class="space-y-6 animate-fade-in">
        <!-- Gemini API Key -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <div class="flex items-center space-x-3 mb-4">
            <div class="p-2 bg-purple-500/20 rounded-lg">
              <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900">Gemini API Key</h3>
          </div>
          <input
            v-model="apiKey"
            type="password"
            placeholder="Enter your Gemini 2.0 Flash API key"
            class="w-full px-4 py-3 rounded-lg bg-white/5 dark:bg-white/5 bg-gray-100 border border-white/10 dark:border-white/10 border-gray-300 text-white dark:text-white text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
          />
          <p class="text-sm text-gray-400 mt-2">Required for AI receipt scanning</p>
        </div>
        
        <!-- Currency -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <div class="flex items-center space-x-3 mb-4">
            <div class="p-2 bg-green-500/20 rounded-lg">
              <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900">Default Currency</h3>
          </div>
          <select
            v-model="currency"
            class="w-full px-4 py-3 rounded-lg bg-white/5 dark:bg-white/5 bg-gray-100 border border-white/10 dark:border-white/10 border-gray-300 text-white dark:text-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
          >
            <option value="€">€ Euro</option>
            <option value="$">$ US Dollar</option>
            <option value="£">£ Pound</option>
            <option value="₺">₺ Turkish Lira</option>
            <option value="¥">¥ Yen/Yuan</option>
          </select>
        </div>
        
        <!-- Theme -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <div class="flex items-center space-x-3 mb-4">
            <div class="p-2 bg-blue-500/20 rounded-lg">
              <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900">Theme</h3>
          </div>
          <div class="flex space-x-4">
            <button
              @click="theme = 'dark'"
              :class="[
                'flex-1 py-3 rounded-lg font-medium transition-all flex items-center justify-center space-x-2',
                theme === 'dark'
                  ? 'bg-primary-600 text-white shadow-lg shadow-primary-600/30'
                  : 'bg-white/5 text-gray-300 hover:bg-white/10'
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
              <span>Dark</span>
            </button>
            <button
              @click="theme = 'light'"
              :class="[
                'flex-1 py-3 rounded-lg font-medium transition-all flex items-center justify-center space-x-2',
                theme === 'light'
                  ? 'bg-primary-600 text-white shadow-lg shadow-primary-600/30'
                  : 'bg-white/5 text-gray-300 hover:bg-white/10'
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              <span>Light</span>
            </button>
          </div>
        </div>
        
        <!-- Save Button -->
        <button
          @click="saveSettings"
          :disabled="saving"
          class="w-full py-3 bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white font-semibold rounded-lg transition-all disabled:opacity-50 shadow-lg shadow-primary-600/30"
        >
          {{ saving ? 'Saving...' : 'Save Settings' }}
        </button>
        
        <div v-if="message" :class="[
          'p-4 rounded-lg animate-fade-in',
          messageType === 'success' ? 'bg-green-500/20 border border-green-500/50' : 'bg-red-500/20 border border-red-500/50'
        ]">
          <p :class="messageType === 'success' ? 'text-green-200' : 'text-red-200'">{{ message }}</p>
        </div>
      </div>
      
      <!-- Users Tab (Admin Only) -->
      <div v-if="activeTab === 'users' && authStore.user?.is_admin" class="space-y-6 animate-fade-in">
        <!-- Create User Form -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <div class="flex items-center space-x-3 mb-6">
            <div class="p-2 bg-indigo-500/20 rounded-lg">
              <svg class="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900">Create New User</h3>
          </div>
          
          <form @submit.prevent="createUser" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 dark:text-gray-300 text-gray-700 mb-2">
                  Username
                </label>
                <input
                  v-model="newUser.username"
                  type="text"
                  required
                  minlength="3"
                  class="w-full px-4 py-3 rounded-lg bg-white/5 dark:bg-white/5 bg-gray-100 border border-white/10 dark:border-white/10 border-gray-300 text-white dark:text-white text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
                  placeholder="Enter username"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 dark:text-gray-300 text-gray-700 mb-2">
                  Email
                </label>
                <input
                  v-model="newUser.email"
                  type="email"
                  required
                  class="w-full px-4 py-3 rounded-lg bg-white/5 dark:bg-white/5 bg-gray-100 border border-white/10 dark:border-white/10 border-gray-300 text-white dark:text-white text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
                  placeholder="user@example.com"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 dark:text-gray-300 text-gray-700 mb-2">
                  Password
                </label>
                <input
                  v-model="newUser.password"
                  type="password"
                  required
                  minlength="8"
                  class="w-full px-4 py-3 rounded-lg bg-white/5 dark:bg-white/5 bg-gray-100 border border-white/10 dark:border-white/10 border-gray-300 text-white dark:text-white text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
                  placeholder="Minimum 8 characters"
                />
              </div>
              
              <div class="flex items-center">
                <label class="flex items-center cursor-pointer">
                  <input
                    v-model="newUser.is_admin"
                    type="checkbox"
                    class="w-5 h-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span class="ml-2 text-white dark:text-white text-gray-900">Grant admin privileges</span>
                </label>
              </div>
            </div>
            
            <div v-if="userError" class="bg-red-500/20 border border-red-500/50 rounded-lg p-3 animate-fade-in">
              <p class="text-red-200 text-sm">{{ userError }}</p>
            </div>
            
            <div v-if="userSuccess" class="bg-green-500/20 border border-green-500/50 rounded-lg p-3 animate-fade-in">
              <p class="text-green-200 text-sm">{{ userSuccess }}</p>
            </div>
            
            <button
              type="submit"
              :disabled="userLoading"
              class="px-6 py-3 bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white font-semibold rounded-lg transition-all disabled:opacity-50 shadow-lg shadow-primary-600/30"
            >
              {{ userLoading ? 'Creating...' : 'Create User' }}
            </button>
          </form>
        </div>
        
        <!-- Users List -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <div class="flex items-center space-x-3 mb-6">
            <div class="p-2 bg-cyan-500/20 rounded-lg">
              <svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900">All Users</h3>
          </div>
          
          <div v-if="users.length > 0" class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-white/10">
                  <th class="text-left py-3 px-4 text-gray-300 font-medium">Username</th>
                  <th class="text-left py-3 px-4 text-gray-300 font-medium">Email</th>
                  <th class="text-left py-3 px-4 text-gray-300 font-medium">Role</th>
                  <th class="text-right py-3 px-4 text-gray-300 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="user in users"
                  :key="user.id"
                  class="border-b border-white/5 hover:bg-white/5 transition-colors"
                >
                  <td class="py-3 px-4 text-white dark:text-white text-gray-900">{{ user.username }}</td>
                  <td class="py-3 px-4 text-gray-300 dark:text-gray-300 text-gray-700">{{ user.email }}</td>
                  <td class="py-3 px-4">
                    <span :class="[user.is_admin ? 'bg-purple-500/20 text-purple-300' : 'bg-gray-500/20 text-gray-300', 'px-2 py-1 rounded text-xs']">
                      {{ user.is_admin ? 'Admin' : 'User' }}
                    </span>
                  </td>
                  <td class="py-3 px-4 text-right">
                    <button
                      v-if="user.id !== currentUserId"
                      @click="deleteUser(user.id)"
                      class="px-3 py-1 bg-red-500/20 hover:bg-red-500/30 text-red-200 rounded text-sm transition-colors"
                    >
                      Delete
                    </button>
                    <span v-else class="text-gray-500 text-sm">Current User</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <p v-else class="text-gray-400 text-center py-8">No users found</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'
import { useThemeStore } from '../stores/theme'
import { useAuthStore } from '../stores/auth'
import NavigationBar from '../components/NavigationBar.vue'

const themeStore = useThemeStore()
const authStore = useAuthStore()

// Tab state
const activeTab = ref('general')

// General settings state
const apiKey = ref('')
const currency = ref('€')
const theme = ref('dark')
const saving = ref(false)
const message = ref('')
const messageType = ref('success')

// User management state
const newUser = ref({
  username: '',
  email: '',
  password: '',
  is_admin: false
})
const users = ref([])
const userLoading = ref(false)
const userError = ref('')
const userSuccess = ref('')

const currentUserId = computed(() => authStore.user?.id)

async function loadSettings() {
  try {
    const response = await api.get('/settings/')
    currency.value = response.data.default_currency
    theme.value = response.data.theme
    themeStore.setTheme(response.data.theme)
  } catch (error) {
    console.error('Failed to load settings:', error)
  }
}

async function saveSettings() {
  saving.value = true
  message.value = ''
  
  try {
    const updates = {
      default_currency: currency.value,
      theme: theme.value
    }
    
    if (apiKey.value) {
      updates.gemini_api_key = apiKey.value
    }
    
    await api.put('/settings/', updates)
    themeStore.setTheme(theme.value)
    
    message.value = 'Settings saved successfully!'
    messageType.value = 'success'
    apiKey.value = ''
  } catch (error) {
    message.value = 'Failed to save settings'
    messageType.value = 'error'
  } finally {
    saving.value = false
  }
}

async function fetchUsers() {
  try {
    const response = await api.get('/auth/admin/users')
    users.value = response.data
  } catch (err) {
    console.error('Failed to fetch users:', err)
  }
}

async function createUser() {
  userError.value = ''
  userSuccess.value = ''
  userLoading.value = true
  
  try {
    await api.post('/auth/admin/create-user', newUser.value)
    userSuccess.value = 'User created successfully!'
    
    newUser.value = {
      username: '',
      email: '',
      password: '',
      is_admin: false
    }
    
    await fetchUsers()
  } catch (err) {
    userError.value = err.response?.data?.detail || 'Failed to create user'
  } finally {
    userLoading.value = false
  }
}

async function deleteUser(userId) {
  if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
    return
  }
  
  try {
    await api.delete(`/auth/admin/users/${userId}`)
    await fetchUsers()
  } catch (err) {
    userError.value = err.response?.data?.detail || 'Failed to delete user'
  }
}

onMounted(() => {
  loadSettings()
  if (authStore.user?.is_admin) {
    fetchUsers()
  }
})
</script>
