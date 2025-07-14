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
          <label for="email" class="form-label">
            Email Address
          </label>
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
          <label for="password" class="form-label">
            Password
          </label>
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
        <div v-if="error" class="error-message">
          ❌ {{ error }}
        </div>

        <!-- Success Message -->
        <div v-if="success" class="success-message">
          ✅ {{ success }}
        </div>

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
        <p class="signup-text">
          Don't have an account?
          <button
            @click="goToSignup"
            class="signup-button"
          >
            Sign up here
          </button>
        </p>
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

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #016064 0%, #48AAAD 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.login-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 3rem;
  width: 100%;
  max-width: 450px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.login-subtitle {
  color: #718096;
  font-size: 1.1rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 600;
  color: #4a5568;
  font-size: 0.95rem;
}

.form-input {
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #f8fafc;
}

.form-input:focus {
  outline: none;
  border-color: #48AAAD;
  background: white;
  box-shadow: 0 0 0 3px rgba(72, 170, 173, 0.1);
}

input[type='file'],
input[type='text'],
input[type='email'],
input[type='password'] {
  background: #fff !important;
  color: #016064 !important;
  border: 2px solid #48AAAD;
  border-radius: 0.75rem;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  margin: 0.25rem 0;
  box-shadow: 0 2px 8px rgba(1,96,100,0.04);
}

input[type='file']:focus,
input[type='text']:focus,
input[type='email']:focus,
input[type='password']:focus {
  outline: none;
  border-color: #016064;
  background: #f4f8f8;
}

.error-message {
  background: #fed7d7;
  color: #c53030;
  padding: 1rem;
  border-radius: 12px;
  font-size: 0.9rem;
  border: 1px solid #feb2b2;
}

.success-message {
  background: #c6f6d5;
  color: #2f855a;
  padding: 1rem;
  border-radius: 12px;
  font-size: 0.9rem;
  border: 1px solid #9ae6b4;
}

.login-button {
  background: linear-gradient(135deg, #016064 0%, #48AAAD 100%);
  color: white;
  padding: 1rem;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(1, 96, 100, 0.3);
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.signup-link {
  text-align: center;
  margin-top: 2rem;
}

.signup-text {
  color: #718096;
  font-size: 1rem;
}

.signup-button {
  background: none;
  border: none;
  color: #48AAAD;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.3s ease;
  margin-left: 0.5rem;
}

.signup-button:hover {
  color: #016064;
  text-decoration: underline;
}

.back-link {
  text-align: center;
  margin-top: 1.5rem;
}

.back-button {
  background: none;
  border: none;
  color: #a0aec0;
  font-size: 0.9rem;
  cursor: pointer;
  transition: color 0.3s ease;
}

.back-button:hover {
  color: #4a5568;
}

@media (max-width: 480px) {
  .login-card {
    padding: 2rem;
    margin: 1rem;
  }
  
  .login-title {
    font-size: 2rem;
  }
}
</style> 