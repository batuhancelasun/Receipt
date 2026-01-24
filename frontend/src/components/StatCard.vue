<template>
  <div :class="[color === 'green' ? 'glass-success' : color === 'red' ? 'glass-danger' : 'glass-primary', 'rounded-2xl p-6 animate-fade-in shadow-xl']">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm text-gray-400 mb-1">{{ title }}</p>
        <p class="text-3xl font-bold" :class="textColorClass">{{ value }}</p>
      </div>
      <div :class="[bgColorClass, 'p-4 rounded-xl']">
        <svg v-if="icon === 'arrow-trending-up'" class="w-8 h-8" :class="iconColorClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
        <svg v-else-if="icon === 'arrow-trending-down'" class="w-8 h-8" :class="iconColorClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
        </svg>
        <svg v-else-if="icon === 'wallet'" class="w-8 h-8" :class="iconColorClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a2.25 2.25 0 00-2.25-2.25H15a3 3 0 11-6 0H5.25A2.25 2.25 0 003 12m18 0v6a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 18v-6m18 0V9M3 12V9m18 0a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 9m18 0V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v3" />
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: String,
  value: String,
  icon: String,
  color: { type: String, default: 'blue' }
})

const textColorClass = computed(() => {
  if (props.color === 'green') return 'text-green-400'
  if (props.color === 'red') return 'text-red-400'
  return 'text-blue-400'
})

const bgColorClass = computed(() => {
  if (props.color === 'green') return 'bg-green-500/10'
  if (props.color === 'red') return 'bg-red-500/10'
  return 'bg-blue-500/10'
})

const iconColorClass = computed(() => {
  if (props.color === 'green') return 'text-green-400'
  if (props.color === 'red') return 'text-red-400'
  return 'text-blue-400'
})
</script>

<style scoped>
.glass-success {
  @apply bg-green-500/10 backdrop-blur-xl border border-green-500/30;
}

.glass-danger {
  @apply bg-red-500/10 backdrop-blur-xl border border-red-500/30;
}

.glass-primary {
  @apply bg-blue-500/10 backdrop-blur-xl border border-blue-500/30;
}
</style>
