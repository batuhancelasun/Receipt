<template>
  <div class="min-h-screen">
    <NavigationBar />
    
    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-3xl font-bold text-white dark:text-white text-gray-900 mb-8">Dashboard</h1>
      
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <stat-card
          title="Total Income"
          :value="formatCurrency(stats.total_income)"
          icon="arrow-trending-up"
          color="green"
        />
        <stat-card
          title="Total Expenses"
          :value="formatCurrency(stats.total_expenses)"
          icon="arrow-trending-down"
          color="red"
        />
        <stat-card
          title="Net Balance"
          :value="formatCurrency(stats.net)"
          icon="wallet"
          :color="stats.net >= 0 ? 'blue' : 'red'"
        />
      </div>

      <!-- Recent Activity -->
      <div class="glass-dark dark:glass-dark glass-light rounded-2xl p-6 mb-8">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-white dark:text-white text-gray-900">Recent Transactions</h2>
          <router-link to="/transactions" class="text-primary-400 hover:text-primary-300 text-sm font-medium">
            View All
          </router-link>
        </div>
        
        <div v-if="recentTransactions.length > 0" class="space-y-3">
          <div
            v-for="txn in recentTransactions.slice(0, 5)"
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
                <p class="text-sm text-gray-400">{{ new Date(txn.date).toLocaleDateString('en-GB') }}</p>
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
        
        <p v-else class="text-gray-400 text-center py-8">No recent transactions</p>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <router-link
          to="/scan"
          class="glass-dark dark:glass-dark glass-light rounded-2xl p-8 text-center hover:scale-105 transition-transform cursor-pointer group"
        >
          <div class="w-16 h-16 mx-auto mb-4 bg-primary-600 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform shadow-lg shadow-primary-500/50">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-2">Scan Receipt</h3>
          <p class="text-gray-400">AI-powered receipt scanning</p>
        </router-link>

        <router-link
          to="/transactions"
          class="glass-dark dark:glass-dark glass-light rounded-2xl p-8 text-center hover:scale-105 transition-transform cursor-pointer group"
        >
          <div class="w-16 h-16 mx-auto mb-4 bg-green-600 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform shadow-lg shadow-green-500/50">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-2">Add Transaction</h3>
          <p class="text-gray-400">Manual entry</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import NavigationBar from '../components/NavigationBar.vue'
import StatCard from '../components/StatCard.vue'

const stats = ref({
  total_income: 0,
  total_expenses: 0,
  net: 0
})

const recentTransactions = ref([])

const formatCurrency = (amount) => {
  return `€${amount.toFixed(2)}`
}

async function fetchDashboardData() {
  try {
    const response = await api.get('/transactions/', {
      params: {
        limit: 50
      }
    })
    
    recentTransactions.value = response.data
    
    // Calculate stats
    let income = 0
    let expenses = 0
    response.data.forEach(txn => {
      if (txn.type === 'income') {
        income += txn.amount
      } else {
        expenses += txn.amount
      }
    })
    
    stats.value = {
      total_income: income,
      total_expenses: expenses,
      net: income - expenses
    }
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
  }
}

onMounted(() => {
  fetchDashboardData()
})
</script>
