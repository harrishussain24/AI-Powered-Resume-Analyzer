<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const email = ref('')
const password = ref('')
const isLoggingIn = ref(false)
const error = ref('')
const success = ref('')

const handleLogin = async () => {
  if (!email.value || !password.value) {
    error.value = 'Please fill in all fields'
    return
  }

  isLoggingIn.value = true
  error.value = ''
  success.value = ''

  try {
    const response = await axios.post('https://ai-powered-resume-analyzer-u0hx.onrender.com/auth/login', {
      email: email.value,
      password: password.value
    })

    // Store the token in localStorage
    localStorage.setItem('authToken', response.data.access_token)
    localStorage.setItem('user', JSON.stringify(response.data.user))
    
    success.value = 'Login successful! Redirecting...'
    
    // Redirect to resume upload page after successful login
    setTimeout(() => {
      router.push('/')
    }, 1500)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed. Please try again.'
  } finally {
    isLoggingIn.value = false
  }
}

const goToSignup = () => {
  router.push('/signup')
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50 flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-2xl shadow-xl p-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">Welcome Back</h1>
        <p class="text-gray-600">Sign in to your account</p>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="space-y-6">
        <!-- Email Field -->
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
            Email Address
          </label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200"
            placeholder="Enter your email"
          />
        </div>

        <!-- Password Field -->
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
            Password
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200"
            placeholder="Enter your password"
          />
        </div>

        <!-- Error Message -->
        <div v-if="error" class="text-red-600 text-sm bg-red-50 p-3 rounded-lg">
          ❌ {{ error }}
        </div>

        <!-- Success Message -->
        <div v-if="success" class="text-green-600 text-sm bg-green-50 p-3 rounded-lg">
          ✅ {{ success }}
        </div>

        <!-- Login Button -->
        <button
          type="submit"
          :disabled="isLoggingIn"
          class="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 px-4 rounded-lg font-medium hover:from-purple-700 hover:to-pink-700 focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isLoggingIn">Signing in...</span>
          <span v-else>Sign In</span>
        </button>
      </form>

      <!-- Sign Up Link -->
      <div class="text-center mt-6">
        <p class="text-gray-600">
          Don't have an account?
          <button
            @click="goToSignup"
            class="text-purple-600 hover:text-purple-700 font-medium transition duration-200"
          >
            Sign up here
          </button>
        </p>
      </div>

      <!-- Back to Home -->
      <div class="text-center mt-4">
        <button
          @click="router.push('/')"
          class="text-gray-500 hover:text-gray-700 text-sm transition duration-200"
        >
          ← Back to Resume Analyzer
        </button>
      </div>
    </div>
  </div>
</template> 