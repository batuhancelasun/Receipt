<template>
  <div class="min-h-screen">
    <NavigationBar />
    
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-3xl font-bold text-white dark:text-white text-gray-900 mb-8">Scan Receipt</h1>
      
      <div class="glass-dark dark:glass-dark glass-light rounded-xl p-8">
        <!-- Upload Area (Hidden when result exists) -->
        <div
          v-if="!result"
          class="space-y-4"
        >
          <!-- Hidden inputs -->
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            @change="handleFileSelect"
            class="hidden"
          />
          <input
            ref="cameraInput"
            type="file"
            accept="image/*"
            capture="environment"
            @change="handleFileSelect"
            class="hidden"
          />

          <!-- Mobile Quick Action (Take Photo) -->
          <div 
            @click="$refs.cameraInput.click()"
            class="group relative overflow-hidden glass-dark dark:glass-dark glass-light border border-primary-500/30 rounded-2xl p-6 text-center cursor-pointer hover:border-primary-500 transition-all active:scale-95 sm:hidden"
          >
            <div class="absolute inset-0 bg-primary-500/10 group-hover:bg-primary-500/20 transition-colors"></div>
            <div class="relative z-10">
              <div class="w-16 h-16 mx-auto mb-3 bg-primary-500/20 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                <svg class="w-8 h-8 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <p class="text-xl font-semibold text-white">Take Photo</p>
              <p class="text-sm text-gray-400 italic">Open camera instantly</p>
            </div>
          </div>

          <!-- Upload/Drop Area -->
          <div
            @drop.prevent="handleDrop"
            @dragover.prevent
            class="border-2 border-dashed border-white/20 rounded-2xl p-8 text-center cursor-pointer hover:border-primary-500/50 transition-colors group"
            @click="$refs.fileInput.click()"
          >
            <div v-if="!selectedFile">
              <div class="w-16 h-16 mx-auto mb-4 bg-white/5 rounded-xl flex items-center justify-center group-hover:bg-primary-500/10 transition-colors">
                <svg class="w-8 h-8 text-gray-400 group-hover:text-primary-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
              </div>
              <p class="text-lg text-gray-300 font-medium">Browse Gallery</p>
              <p class="text-xs text-gray-500 mt-1 hidden sm:block">or drop image here</p>
            </div>
            
            <div v-else class="py-4">
              <div class="flex items-center justify-center space-x-3">
                <div class="w-10 h-10 bg-primary-500/20 rounded-lg flex items-center justify-center">
                  <svg class="w-6 h-6 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <div class="text-left">
                  <p class="text-sm font-medium text-white truncate max-w-[200px]">{{ selectedFile.name }}</p>
                  <p class="text-xs text-gray-500">{{ (selectedFile.size / 1024 / 1024).toFixed(2) }} MB</p>
                </div>
                <button
                  @click.stop="selectedFile = null"
                  class="p-2 hover:bg-red-500/20 text-red-400 rounded-lg transition-colors"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <button
          v-if="selectedFile && !scanning && !result"
          @click="scanReceipt"
          class="w-full mt-6 py-3 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-lg transition-all"
        >
          Scan Receipt with AI
        </button>
        
        <!-- Scanning Loading State -->
        <div v-if="scanning" class="mt-6 text-center">
          <div class="flex items-center justify-center space-x-2">
            <svg class="w-5 h-5 text-primary-400 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p class="text-primary-400 animate-pulse">Scanning with Gemini 2.0 Flash...</p>
          </div>
        </div>
        
        <!-- Scanned Result Form -->
        <div v-if="result" class="mt-6 animate-fade-in">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900">Review & Edit</h3>
            <button 
              @click="resetScan"
              class="text-sm text-gray-400 hover:text-white transition-colors"
            >
              Cancel & Rescan
            </button>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <!-- Merchant -->
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">Merchant</label>
              <input 
                v-model="editForm.merchant_name"
                type="text"
                class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-primary-500"
              />
            </div>
            
            <!-- Category Selection -->
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">Category</label>
              <select 
                v-model="editForm.category_id"
                class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Select a Category</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                  {{ cat.name }}
                </option>
              </select>
            </div>
            
            <!-- Date -->
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">Date</label>
              <input 
                v-model="editForm.date"
                type="date"
                class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-primary-500"
              />
            </div>
            
            <!-- Total Amount -->
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1">Total Amount</label>
              <div class="relative">
                <span class="absolute left-3 top-3 text-gray-400">{{ editForm.currency }}</span>
                <input 
                  v-model.number="editForm.total_amount"
                  type="number"
                  step="0.01"
                  class="w-full pl-12 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>
          </div>
          
          <!-- Items List -->
          <div class="mb-6">
            <div class="flex items-center justify-between mb-2">
              <label class="block text-sm font-medium text-gray-300">Items</label>
              <button 
                @click="addItem"
                class="text-xs px-2 py-1 bg-primary-600/20 text-primary-300 rounded hover:bg-primary-600/30"
              >
                + Add Item
              </button>
            </div>
            
            <div class="space-y-2 max-h-60 overflow-y-auto pr-1">
              <div v-if="editForm.items.length === 0" class="text-gray-500 text-sm italic p-2 text-center border border-white/5 rounded-lg">
                No items detected
              </div>
              
              <div 
                v-for="(item, idx) in editForm.items" 
                :key="idx" 
                class="flex items-center space-x-2 bg-white/5 p-2 rounded-lg"
              >
                <input 
                  v-model="item.name"
                  type="text"
                  placeholder="Item Name"
                  class="flex-1 px-2 py-1 bg-transparent border-b border-white/10 text-white text-sm focus:border-primary-500 focus:outline-none"
                />
                <input 
                  v-model.number="item.quantity"
                  type="number"
                  step="0.1"
                  placeholder="Qty"
                  class="w-16 px-2 py-1 bg-transparent border-b border-white/10 text-white text-sm focus:border-primary-500 focus:outline-none"
                />
                <input 
                  v-model.number="item.total_price"
                  type="number"
                  step="0.01"
                  placeholder="Price"
                  class="w-20 px-2 py-1 bg-transparent border-b border-white/10 text-white text-sm focus:border-primary-500 focus:outline-none text-right"
                />
                <button 
                  @click="editForm.items.splice(idx, 1)"
                  class="text-red-400 hover:text-red-300 p-1"
                >
                  &times;
                </button>
              </div>
            </div>
            
            <div class="flex justify-end text-sm text-gray-400 mt-2">
              Calculated Total: {{ editForm.currency }}{{ calculateItemsTotal() }}
            </div>
          </div>
          
          <button
            @click="createTransaction"
            :disabled="creating"
            class="w-full py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-all disabled:opacity-50"
          >
            {{ creating ? 'Creating...' : 'Create Transaction' }}
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
import NavigationBar from '../components/NavigationBar.vue'

