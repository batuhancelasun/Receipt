import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
    const theme = ref(localStorage.getItem('theme') || 'dark')

    function toggleTheme() {
        theme.value = theme.value === 'dark' ? 'light' : 'dark'
        localStorage.setItem('theme', theme.value)
        updateDocumentClass()
    }

    function setTheme(newTheme) {
        theme.value = newTheme
        localStorage.setItem('theme', newTheme)
        updateDocumentClass()
    }

    function updateDocumentClass() {
        if (theme.value === 'dark') {
            document.documentElement.classList.add('dark')
            document.documentElement.classList.remove('light')
        } else {
            document.documentElement.classList.add('light')
            document.documentElement.classList.remove('dark')
        }
    }

    // Initialize on load
    updateDocumentClass()

    return {
        theme,
        toggleTheme,
        setTheme
    }
})
