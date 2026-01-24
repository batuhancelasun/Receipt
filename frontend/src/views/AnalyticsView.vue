<template>
  <div class="min-h-screen">
    <NavigationBar />
    
    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-3xl font-bold text-white dark:text-white text-gray-900 mb-8">Analytics</h1>
      
      <!-- Period Selector -->
      <div class="glass-dark dark:glass-dark glass-light rounded-2xl p-6 mb-8">
        <div class="flex flex-wrap gap-3">
          <button
            v-for="p in periods"
            :key="p.value"
            @click="selectedPeriod = p.value"
            :class="[
              'px-6 py-3 rounded-xl font-medium transition-all',
              selectedPeriod === p.value
                ? 'bg-primary-500 text-white shadow-lg shadow-primary-500/50'
                : 'bg-white/5 dark:bg-white/5 bg-gray-100/50 text-gray-300 dark:text-gray-300 text-gray-700 hover:bg-white/10'
            ]"
          >
            {{ p.label }}
          </button>
        </div>
      </div>

      <!-- Stats Summary -->
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

      <!-- Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- Income Breakdown -->
        <div class="glass-dark dark:glass-dark glass-light rounded-2xl p-6">
          <h2 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-4">Income by Category</h2>
          <div v-if="hasIncomeData" class="relative h-64">
            <canvas ref="incomeChartRef"></canvas>
          </div>
          <p v-else class="text-gray-400 text-center py-16">No income data for this period</p>
        </div>

        <!-- Expense Breakdown -->
        <div class="glass-dark dark:glass-dark glass-light rounded-2xl p-6">
          <h2 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-4">Expenses by Category</h2>
          <div v-if="hasExpenseData" class="relative h-64">
            <canvas ref="expenseChartRef"></canvas>
          </div>
          <p v-else class="text-gray-400 text-center py-16">No expense data for this period</p>
        </div>
      </div>

      <!-- Category Details -->
      <div class="glass-dark dark:glass-dark glass-light rounded-2xl p-6">
        <h2 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-4">Category Breakdown</h2>
        
        <div class="space-y-4">
          <div v-for="category in categoryList" :key="category.name" class="bg-white/5 dark:bg-white/5 bg-gray-100/50 rounded-lg p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="font-medium text-white dark:text-white text-gray-900">{{ category.name }}</span>
              <span :class="[category.type === 'income' ? 'text-green-400' : 'text-red-400', 'font-mono font-semibold']">
                {{ formatCurrency(category.total) }}
              </span>
            </div>
            <div class="w-full bg-white/10 dark:bg-white/10 bg-gray-200/50 rounded-full h-2">
              <div
                :class="[category.type === 'income' ? 'bg-green-500' : 'bg-red-500', 'h-2 rounded-full transition-all']"
                :style="{ width: category.percentage + '%' }"
              ></div>
            </div>
            <div class="flex items-center justify-between mt-1 text-sm text-gray-400">
              <span v-if="category.count > 0">{{ category.count }} transactions</span>
              <span v-else></span>
              <span>{{ category.percentage.toFixed(1) }}%</span>
            </div>
          </div>
        </div>

        <p v-if="categoryList.length === 0" class="text-gray-400 text-center py-8">No data for this period</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import api from '../services/api'
import NavigationBar from '../components/NavigationBar.vue'
import StatCard from '../components/StatCard.vue'

Chart.register(...registerables)

const periods = [
  { label: 'Daily', value: 'daily' },
  { label: 'Monthly', value: 'monthly' },
  { label: 'Yearly', value: 'yearly' }
]

const selectedPeriod = ref('monthly')
const analyticsData = ref({
  stats: {
    total_income: 0,
    total_expenses: 0,
    net: 0,
    transaction_count: 0
  },
  expense_breakdown: [],
  income_breakdown: []
})

const incomeChartRef = ref(null)
const expenseChartRef = ref(null)
let incomeChart = null
let expenseChart = null

const hasIncomeData = computed(() => {
  return analyticsData.value.income_breakdown && analyticsData.value.income_breakdown.length > 0
})

const hasExpenseData = computed(() => {
  return analyticsData.value.expense_breakdown && analyticsData.value.expense_breakdown.length > 0
})

const stats = computed(() => analyticsData.value.stats)

const categoryList = computed(() => {
  const list = [
    ...analyticsData.value.income_breakdown.map(item => ({ 
      name: item.category_name,
      total: item.amount,
      percentage: item.percentage,
      count: 0, // Backend doesn't provide count per category yet
      type: 'income',
      color: item.color
    })),
    ...analyticsData.value.expense_breakdown.map(item => ({ 
      name: item.category_name,
      total: item.amount,
      percentage: item.percentage,
      count: 0, // Backend doesn't provide count per category yet
      type: 'expense',
      color: item.color
    }))
  ]
  
  return list.sort((a, b) => b.total - a.total)
})

const formatCurrency = (amount) => {
  const value = amount ?? 0
  return `€${value.toFixed(2)}`
}

const chartColors = [
  '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
  '#EC4899', '#14B8A6', '#F97316', '#6366F1', '#84CC16'
]

function createPieChart(canvas, data, title) {
  if (!canvas) return null
  
  const ctx = canvas.getContext('2d')
  const labels = data.map(d => d.category_name)
  const values = data.map(d => d.amount)
  const bgColors = data.map((d, i) => d.color || chartColors[i % chartColors.length])
  
  return new Chart(ctx, {
    type: 'pie',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: bgColors,
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#9CA3AF',
            padding: 15,
            font: {
              size: 12
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.label || ''
              const value = context.parsed || 0
              return `${label}: €${value.toFixed(2)}`
            }
          }
        }
      }
    }
  })
}

function destroyCharts() {
  if (incomeChart) {
    incomeChart.destroy()
    incomeChart = null
  }
  if (expenseChart) {
    expenseChart.destroy()
    expenseChart = null
  }
}

function renderCharts() {
  destroyCharts()
  
  nextTick(() => {
    if (hasIncomeData.value && incomeChartRef.value) {
      incomeChart = createPieChart(incomeChartRef.value, analyticsData.value.income_breakdown, 'Income')
    }
    if (hasExpenseData.value && expenseChartRef.value) {
      expenseChart = createPieChart(expenseChartRef.value, analyticsData.value.expense_breakdown, 'Expenses')
    }
  })
}

async function fetchAnalytics() {
  try {
    const response = await api.get(`/transactions/analytics/${selectedPeriod.value}`)
    analyticsData.value = response.data
    renderCharts()
  } catch (error) {
    console.error('Failed to fetch analytics:', error)
  }
}

watch(selectedPeriod, () => {
  fetchAnalytics()
})

onMounted(() => {
  fetchAnalytics()
})
</script>
