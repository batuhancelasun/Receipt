<template>
  <div class="min-h-screen">
    <NavigationBar />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-bold text-white dark:text-white text-gray-900">Transactions</h1>
        <button
          @click="showAddForm = !showAddForm"
          class="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-xl font-medium transition-all shadow-lg shadow-primary-600/30 flex items-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>{{ showAddForm ? 'Cancel' : 'Add Transaction' }}</span>
        </button>
      </div>
      
      <!-- Add Transaction Form -->
      <div v-if="showAddForm" class="glass-dark dark:glass-dark glass-light rounded-2xl p-6 mb-8 animate-fade-in">
        <h2 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-6">New Transaction</h2>
        
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Type Selection -->
            <div>
              <label class="block text-sm font-medium text-gray-300 dark:text-gray-300 text-gray-700 mb-2">Type</label>
              <div class="flex space-x-3">
                <button
                  type="button"
                  @click="form.type = 'expense'"
                  :class="[
                    'flex-1 py-3 px-4 rounded-lg font-medium transition-all',
                    form.type === 'expense'
                      ? 'bg-red-500 text-white shadow-lg shadow-red-500/30'
                      : 'bg-white/5 dark:bg-white/5 bg-gray-100/50 text-gray-300 dark:text-gray-300 text-gray-700  hover:bg-white/10'
                  ]"
                >
                  Expense
                </button>
                <button
                  type="button"
                  @click="form.type = 'income'"
                  :class="[
                    'flex-1 py-3 px-4 rounded-lg font-medium transition-all',
                    form.type === 'income'
                      ? 'bg-green-500 text-white shadow-lg shadow-green-500/30'
                      : 'bg-white/5 dark:bg-white/5 bg-gray-100/50 text-gray-300 dark:text-gray-300 text-gray-700 hover:bg-white/10'
                  ]"
                >
                  Income
                </button>
              </div>
            </div>
            
            <!-- Amount -->
            <div>
              <label class="block text-sm font-medium text-gray-300 dark:text-gray-300 text-gray-700 mb-2">Amount</label>
              <input
                v-model.number="form.amount"
                type="number"
                step="0.01"
                required
                class="w-full px-4 py-3 bg-white/5 dark:bg-white/5 bg-gray-100/50 border border-white/10 rounded-lg text-white dark:text-white text-gray-900 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                placeholder="0.00"
              />
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Description -->
            <div>
              <label class="block text-sm font-medium text-gray-300 dark:text-gray-300 text-gray-700 mb-2">Description</label>
              <input
                v-model="form.description"
                type="text"
                required
                class="w-full px-4 py-3 bg-white/5 dark:bg-white/5 bg-gray-100/50 border border-white/10 rounded-lg text-white dark:text-white text-gray-900 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                placeholder="e.g., Grocery shopping"
              />
            </div>
            
            <!-- Date -->
            <div>
              <label class="block text-sm font-medium text-gray-300 dark:text-gray-300 text-gray-700 mb-2">Date</label>
              <input
                v-model="form.date"
                type="date"
                required
                class="w-full px-4 py-3 bg-white/5 dark:bg-white/5 bg-gray-100/50 border border-white/10 rounded-lg text-white dark:text-white text-gray-900 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Category -->
            <div>
              <label class="block text-sm font-medium text-gray-300 dark:text-gray-300 text-gray-700 mb-2">Category (optional)</label>
              <select
                v-model="form.category_id"
                class="w-full px-4 py-3 bg-white/5 dark:bg-white/5 bg-gray-100/50 border border-white/10 rounded-lg text-white dark:text-white text-gray-900 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              >
                <option value="">No category</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
              </select>
            </div>
            
            <!-- Currency -->
            <div>
              <label class="block text-sm font-medium text-gray-300 dark:text-gray-300 text-gray-700 mb-2">Currency</label>
              <input
                v-model="form.currency"
                type="text"
                maxlength="3"
                class="w-full px-4 py-3 bg-white/5 dark:bg-white/5 bg-gray-100/50 border border-white/10 rounded-lg text-white dark:text-white text-gray-900 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                placeholder="€"
              />
            </div>
          </div>
          
          <!-- Notes -->
          <div>
            <label class="block text-sm font-medium text-gray-300 dark:text-gray-300 text-gray-700 mb-2">Notes (optional)</label>
            <textarea
              v-model="form.notes"
              rows="3"
              class="w-full px-4 py-3 bg-white/5 dark:bg-white/5 bg-gray-100/50 border border-white/10 rounded-lg text-white dark:text-white text-gray-900 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
              placeholder="Additional notes..."
            ></textarea>
          </div>
          
          <!-- Submit Button -->
          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="showAddForm = false"
              class="px-6 py-3 bg-white/5 hover:bg-white/10 text-gray-300 rounded-lg font-medium transition-all"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="submitting"
              class="px-6 py-3 bg-primary-600 hover:bg-primary-700 disabled:bg-primary-600/50 text-white rounded-lg font-medium transition-all shadow-lg shadow-primary-600/30"
            >
              {{ submitting ? 'Saving...' : 'Save Transaction' }}
            </button>
          </div>
        </form>
      </div>
      
      <!-- Transactions List -->
      <div class="glass-dark dark:glass-dark glass-light rounded-2xl p-6">
        <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-4">All Transactions</h3>
        
        <div v-if="transactions.length > 0" class="space-y-3">
          <div
            v-for="txn in transactions"
            :key="txn.id"
            class="flex items-center justify-between p-4 bg-white/5 dark:bg-white/5 bg-gray-100/50 rounded-lg hover:bg-white/10 transition-all"
          >
            <div class="flex items-center space-x-3">
              <div :class="[txn.type === 'income' ? 'bg-green-500/20' : 'bg-red-500/20', 'p-2 rounded-lg']">
                <svg v-if="txn.type === 'income'" class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                <svg v-else class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                </svg>
              </div>
              <div>
                <p class="text-white dark:text-white text-gray-900 font-medium">{{ txn.merchant_name || txn.description || 'Transaction' }}</p>
                <p class="text-sm text-gray-400">{{ new Date(txn.date).toLocaleDateString() }}</p>
              </div>
            </div>
            <div class="text-right">
              <p :class="[txn.type === 'income' ? 'text-green-400' : 'text-red-400', 'font-mono text-lg font-semibold']">
                {{ txn.type === 'income' ? '+' : '-' }}{{ txn.currency }}{{ txn.amount.toFixed(2) }}
              </p>
              <p v-if="txn.category_name" class="text-sm text-gray-400">{{ txn.category_name }}</p>
            </div>
          </div>
        </div>
        
        <p v-else class="text-gray-400 text-center py-12">No transactions yet</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import NavigationBar from '../components/NavigationBar.vue'

