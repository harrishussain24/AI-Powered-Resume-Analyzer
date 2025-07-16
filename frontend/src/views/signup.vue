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
  <div class="signup-root">
    <div class="signup-container">
      <!-- Header -->
      <div class="signup-header">
        <h1 class="signup-title">Create Account</h1>
        <p class="signup-subtitle">Join us to analyze your resume</p>
      </div>
      <!-- Signup Form -->
      <form @submit.prevent="handleSignup" class="signup-form">
        <!-- Name Field -->
        <div class="signup-form-group">
          <label for="name" class="signup-label">Full Name</label>
          <input
            id="name"
            v-model="name"
            type="text"
            required
            class="signup-input"
            placeholder="Enter your full name"
          />
        </div>
        <!-- Email Field -->
        <div class="signup-form-group">
          <label for="email" class="signup-label">Email Address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="signup-input"
            placeholder="Enter your email"
          />
        </div>
        <!-- Password Field -->
        <div class="signup-form-group">
          <label for="password" class="signup-label">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="signup-input"
            placeholder="Enter your password"
          />
        </div>
        <!-- Confirm Password Field -->
        <div class="signup-form-group">
          <label for="confirmPassword" class="signup-label">Confirm Password</label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            required
            class="signup-input"
            placeholder="Confirm your password"
          />
        </div>
        <!-- Error Message -->
        <div v-if="error" class="signup-error">❌ {{ error }}</div>
        <!-- Success Message -->
        <div v-if="success" class="signup-success">✅ {{ success }}</div>
        <!-- Signup Button -->
        <button
          type="submit"
          :disabled="isSigningUp"
          class="signup-btn"
        >
          <span v-if="isSigningUp">Creating account...</span>
          <span v-else>Create Account</span>
        </button>
      </form>
      <!-- Login Link -->
      <div class="signup-login-link">
        <p>
          Already have an account?
          <button
            @click="goToLogin"
            class="signup-login-btn"
          >
            Sign in here
          </button>
        </p>
      </div>
      <!-- Back to Home -->
      <div class="signup-back-home">
        <button
          @click="router.push('/')"
          class="signup-back-btn"
        >
          ← Back to Resume Analyzer
        </button>
      </div>
    </div>
  </div>
</template> 