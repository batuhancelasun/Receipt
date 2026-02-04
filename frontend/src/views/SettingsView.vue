<template>
  <div class="min-h-screen">
    <NavigationBar />
    
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-3xl font-bold text-white dark:text-white text-gray-900 mb-8">Settings</h1>
      
      <!-- Settings Navigation Tabs -->
      <div class="flex space-x-2 mb-8 overflow-x-auto">
        <button
          @click="activeTab = 'general'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-all flex items-center space-x-2',
            activeTab === 'general'
              ? 'bg-primary-600 text-white'
              : 'bg-white/10 text-gray-300 hover:bg-white/20'
          ]"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span>General</span>
        </button>
        <button
          @click="activeTab = 'categories'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-all flex items-center space-x-2',
            activeTab === 'categories'
              ? 'bg-primary-600 text-white'
              : 'bg-white/10 text-gray-300 hover:bg-white/20'
          ]"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
          </svg>
          <span>Categories</span>
        </button>
        <button
          v-if="authStore.user?.is_admin"
          @click="activeTab = 'users'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-all flex items-center space-x-2',
            activeTab === 'users'
              ? 'bg-primary-600 text-white'
              : 'bg-white/10 text-gray-300 hover:bg-white/20'
          ]"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <span>Users</span>
        </button>
      </div>
      
      <!-- General Settings Tab -->
      <div v-if="activeTab === 'general'" class="space-y-6 animate-fade-in">
        <!-- Gemini API Key -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <div class="flex items-center space-x-3 mb-4">
            <div class="p-2 bg-purple-500/20 rounded-lg">
              <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900">Gemini API Key</h3>
          </div>
          <input
            v-model="apiKey"
            type="password"
            placeholder="Enter your Gemini 2.5 Flash Lite API key"
            class="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
          />
          <p class="text-sm text-gray-400 mt-2">Required for AI receipt scanning</p>
        </div>
        
        <!-- Currency -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <div class="flex items-center space-x-3 mb-4">
            <div class="p-2 bg-green-500/20 rounded-lg">
              <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900">Default Currency</h3>
          </div>
          <select
            v-model="currency"
            class="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
          >
            <option value="€">€ Euro</option>
            <option value="$">$ US Dollar</option>
            <option value="£">£ Pound</option>
            <option value="₺">₺ Turkish Lira</option>
            <option value="¥">¥ Yen/Yuan</option>
          </select>
        </div>
        
        <!-- Theme -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <div class="flex items-center space-x-3 mb-4">
            <div class="p-2 bg-blue-500/20 rounded-lg">
              <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900">Theme</h3>
          </div>
          <div class="flex space-x-4">
            <button
              @click="theme = 'dark'"
              :class="[
                'flex-1 py-3 rounded-lg font-medium transition-all flex items-center justify-center space-x-2',
                theme === 'dark' ? 'bg-primary-600 text-white shadow-lg' : 'bg-white/5 text-gray-300 hover:bg-white/10'
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
              <span>Dark</span>
            </button>
            <button
              @click="theme = 'light'"
              :class="[
                'flex-1 py-3 rounded-lg font-medium transition-all flex items-center justify-center space-x-2',
                theme === 'light' ? 'bg-primary-600 text-white shadow-lg' : 'bg-white/5 text-gray-300 hover:bg-white/10'
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              <span>Light</span>
            </button>
          </div>
        </div>

        <!-- Backup & Restore -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <div class="flex items-center space-x-3 mb-4">
            <div class="p-2 bg-indigo-500/20 rounded-lg">
              <svg class="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8 8 0 104.582 9m0 0H9" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900">Backup & Restore</h3>
          </div>
          <p class="text-sm text-gray-400 mb-4">Export your settings, categories, and transactions to a JSON file, or import them after reinstall.</p>
          <div class="flex flex-col sm:flex-row gap-3">
            <button
              type="button"
              @click="exportData"
              class="px-4 py-2 rounded-lg bg-primary-600 text-white hover:bg-primary-700 transition"
            >
              Export Data
            </button>
            <input ref="importInput" type="file" accept="application/json" class="hidden" @change="handleImportFile" />
            <button
              type="button"
              @click="triggerImport"
              class="px-4 py-2 rounded-lg bg-white/10 text-gray-200 hover:bg-white/20 transition"
            >
              Import Data
            </button>
          </div>
          <p v-if="backupMessage" :class="['text-sm mt-3', backupType === 'error' ? 'text-red-400' : 'text-green-400']">{{ backupMessage }}</p>
        </div>
        
        <!-- Save Button -->
        <button
          @click="saveSettings"
          :disabled="saving"
          class="w-full py-3 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-lg transition-all disabled:opacity-50 shadow-lg"
        >
          {{ saving ? 'Saving...' : 'Save Settings' }}
        </button>
        
        <div v-if="message" :class="[
          'p-4 rounded-lg animate-fade-in',
          messageType === 'success' ? 'bg-green-500/20 border border-green-500/50' : 'bg-red-500/20 border border-red-500/50'
        ]">
          <p :class="messageType === 'success' ? 'text-green-200' : 'text-red-200'">{{ message }}</p>
        </div>
      </div>
      
      <!-- Categories Tab -->
      <div v-if="activeTab === 'categories'" class="space-y-6 animate-fade-in">
        <!-- Create Category Form -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6 overflow-visible">
          <div class="flex items-center space-x-3 mb-6">
            <div class="p-2 bg-orange-500/20 rounded-lg">
              <svg class="w-6 h-6 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900">
              {{ editingCategory ? 'Edit Category' : 'Create Category' }}
            </h3>
          </div>
          
          <form @submit.prevent="editingCategory ? updateCategory() : createCategory()" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Name</label>
                <input
                  v-model="categoryForm.name"
                  type="text"
                  required
                  maxlength="50"
                  class="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
                  placeholder="e.g., Groceries"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Type</label>
                <select
                  v-model="categoryForm.type"
                  :disabled="editingCategory"
                  class="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all disabled:opacity-50"
                >
                  <option value="expense">Expense</option>
                  <option value="income">Income</option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Icon</label>
                <IconPicker v-model="categoryForm.icon" />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Color</label>
                <div class="flex items-center space-x-3">
                  <input
                    v-model="categoryForm.color"
                    type="color"
                    class="w-14 h-12 rounded-lg cursor-pointer bg-white/5 border border-white/10"
                  />
                  <input
                    v-model="categoryForm.color"
                    type="text"
                    pattern="^#[0-9A-Fa-f]{6}$"
                    class="flex-1 px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white font-mono focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
                    placeholder="#6366f1"
                  />
                </div>
              </div>
            </div>
            
            <div class="flex space-x-3">
              <button
                v-if="editingCategory"
                type="button"
                @click="cancelEdit"
                class="px-6 py-3 bg-white/10 hover:bg-white/20 text-gray-300 font-medium rounded-lg transition-all"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="categoryLoading"
                class="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-lg transition-all disabled:opacity-50 shadow-lg"
              >
                {{ categoryLoading ? 'Saving...' : (editingCategory ? 'Update Category' : 'Create Category') }}
              </button>
            </div>
            
            <div v-if="categoryError" class="bg-red-500/20 border border-red-500/50 rounded-lg p-3 animate-fade-in">
              <p class="text-red-200 text-sm">{{ categoryError }}</p>
            </div>
          </form>
        </div>
        
        <!-- Categories List -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-4">Your Categories</h3>
          
          <!-- Expense Categories -->
          <div v-if="expenseCategories.length > 0" class="mb-6">
            <h4 class="text-sm font-medium text-gray-400 uppercase tracking-wide mb-3">Expense Categories</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div
                v-for="cat in expenseCategories"
                :key="cat.id"
                class="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition-all"
              >
                <div class="flex items-center space-x-3">
                  <div
                    class="w-10 h-10 rounded-lg flex items-center justify-center"
                    :style="{ backgroundColor: cat.color + '30' }"
                  >
                    <div class="w-5 h-5" :style="{ color: cat.color }" v-html="getIconSvg(cat.icon)"></div>
                  </div>
                  <span class="text-white font-medium">{{ cat.name }}</span>
                </div>
                <div class="flex items-center space-x-2">
                  <button
                    @click="startEdit(cat)"
                    class="p-2 hover:bg-white/10 rounded-lg transition-colors"
                    title="Edit"
                  >
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </button>
                  <button
                    @click="deleteCategory(cat.id)"
                    class="p-2 hover:bg-red-500/20 rounded-lg transition-colors"
                    title="Delete"
                  >
                    <svg class="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Income Categories -->
          <div v-if="incomeCategories.length > 0">
            <h4 class="text-sm font-medium text-gray-400 uppercase tracking-wide mb-3">Income Categories</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div
                v-for="cat in incomeCategories"
                :key="cat.id"
                class="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition-all"
              >
                <div class="flex items-center space-x-3">
                  <div
                    class="w-10 h-10 rounded-lg flex items-center justify-center"
                    :style="{ backgroundColor: cat.color + '30' }"
                  >
                    <div class="w-5 h-5" :style="{ color: cat.color }" v-html="getIconSvg(cat.icon)"></div>
                  </div>
                  <span class="text-white font-medium">{{ cat.name }}</span>
                </div>
                <div class="flex items-center space-x-2">
                  <button
                    @click="startEdit(cat)"
                    class="p-2 hover:bg-white/10 rounded-lg transition-colors"
                    title="Edit"
                  >
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </button>
                  <button
                    @click="deleteCategory(cat.id)"
                    class="p-2 hover:bg-red-500/20 rounded-lg transition-colors"
                    title="Delete"
                  >
                    <svg class="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <p v-if="categories.length === 0" class="text-gray-400 text-center py-8">
            No categories yet. Create your first category above!
          </p>
        </div>
      </div>
      
      <!-- Users Tab (Admin Only) -->
      <div v-if="activeTab === 'users' && authStore.user?.is_admin" class="space-y-6 animate-fade-in">
        <!-- Create User Form -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <div class="flex items-center space-x-3 mb-6">
            <div class="p-2 bg-indigo-500/20 rounded-lg">
              <svg class="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900">Create New User</h3>
          </div>
          
          <form @submit.prevent="createUser" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Username</label>
                <input
                  v-model="newUser.username"
                  type="text"
                  required
                  minlength="3"
                  class="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
                  placeholder="Enter username"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Email</label>
                <input
                  v-model="newUser.email"
                  type="email"
                  required
                  class="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
                  placeholder="user@example.com"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Password</label>
                <input
                  v-model="newUser.password"
                  type="password"
                  required
                  minlength="8"
                  class="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
                  placeholder="Minimum 8 characters"
                />
              </div>
              
              <div class="flex items-center">
                <label class="flex items-center cursor-pointer">
                  <input
                    v-model="newUser.is_admin"
                    type="checkbox"
                    class="w-5 h-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span class="ml-2 text-white">Grant admin privileges</span>
                </label>
              </div>
            </div>
            
            <div v-if="userError" class="bg-red-500/20 border border-red-500/50 rounded-lg p-3 animate-fade-in">
              <p class="text-red-200 text-sm">{{ userError }}</p>
            </div>
            
            <div v-if="userSuccess" class="bg-green-500/20 border border-green-500/50 rounded-lg p-3 animate-fade-in">
              <p class="text-green-200 text-sm">{{ userSuccess }}</p>
            </div>
            
            <button
              type="submit"
              :disabled="userLoading"
              class="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-lg transition-all disabled:opacity-50"
            >
              {{ userLoading ? 'Creating...' : 'Create User' }}
            </button>
          </form>
        </div>
        
        <!-- Users List -->
        <div class="glass-dark dark:glass-dark glass-light rounded-xl p-6">
          <h3 class="text-xl font-semibold text-white dark:text-white text-gray-900 mb-4">All Users</h3>
          
          <div v-if="users.length > 0" class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-white/10">
                  <th class="text-left py-3 px-4 text-gray-300 font-medium">Username</th>
                  <th class="text-left py-3 px-4 text-gray-300 font-medium">Email</th>
                  <th class="text-left py-3 px-4 text-gray-300 font-medium">Role</th>
                  <th class="text-right py-3 px-4 text-gray-300 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="user in users"
                  :key="user.id"
                  class="border-b border-white/5 hover:bg-white/5 transition-colors"
                >
                  <td class="py-3 px-4 text-white">{{ user.username }}</td>
                  <td class="py-3 px-4 text-gray-300">{{ user.email }}</td>
                  <td class="py-3 px-4">
                    <span :class="[user.is_admin ? 'bg-purple-500/20 text-purple-300' : 'bg-gray-500/20 text-gray-300', 'px-2 py-1 rounded text-xs']">
                      {{ user.is_admin ? 'Admin' : 'User' }}
                    </span>
                  </td>
                  <td class="py-3 px-4 text-right">
                    <button
                      v-if="user.id !== currentUserId"
                      @click="deleteUser(user.id)"
                      class="px-3 py-1 bg-red-500/20 hover:bg-red-500/30 text-red-200 rounded text-sm transition-colors"
                    >
                      Delete
                    </button>
                    <span v-else class="text-gray-500 text-sm">Current User</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <p v-else class="text-gray-400 text-center py-8">No users found</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'
