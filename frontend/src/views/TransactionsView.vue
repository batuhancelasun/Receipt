<template>
  <div class="min-h-screen p-8">
    <div class="max-w-6xl mx-auto">
      <h1 class="text-3xl font-bold text-white dark:text-white text-gray-900 mb-8">Transactions</h1>
      
      <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
        <h3 class="text-xl font-semibold text-white mb-4">Recent Transactions</h3>
        
        <div v-if="transactions.length > 0" class="space-y-3">
          <div
            v-for="txn in transactions"
            :key="txn.id"
            class="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition-colors"
          >
            <div>
              <p class="text-white font-medium">{{ txn.merchant_name || txn.description || 'Transaction' }}</p>
              <p class="text-sm text-gray-400">{{ new Date(txn.date).toLocaleDateString() }}</p>
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

const transactions = ref([])

async function fetchTransactions() {
  try {
    const response = await api.get('/transactions/', { params: { limit: 50 } })
    transactions.value = response.data
  } catch (error) {
    console.error('Failed to fetch transactions:', error)
  }
}

onMounted(() => {
  fetchTransactions()
})
</script>
