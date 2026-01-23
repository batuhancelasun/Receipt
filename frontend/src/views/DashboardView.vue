<template>
  <div class="min-h-screen">
    <!-- Navigation -->
    <nav class="glass-dark dark:glass-dark glass-light border-b border-white/10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center space-x-8">
            <h1 class="text-2xl font-bold text-white dark:text-white text-gray-900">Receipt</h1>
            <div class="hidden md:flex space-x-4">
              <router-link to="/" class="nav-link">Dashboard</router-link>
              <router-link to="/ scan" class="nav-link">Scan</router-link>
              <router-link to="/transactions" class="nav-link">Transactions</router-link>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="themeStore.toggleTheme()"
              class="p-2 rounded-lg hover:bg-white/10 transition-colors"
              title="Toggle theme"
            >
              <span v-if="themeStore.theme === 'dark'" class="text-2xl">☀️</span>
              <span v-else class="text-2xl">🌙</span>
            </button>
            <router-link to="/settings" class="p-2 rounded-lg hover:bg-white/10 transition-colors">
              <span class="text-2xl">⚙️</span>
            </router-link>
            <button
              @click="handleLogout"
              class="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-200 rounded-lg transition-colors text-sm font-medium"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <stat-card
          title="Total Income"
          :value="formatCurrency(analytics?.stats.total_income || 0)"
          icon="💰"
          color="green"
        />
        <stat-card
          title="Total Expenses"
          :value="formatCurrency(analytics?.stats.total_expenses || 0)"
          icon="💸"
          color="red"
        />
        <stat-card
          title="Net Balance"
          :value="formatCurrency(analytics?.stats.net || 0)"
          icon="📊"
          :color="(analytics?.stats.net || 0) >= 0 ? 'blue' : 'red'"
        />
      </div>

      <!-- Period Selector -->
      <div class="glass-dark dark:glass-dark glass-light rounded-xl p-4 mb-8">
        <div class="flex space-x-2">
          <button
            v-for="p in ['daily', 'monthly', 'yearly']"
            :key="p"
            @click="period = p; fetchAnalytics()"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-all capitalize',
              period === p
                ? 'bg-primary-600 text-white'
                : 'text-gray-300 hover:bg-white/10'
            ]"
          >
            {{ p }}
          </button>
        </div>
      </div>

      <!-- Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-4">
            Expense Breakdown
          </h3>
          <div v-if="analytics?.expense_breakdown.length > 0" class="h-64">
            <Pie :data="expenseChartData" :options="chartOptions" />
          </div>
          <p v-else class="text-gray-400 text-center py-12">No expenses yet</p>
        </div>

        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-4">
            Income Breakdown
          </h3>
          <div v-if="analytics?.income_breakdown.length > 0" class="h-64">
            <Pie :data="incomeChartData" :options="chartOptions" />
          </div>
          <p v-else class="text-gray-400 text-center py-12">No income yet</p>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <router-link
          to="/scan"
          class="glass-dark dark:glass-dark glass-light rounded-xl p-8 text-center hover:scale-105 transition-transform cursor-pointer group"
        >
          <span class="text-6xl mb-4 block group-hover:scale-110 transition-transform">📸</span>
          <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900">Scan Receipt</h3>
          <p class="text-gray-400 mt-2">AI-powered receipt scanning</p>
        </router-link>

        <router-link
          to="/transactions"
          class="glass-dark dark:glass-dark glass-light rounded-xl p-8 text-center hover:scale-105 transition-transform cursor-pointer group"
        >
          <span class="text-6xl mb-4 block group-hover:scale-110 transition-transform">📝</span>
          <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900">Add Transaction</h3>
          <p class="text-gray-400 mt-2">Manual entry</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js'
import api from '../services/api'
import { useAuthStore } from '../stores/auth'
import { useThemeStore } from '../stores/theme'
import StatCard from '../components/StatCard.vue'

ChartJS.register(ArcElement, Tooltip, Legend)

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const analytics = ref(null)
const period = ref('monthly')

const formatCurrency = (amount) => {
  return `€${amount.toFixed(2)}`
}

const expenseChartData = computed(() => ({
  labels: analytics.value?.expense_breakdown.map(c => c.category_name) || [],
  datasets: [{
    data: analytics.value?.expense_breakdown.map(c => c.amount) || [],
    backgroundColor: analytics.value?.expense_breakdown.map(c => c.color) || [],
    borderWidth: 0
  }]
}))

const incomeChartData = computed(() => ({
  labels: analytics.value?.income_breakdown.map(c => c.category_name) || [],
  datasets: [{
    data: analytics.value?.income_breakdown.map(c => c.amount) || [],
    backgroundColor: analytics.value?.income_breakdown.map(c => c.color) || [],
    borderWidth: 0
  }]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: '#9CA3AF',
        padding: 15,
        font: { size: 12 }
      }
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          return `${context.label}: €${context.parsed.toFixed(2)}`
        }
      }
    }
  }
}

async function fetchAnalytics() {
  try {
    const response = await api.get(`/transactions/analytics/${period.value}`)
    analytics.value = response.data
  } catch (error) {
    console.error('Failed to fetch analytics:', error)
  }
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  fetchAnalytics()
})
</script>

<style scoped>
.nav-link {
  @apply px-3 py-2 rounded-lg text-gray-300 dark:text-gray-300 text-gray-700 hover:bg-white/10 transition-colors font-medium;
}

.nav-link.router-link-active {
  @apply bg-primary-600 text-white;
}
</style>