import { useThemeStore } from '../stores/theme'
import { useAuthStore } from '../stores/auth'
import NavigationBar from '../components/NavigationBar.vue'
import IconPicker from '../components/IconPicker.vue'

const themeStore = useThemeStore()
const authStore = useAuthStore()

// Tab state
const activeTab = ref('general')

// General settings state
const apiKey = ref('')
const currency = ref('€')
const theme = ref('dark')
const saving = ref(false)
const message = ref('')
const messageType = ref('success')

// Category management state
const categories = ref([])
const categoryForm = ref({
  name: '',
  icon: 'shopping-cart',
  color: '#6366f1',
  type: 'expense'
})
const editingCategory = ref(null)
const categoryLoading = ref(false)
const categoryError = ref('')

// User management state
const newUser = ref({
  username: '',
  email: '',
  password: '',
  is_admin: false
})
const users = ref([])
const userLoading = ref(false)
const userError = ref('')
const userSuccess = ref('')
const backupMessage = ref('')
const backupType = ref('success')
const importInput = ref(null)

const currentUserId = computed(() => authStore.user?.id)

const expenseCategories = computed(() => categories.value.filter(c => c.type === 'expense'))
const incomeCategories = computed(() => categories.value.filter(c => c.type === 'income'))

// Icon SVG mapping
const iconSvgMap = {
  'shopping-cart': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"/></svg>',
  'home': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>',
  'car': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h8m-8 5h8m-4 7v-7m0 0l-4-4 4-4 4 4-4 4z"/></svg>',
  'utensils': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>',
  'heart': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>',
  'briefcase': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>',
  'graduation-cap': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"/></svg>',
  'film': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z"/></svg>',
  'gift': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"/></svg>',
  'plane': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg>',
  'wifi': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"/></svg>',
  'phone': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>',
  'bolt': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>',
  'credit-card': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/></svg>',
  'currency-dollar': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
  'chart-bar': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>',
  'sparkles': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/></svg>',
  'puzzle': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z"/></svg>',
  'scissors': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.121 14.121L19 19m-7-7l7-7m-7 7l-2.879 2.879M12 12L9.121 9.121m0 5.758a3 3 0 10-4.243 4.243 3 3 0 004.243-4.243zm0-5.758a3 3 0 10-4.243-4.243 3 3 0 004.243 4.243z"/></svg>',
  'paw': '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5"/></svg>'
}

