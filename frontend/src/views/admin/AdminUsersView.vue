<template>
  <div class="min-h-screen">
    <NavigationBar />
    
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-3xl font-bold text-white dark:text-white text-gray-900 mb-8">User Management</h1>
      
      <!-- Create User Form -->
      <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6 mb-8">
        <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-4">Create New User</h3>
        
        <form @submit.prevent="createUser" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-200 dark:text-gray-200 text-gray-700 mb-2">
                Username
              </label>
              <input
                v-model="newUser.username"
                type="text"
                required
                minlength="3"
                class="w-full px-4 py-3 rounded-lg bg-white/10 dark:bg-white/10 bg-gray-100 border border-white/20 dark:border-white/20 border-gray-300 text-white dark:text-white text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="Enter username"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-200 dark:text-gray-200 text-gray-700 mb-2">
                Email
              </label>
              <input
                v-model="newUser.email"
                type="email"
                required
                class="w-full px-4 py-3 rounded-lg bg-white/10 dark:bg-white/10 bg-gray-100 border border-white/20 dark:border-white/20 border-gray-300 text-white dark:text-white text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="user@example.com"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-200 dark:text-gray-200 text-gray-700 mb-2">
                Password
              </label>
              <input
                v-model="newUser.password"
                type="password"
                required
                minlength="8"
                class="w-full px-4 py-3 rounded-lg bg-white/10 dark:bg-white/10 bg-gray-100 border border-white/20 dark:border-white/20 border-gray-300 text-white dark:text-white text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
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
          
          <div v-if="error" class="bg-red-500/20 border border-red-500/50 rounded-lg p-3">
            <p class="text-red-200 text-sm">{{ error }}</p>
          </div>
          
          <div v-if="success" class="bg-green-500/20 border border-green-500/50 rounded-lg p-3">
            <p class="text-green-200 text-sm">{{ success }}</p>
          </div>
          
          <button
            type="submit"
            :disabled="loading"
            class="px-6 py-3 bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white font-semibold rounded-lg transition-all disabled:opacity-50"
          >
            {{ loading ? 'Creating...' : 'Create User' }}
          </button>
        </form>
      </div>
      
      <!-- Users List -->
      <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
        <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-4">All Users</h3>
        
        <div v-if="users.length > 0" class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-white/10">
                <th class="text-left py-3 px-4 text-gray-300 font-medium">Username</th>
                <th class="text-left py-3 px-4 text-gray-300 font-medium">Email</th>
                <th class="text-left py-3 px-4 text-gray-300 font-medium">Role</th>
                <th class="text-left py-3 px-4 text-gray-300 font-medium">Created</th>
                <th class="text-right py-3 px-4 text-gray-300 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="user in users"
                :key="user.id"
                class="border-b border-white/5 hover:bg-white/5 transition-colors"
              >
                <td class="py-3 px-4 text-white">{{ user.username }}</td>
                <td class="py-3 px-4 text-gray-300">{{ user.email }}</td>
                <td class="py-3 px-4">
                  <span :class="[user.is_admin ? 'bg-purple-500/20 text-purple-300' : 'bg-gray-500/20 text-gray-300', 'px-2 py-1 rounded text-xs']">
                    {{ user.is_admin ? 'Admin' : 'User' }}
                  </span>
                </td>
                <td class="py-3 px-4 text-gray-400 text-sm">
                  {{ new Date(user.created_at).toLocaleDateString() }}
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
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../../services/api'
import { useAuthStore } from '../../stores/auth'
import NavigationBar from '../../components/NavigationBar.vue'

const authStore = useAuthStore()

const newUser = ref({
  username: '',
  email: '',
  password: '',
  is_admin: false
})

const users = ref([])
const loading = ref(false)
const error = ref('')
const success = ref('')

const currentUserId = computed(() => authStore.user?.id)

async function createUser() {
  error.value = ''
  success.value = ''
  loading.value = true
  
  try {
    await api.post('/auth/admin/create-user', newUser.value)
    success.value = 'User created successfully!'
    
    // Reset form
    newUser.value = {
      username: '',
      email: '',
      password: '',
      is_admin: false
    }
    
    // Refresh user list
    await fetchUsers()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to create user'
  } finally {
    loading.value = false
  }
}

async function fetchUsers() {
  try {
    const response = await api.get('/auth/admin/users')
    users.value = response.data
  } catch (err) {
    console .error('Failed to fetch users:', err)
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
    error.value = err.response?.data?.detail || 'Failed to delete user'
  }
}

onMounted(() => {
  fetchUsers()
})
</script>
