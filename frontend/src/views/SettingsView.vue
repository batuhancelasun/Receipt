<template>
  <div class="min-h-screen p-8">
    <div class="max-w-2xl mx-auto">
      <h1 class="text-3xl font-bold text-white dark:text-white text-gray-900 mb-8">Settings</h1>
      
      <div class="space-y-6">
        <!-- Gemini API Key -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-4">Gemini API Key</h3>
          <input
            v-model="apiKey"
            type="password"
            placeholder="Enter your Gemini 2.0 Flash API key"
            class="w-full px-4 py-3 rounded-lg bg-white/10 dark:bg-white/10 bg-gray-100 border border-white/20 dark:border-white/20 border-gray-300 text-white dark:text-white text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
          <p class="text-sm text-gray-400 mt-2">Required for AI receipt scanning</p>
        </div>
        
        <!-- Currency -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-4">Default Currency</h3>
          <select
            v-model="currency"
            class="w-full px-4 py-3 rounded-lg bg-white/10 dark:bg-white/10 bg-gray-100 border border-white/20 dark:border-white/20 border-gray-300 text-white dark:text-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary-500"
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
          <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-4">Theme</h3>
          <div class="flex space-x-4">
            <button
              @click="theme = 'dark'"
              :class="[
                'flex-1 py-3 rounded-lg font-medium transition-all',
                theme === 'dark'
                  ? 'bg-primary-600 text-white'
                  : 'bg-white/10 text-gray-300 hover:bg-white/20'
              ]"
            >
              🌙 Dark
            </button>
            <button
              @click="theme = 'light'"
              :class="[
                'flex-1 py-3 rounded-lg font-medium transition-all',
                theme === 'light'
                  ? 'bg-primary-600 text-white'
                  : 'bg-white/10 text-gray-300 hover:bg-white/20'
              ]"
            >
              ☀️ Light
            </button>
          </div>
        </div>
        
        <!-- Save Button -->
        <button
          @click="saveSettings"
          :disabled="saving"
          class="w-full py-3 bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white font-semibold rounded-lg transition-all disabled:opacity-50"
        >
          {{ saving ? 'Saving...' : 'Save Settings' }}
        </button>
        
        <div v-if="message" :class="[
          'p-4 rounded-lg',
          messageType === 'success' ? 'bg-green-500/20 border border-green-500/50' : 'bg-red-500/20 border border-red-500/50'
        ]">
          <p :class="messageType === 'success' ? 'text-green-200' : 'text-red-200'">{{ message }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { useThemeStore } from '../stores/theme'

const themeStore = useThemeStore()

const apiKey = ref('')
const currency = ref('€')
const theme = ref('dark')
const saving = ref(false)
const message = ref('')
const messageType = ref('success')

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

onMounted(() => {
  loadSettings()
})
</script>