function getIconSvg(iconId) {
  return iconSvgMap[iconId] || iconSvgMap['sparkles']
}

// General settings functions
async function loadSettings() {
  try {
    const response = await api.get('/settings/')
    currency.value = response.data.default_currency
    theme.value = response.data.theme
    themeStore.setTheme(response.data.theme)
  } catch (error) {
    console.error('Failed to load settings:', error)
  }
}

async function saveSettings() {
  saving.value = true
  message.value = ''
  
  try {
    const updates = {
      default_currency: currency.value,
      theme: theme.value
    }
    
    if (apiKey.value) {
      updates.gemini_api_key = apiKey.value
    }
    
    await api.put('/settings/', updates)
    themeStore.setTheme(theme.value)
    
    message.value = 'Settings saved successfully!'
    messageType.value = 'success'
    apiKey.value = ''
  } catch (error) {
    message.value = 'Failed to save settings'
    messageType.value = 'error'
  } finally {
    saving.value = false
  }
}

function triggerImport() {
  if (importInput.value) {
    importInput.value.click()
  }
}

async function exportData() {
  backupMessage.value = ''
  try {
    const response = await api.get('/settings/export')
    const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    link.href = url
    link.download = `receipt-backup-${timestamp}.json`
    document.body.appendChild(link)
    link.click()
    link.remove()
    URL.revokeObjectURL(url)
    backupMessage.value = 'Export completed successfully.'
    backupType.value = 'success'
  } catch (error) {
    backupMessage.value = 'Failed to export data.'
    backupType.value = 'error'
  }
}

