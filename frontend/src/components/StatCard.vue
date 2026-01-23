<template>
  <div :class="[color === 'green' ? 'glass-success' : color === 'red' ? 'glass-danger' : 'glass-primary', 'rounded-xl p-6 animate-fade-in']">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm text-gray-400 mb-1">{{ title }}</p>
        <p class="text-3xl font-bold text-white dark:text-white" :class="textColorClass">{{ value }}</p>
      </div>
      <span class="text-4xl">{{ icon }}</span>
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
</script>

<style scoped>
.glass-success {
  @apply bg-green-500/10 backdrop-blur-md border border-green-500/30;
}

.glass-danger {
  @apply bg-red-500/10 backdrop-blur-md border border-red-500/30;
}

.glass-primary {
  @apply bg-blue-500/10 backdrop-blur-md border border-blue-500/30;
}
</style>
