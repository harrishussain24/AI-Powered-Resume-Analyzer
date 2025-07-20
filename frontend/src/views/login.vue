<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import '../assets/login.css'

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
  <div class="login-container">
    <div class="login-card">
      <!-- Header -->
      <div class="login-header">
        <h1 class="login-title">Welcome Back</h1>
        <p class="login-subtitle">Sign in to your account</p>
      </div>
      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="login-form">
        <!-- Email Field -->
        <div class="form-group">
          <label for="email" class="form-label">Email Address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="form-input"
            placeholder="Enter your email"
          />
        </div>
        <!-- Password Field -->
        <div class="form-group">
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="form-input"
            placeholder="Enter your password"
          />
        </div>
        <!-- Error Message -->
        <div v-if="error" class="error-message">❌ {{ error }}</div>
        <!-- Success Message -->
        <div v-if="success" class="success-message">✅ {{ success }}</div>
        <!-- Login Button -->
        <button
          type="submit"
          :disabled="isLoggingIn"
          class="login-button"
        >
          <span v-if="isLoggingIn">Signing in...</span>
          <span v-else>Sign In</span>
        </button>
      </form>
      <!-- Sign Up Link -->
      <div class="signup-link">
        <span class="signup-text">Don't have an account?</span>
        <button
          @click="goToSignup"
          class="signup-button"
        >
          Sign up here
        </button>
      </div>
      <!-- Back to Home -->
      <div class="back-link">
        <button
          @click="router.push('/')"
          class="back-button"
        >
          ← Back to Resume Analyzer
        </button>
      </div>
    </div>
  </div>
</template> 