async function handleImportFile(event) {
  const file = event.target.files?.[0]
  if (!file) return
  backupMessage.value = ''
  try {
    const text = await file.text()
    const payload = JSON.parse(text)
    await api.post('/settings/import', payload, { params: { mode: 'replace' } })
    backupMessage.value = 'Import completed successfully.'
    backupType.value = 'success'
    await loadSettings()
    await fetchCategories()
  } catch (error) {
    backupMessage.value = 'Failed to import data. Please check the file.'
    backupType.value = 'error'
  } finally {
    if (importInput.value) {
      importInput.value.value = ''
    }
  }
}

// Category functions
async function fetchCategories() {
  try {
    const response = await api.get('/settings/categories')
    categories.value = response.data
  } catch (error) {
    console.error('Failed to fetch categories:', error)
  }
}

async function createCategory() {
  categoryError.value = ''
  categoryLoading.value = true
  
  try {
    await api.post('/settings/categories', categoryForm.value)
    
    categoryForm.value = {
      name: '',
      icon: 'shopping-cart',
      color: '#6366f1',
      type: 'expense'
    }
    
    await fetchCategories()
  } catch (error) {
    categoryError.value = error.response?.data?.detail || 'Failed to create category'
  } finally {
    categoryLoading.value = false
  }
}

