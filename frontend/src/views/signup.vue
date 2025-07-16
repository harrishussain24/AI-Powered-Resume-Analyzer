<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import '../assets/signup.css'

const router = useRouter()
const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const isSigningUp = ref(false)
const error = ref('')
const success = ref('')

const handleSignup = async () => {
  if (!name.value || !email.value || !password.value || !confirmPassword.value) {
    error.value = 'Please fill in all fields'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  if (password.value.length < 6) {
    error.value = 'Password must be at least 6 characters long'
    return
  }

  isSigningUp.value = true
  error.value = ''
  success.value = ''

  try {
    const response = await axios.post('https://ai-powered-resume-analyzer-u0hx.onrender.com/auth/register', {
      name: name.value,
      email: email.value,
      password: password.value
    })

    success.value = 'Account created successfully! Redirecting to login...'
    
    // Redirect to login page after successful signup
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Signup failed. Please try again.'
  } finally {
    isSigningUp.value = false
  }
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-[#016064] to-[#48AAAD] flex items-center justify-center p-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-xl p-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">Create Account</h1>
        <p class="text-gray-600">Join us to analyze your resume</p>
      </div>
      <!-- Signup Form -->
      <form @submit.prevent="handleSignup" class="flex flex-col gap-6">
        <!-- Name Field -->
        <div class="flex flex-col gap-2">
          <label for="name" class="font-semibold text-gray-700 text-sm">Full Name</label>
          <input
            id="name"
            v-model="name"
            type="text"
            required
            class="w-full px-4 py-3 border-2 border-[#48AAAD] rounded-lg focus:ring-2 focus:ring-[#016064] focus:border-[#016064] transition text-[#016064] bg-white placeholder-gray-400"
            placeholder="Enter your full name"
          />
        </div>
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
        <!-- Confirm Password Field -->
        <div class="flex flex-col gap-2">
          <label for="confirmPassword" class="font-semibold text-gray-700 text-sm">Confirm Password</label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            required
            class="w-full px-4 py-3 border-2 border-[#48AAAD] rounded-lg focus:ring-2 focus:ring-[#016064] focus:border-[#016064] transition text-[#016064] bg-white placeholder-gray-400"
            placeholder="Confirm your password"
          />
        </div>
        <!-- Error Message -->
        <div v-if="error" class="text-red-600 text-sm bg-red-50 p-3 rounded-lg">❌ {{ error }}</div>
        <!-- Success Message -->
        <div v-if="success" class="text-green-600 text-sm bg-green-50 p-3 rounded-lg">✅ {{ success }}</div>
        <!-- Signup Button -->
        <button
          type="submit"
          :disabled="isSigningUp"
          class="w-full bg-gradient-to-r from-[#016064] to-[#48AAAD] text-white py-3 px-4 rounded-lg font-medium hover:from-[#014d50] hover:to-[#3a8a8d] focus:ring-2 focus:ring-[#016064] focus:ring-offset-2 transition disabled:opacity-50 disabled:cursor-not-allowed mt-2"
        >
          <span v-if="isSigningUp">Creating account...</span>
          <span v-else>Create Account</span>
        </button>
      </form>
      <!-- Login Link -->
      <div class="text-center mt-6">
        <p class="text-gray-600">
          Already have an account?
          <button
            @click="goToLogin"
            class="text-[#48AAAD] hover:text-[#016064] font-medium transition ml-1"
          >
            Sign in here
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