const transactions = ref([])
const categories = ref([])
const showAddForm = ref(false)
const submitting = ref(false)

const form = ref({
  type: 'expense',
  amount: 0,
  description: '',
  date: new Date().toISOString().split('T')[0],
  category_id: '',
  currency: '€',
  notes: ''
})

async function fetchTransactions() {
  try {
    const response = await api.get('/transactions/', { params: { limit: 100 } })
    transactions.value = response.data
  } catch (error) {
    console.error('Failed to fetch transactions:', error)
  }
}

async function fetchCategories() {
  try {
    const response = await api.get('/settings/categories')
    categories.value = response.data
  } catch (error) {
    console.error('Failed to fetch categories:', error)
  }
}

async function handleSubmit() {
  submitting.value = true
  try {
    const payload = {
      type: form.value.type,
      amount: form.value.amount,
      description: form.value.description,
      date: new Date(form.value.date).toISOString(),
      currency: form.value.currency || '€'
    }
    
    if (form.value.category_id) {
      payload.category_id = form.value.category_id
    }
    
    if (form.value.notes) {
      payload.notes = form.value.notes
    }
    
    await api.post('/transactions/', payload)
    
    // Reset form
    form.value = {
      type: 'expense',
      amount: 0,
      description: '',
      date: new Date().toISOString().split('T')[0],
      category_id: '',
      currency: '€',
      notes: ''
    }
    
    showAddForm.value = false
    await fetchTransactions()
  } catch (error) {
    console.error('Failed to create transaction:', error)
    alert('Failed to create transaction. Please try again.')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchTransactions()
  fetchCategories()
})
</script>
