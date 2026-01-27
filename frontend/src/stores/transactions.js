import { defineStore } from 'pinia'
import api from '../services/api'

/**
 * Store for managing transaction data, dashboard stats, and analytics caching.
 */
export const useTransactionStore = defineStore('transactions', {
    state: () => ({
        recentTransactions: [],
        stats: {
            total_income: 0,
            total_expenses: 0,
            net: 0
        },
        analytics: {}, // Cache by period key (e.g., 'monthly-2026-1')
        lastFetchedDashboard: null,
        loading: false,
        error: null
    }),

    getters: {
        hasData: (state) => state.recentTransactions.length > 0
    },

    actions: {
        /**
         * Fetches dashboard data (transactions and stats).
         * @param {boolean} force - Whether to force a refresh even if data exists.
         */
        async fetchDashboardData(force = false) {
            // SWR Logic: If we have data and it's fresh (within 30s), don't refetch unless forced
            const now = Date.now()
            if (!force && this.hasData && this.lastFetchedDashboard && (now - this.lastFetchedDashboard < 30000)) {
                return
            }

            this.loading = true
            try {
                const response = await api.get('/transactions/', {
                    params: { limit: 50 }
                })

                this.recentTransactions = response.data

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

                this.stats = {
                    total_income: income,
                    total_expenses: expenses,
                    net: income - expenses
                }

                this.lastFetchedDashboard = now
                this.error = null
            } catch (err) {
                this.error = 'Failed to fetch dashboard data'
                console.error(err)
            } finally {
                this.loading = false
            }
        },

        /**
         * Fetches analytics data for a specific period.
         * @param {string} period - 'monthly' or 'yearly'
         * @param {Object} params - Query params (year, month)
         */
        async fetchAnalytics(period, params) {
            const cacheKey = `${period}-${params.year || ''}-${params.month || ''}`

            this.loading = true
            try {
                const response = await api.get(`/transactions/analytics/${period}`, { params })
                this.analytics[cacheKey] = response.data
                this.error = null
                return response.data
            } catch (err) {
                this.error = 'Failed to fetch analytics'
                console.error(err)
                throw err
            } finally {
                this.loading = false
            }
        },

        /**
         * Deletes a transaction and updates the local state.
         * @param {string} id - Transaction ID
         */
        async deleteTransaction(id) {
            try {
                await api.delete(`/transactions/${id}`)
                this.recentTransactions = this.recentTransactions.filter(t => t.id !== id)
                // Recalculate stats or just force refresh
                this.fetchDashboardData(true)
            } catch (err) {
                this.error = 'Failed to delete transaction'
                throw err
            }
        }
    }
})