function startEdit(cat) {
  editingCategory.value = cat
  categoryForm.value = {
    name: cat.name,
    icon: cat.icon,
    color: cat.color,
    type: cat.type
  }
}

function cancelEdit() {
  editingCategory.value = null
  categoryForm.value = {
    name: '',
    icon: 'shopping-cart',
    color: '#6366f1',
    type: 'expense'
  }
}

async function updateCategory() {
  categoryError.value = ''
  categoryLoading.value = true
  
  try {
    await api.put(`/settings/categories/${editingCategory.value.id}`, {
      name: categoryForm.value.name,
      icon: categoryForm.value.icon,
      color: categoryForm.value.color
    })
    
    cancelEdit()
    await fetchCategories()
  } catch (error) {
    categoryError.value = error.response?.data?.detail || 'Failed to update category'
  } finally {
    categoryLoading.value = false
  }
}

async function deleteCategory(id) {
  if (!confirm('Are you sure you want to delete this category?')) return
  
  try {
    await api.delete(`/settings/categories/${id}`)
    await fetchCategories()
  } catch (error) {
    categoryError.value = error.response?.data?.detail || 'Failed to delete category'
  }
}

// User management functions
async function fetchUsers() {
  try {
    const response = await api.get('/auth/admin/users')
    users.value = response.data
  } catch (err) {
    console.error('Failed to fetch users:', err)
  }
}

async function createUser() {
  userError.value = ''
  userSuccess.value = ''
  userLoading.value = true
  
  try {
    await api.post('/auth/admin/create-user', newUser.value)
    userSuccess.value = 'User created successfully!'
    
    newUser.value = {
      username: '',
      email: '',
      password: '',
      is_admin: false
    }
    
    await fetchUsers()
  } catch (err) {
    userError.value = err.response?.data?.detail || 'Failed to create user'
  } finally {
    userLoading.value = false
  }
}

async function deleteUser(userId) {
  if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
    return
  }
  
  try {
    await api.delete(`/auth/admin/users/${userId}`)
    await fetchUsers()
  } catch (err) {
    userError.value = err.response?.data?.detail || 'Failed to delete user'
  }
}

onMounted(() => {
  loadSettings()
  fetchCategories()
  if (authStore.user?.is_admin) {
    fetchUsers()
  }
})
</script>
