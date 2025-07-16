<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
// import '../assets/login.css'

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
  <div class="min-h-screen bg-gradient-to-br from-[#016064] to-[#48AAAD] flex items-center justify-center p-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-xl p-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">Welcome Back</h1>
        <p class="text-gray-600">Sign in to your account</p>
      </div>
      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="flex flex-col gap-6">
        <!-- Email Field -->
        <div class="flex flex-col gap-2">
          <label for="email" class="font-semibold text-gray-700 text-sm">Email Address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="w-full px-4 py-3 border-2 border-[#48AAAD] rounded-lg focus:ring-2 focus:ring-[#016064] focus:border-[#016064] transition text-[#016064] bg-white placeholder-gray-400"
            placeholder="Enter your email"
          />
        </div>
        <!-- Password Field -->
        <div class="flex flex-col gap-2">
          <label for="password" class="font-semibold text-gray-700 text-sm">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="w-full px-4 py-3 border-2 border-[#48AAAD] rounded-lg focus:ring-2 focus:ring-[#016064] focus:border-[#016064] transition text-[#016064] bg-white placeholder-gray-400"
            placeholder="Enter your password"
          />
        </div>
        <!-- Error Message -->
        <div v-if="error" class="text-red-600 text-sm bg-red-50 p-3 rounded-lg">❌ {{ error }}</div>
        <!-- Success Message -->
        <div v-if="success" class="text-green-600 text-sm bg-green-50 p-3 rounded-lg">✅ {{ success }}</div>
        <!-- Login Button -->
        <button
          type="submit"
          :disabled="isLoggingIn"
          class="w-full bg-gradient-to-r from-[#016064] to-[#48AAAD] text-white py-3 px-4 rounded-lg font-medium hover:from-[#014d50] hover:to-[#3a8a8d] focus:ring-2 focus:ring-[#016064] focus:ring-offset-2 transition disabled:opacity-50 disabled:cursor-not-allowed mt-2"
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
            class="text-[#48AAAD] hover:text-[#016064] font-medium transition ml-1"
          >
            Sign up here
          </button>
        </p>
      </div>
      <!-- Back to Home -->
      <div class="text-center mt-4">
        <button
          @click="router.push('/')"
          class="text-gray-500 hover:text-gray-700 text-sm transition"
        >
          ← Back to Resume Analyzer
        </button>
      </div>
    </div>
  </div>
</template> 