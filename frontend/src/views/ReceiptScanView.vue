<template>
  <div class="min-h-screen">
    <NavigationBar />
    
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-3xl font-bold text-white dark:text-white text-gray-900 mb-8">Scan Receipt</h1>
      
      <div class="glass-dark dark:glass-dark glass-light rounded-xl p-8">
        <div
          @drop.prevent="handleDrop"
          @dragover.prevent
          class="border-2 border-dashed border-white/30 rounded-xl p-12 text-center cursor-pointer hover:border-primary-500 transition-colors"
          @click="$refs.fileInput.click()"
        >
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            @change="handleFileSelect"
            class="hidden"
          />
          
          <div v-if="!selectedFile">
            <div class="w-20 h-20 mx-auto mb-4 bg-primary-500/20 rounded-2xl flex items-center justify-center">
              <svg class="w-10 h-10 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <p class="text-xl text-gray-300 mb-2">Drop receipt image here</p>
            <p class="text-sm text-gray-400">or click to browse</p>
          </div>
          
          <div v-else>
            <p class="text-lg text-primary-400 mb-4">{{ selectedFile.name }}</p>
            <button
              @click.stop="selectedFile = null"
              class="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-200 rounded-lg"
            >
              Remove
            </button>
          </div>
        </div>
        
        <button
          v-if="selectedFile && !scanning"
          @click="scanReceipt"
          class="w-full mt-6 py-3 bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white font-semibold rounded-lg transition-all"
        >
          Scan Receipt with AI
        </button>
        
        <div v-if="scanning" class="mt-6 text-center">
          <div class="flex items-center justify-center space-x-2">
            <svg class="w-5 h-5 text-primary-400 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p class="text-primary-400 animate-pulse">Scanning with Gemini 2.0 Flash...</p>
          </div>
        </div>
        
        <div v-if="result" class="mt-6 glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-4">Extracted Data</h3>
          <div class="space-y-3">
            <div><span class="text-gray-400">Store:</span> <span class="text-white ml-2">{{ result.merchant_name }}</span></div>
            <div><span class="text-gray-400">Date:</span> <span class="text-white ml-2">{{ result.date }}</span></div>
            <div><span class="text-gray-400">Total:</span> <span class="text-green-400 ml-2 font-mono text-lg">{{ result.currency }}{{ result.total_amount }}</span></div>
            <div v-if="result.confidence"><span class="text-gray-400">Confidence:</span> <span class="text-white ml-2">{{ (result.confidence * 100).toFixed(0) }}%</span></div>
          </div>
          
          <div v-if="result.items && result.items.length > 0" class="mt-4">
            <p class="text-gray-400 mb-2">Items:</p>
            <ul class="space-y-1">
              <li v-for="(item, idx) in result.items" :key="idx" class="text-sm text-gray-300">
                {{ item.name }} - {{ result.currency }}{{ item.total_price }}
              </li>
            </ul>
          </div>
          
          <button
            @click="createTransaction"
            class="w-full mt-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-all"
          >
            Create Transaction
          </button>
        </div>
        
        <div v-if="error" class="mt-6 bg-red-500/20 border border-red-500/50 rounded-lg p-4">
          <p class="text-red-200">{{ error }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
import NavigationBar from '../components/NavigationBar.vue'

const router = useRouter()
const selectedFile = ref(null)
const scanning = ref(false)
const result = ref(null)
const error = ref('')

function handleFileSelect(event) {
  selectedFile.value = event.target.files[0]
  result.value = null
  error.value = ''
}

function handleDrop(event) {
  selectedFile.value = event.dataTransfer.files[0]
  result.value = null
  error.value = ''
}

async function scanReceipt() {
  if (!selectedFile.value) return
  
  scanning.value = true
  error.value = ''
  
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    
    const response = await api.post('/receipts/scan', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    result.value = response.data.extracted_data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to scan receipt. Make sure Gemini API key is configured in settings.'
  } finally {
    scanning.value = false
  }
}

async function createTransaction() {
  try {
    await api.post('/transactions/', {
      type: 'expense',
      amount: result.value.total_amount,
      currency: result.value.currency || '€',
      merchant_name: result.value.merchant_name,
      date: result.value.date,
      items: result.value.items || []
    })
    
    router.push('/transactions')
  } catch (err) {
    error.value = 'Failed to create transaction'
  }
}
</script>