const router = useRouter()
const selectedFile = ref(null)
const scanning = ref(false)
const creating = ref(false)
const result = ref(null)
const error = ref('')
const categories = ref([])
const cameraInput = ref(null)
const fileInput = ref(null)

// Edit form state
const editForm = ref({
  merchant_name: '',
  date: '',
  total_amount: 0,
  currency: '€',
  category_id: '',
  items: []
})

onMounted(() => {
  fetchCategories()
})

async function fetchCategories() {
  try {
    const response = await api.get('/settings/categories')
    // Filter for expense categories only as receipts are expenses
    categories.value = response.data.filter(c => c.type === 'expense')
  } catch (err) {
    console.error('Failed to fetch categories', err)
  }
}

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

function resetScan() {
  selectedFile.value = null
  result.value = null
  error.value = ''
  editForm.value = {
    merchant_name: '',
    date: '',
    total_amount: 0,
    currency: '€',
    category_id: '',
    items: []
  }
}

function addItem() {
  editForm.value.items.push({
    name: 'New Item',
    quantity: 1,
    unit_price: 0,
    total_price: 0
  })
}

function calculateItemsTotal() {
  return editForm.value.items.reduce((sum, item) => sum + (parseFloat(item.total_price) || 0), 0).toFixed(2)
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
    
    // Check if scan status is failed but returned 200 (graceful error handling)
    if (response.data.scan_status === 'failed') {
      throw new Error(response.data.error_message || 'Scan failed')
    }
    
    result.value = response.data.extracted_data
    
    // Initialize edit form with scanned data
    const scanned = response.data.extracted_data
    
    // Normalize currency
    let currencySymbol = scanned.currency || '€'
    if (currencySymbol === 'EUR') currencySymbol = '€'
    if (currencySymbol === 'USD') currencySymbol = '$'
    if (currencySymbol === 'GBP') currencySymbol = '£'
    
    editForm.value = {
      merchant_name: scanned.merchant_name || '',
      date: scanned.date || new Date().toISOString().split('T')[0],
      total_amount: parseFloat(scanned.total_amount) || 0,
      currency: currencySymbol,
      category_id: '', // User must select
      items: (scanned.items || []).map(item => ({
        name: item.name,
        quantity: parseFloat(item.quantity) || 1,
        unit_price: parseFloat(item.unit_price) || 0,
        total_price: parseFloat(item.total_price) || 0
      }))
    }
    
  } catch (err) {
    error.value = err.message || err.response?.data?.detail || 'Failed to scan receipt. Make sure Gemini API key is configured in settings.'
  } finally {
    scanning.value = false
  }
}

async function createTransaction() {
  creating.value = true
  try {
    // Ensure date is in ISO format
    let transactionDate = editForm.value.date
    if (transactionDate) {
      transactionDate = new Date(transactionDate).toISOString()
    } else {
      transactionDate = new Date().toISOString()
    }
    
    // Clean up items
    const items = editForm.value.items.map(item => ({
      name: item.name || 'Unknown item',
      quantity: parseFloat(item.quantity) || 1.0,
      unit_price: parseFloat(item.unit_price) || 0,
      total_price: parseFloat(item.total_price) || 0
    }))
    
    await api.post('/transactions/', {
      type: 'expense',
      amount: parseFloat(editForm.value.total_amount) || 0,
      currency: editForm.value.currency || '€',
      merchant_name: editForm.value.merchant_name || 'Unknown',
      date: transactionDate,
      category_id: editForm.value.category_id || null,
      items: items,
      description: `Receipt from ${editForm.value.merchant_name || 'unknown store'}`
    })
    
    router.push('/transactions')
  } catch (err) {
    console.error('Transaction creation error:', err.response?.data || err)
    error.value = 'Failed to create transaction: ' + (err.response?.data?.detail || 'Unknown error')
  } finally {
    creating.value = false
  }
}
</script>
