<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

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
  <div class="signup-container">
    <div class="signup-card">
      <!-- Header -->
      <div class="signup-header">
        <h1 class="signup-title">Create Account</h1>
        <p class="signup-subtitle">Join us to analyze your resume</p>
      </div>

      <!-- Signup Form -->
      <form @submit.prevent="handleSignup" class="signup-form">
        <!-- Name Field -->
        <div class="form-group">
          <label for="name" class="form-label">
            Full Name
          </label>
          <input
            id="name"
            v-model="name"
            type="text"
            required
            class="form-input"
            placeholder="Enter your full name"
          />
        </div>

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

        <!-- Confirm Password Field -->
        <div class="form-group">
          <label for="confirmPassword" class="form-label">
            Confirm Password
          </label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            required
            class="form-input"
            placeholder="Confirm your password"
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

        <!-- Signup Button -->
        <button
          type="submit"
          :disabled="isSigningUp"
          class="signup-button"
        >
          <span v-if="isSigningUp">Creating account...</span>
          <span v-else>Create Account</span>
        </button>
      </form>

      <!-- Login Link -->
      <div class="login-link">
        <p class="login-text">
          Already have an account?
          <button
            @click="goToLogin"
            class="login-button-link"
          >
            Sign in here
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
.signup-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #016064 0%, #48AAAD 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.signup-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 3rem;
  width: 100%;
  max-width: 450px;
}

.signup-header {
  text-align: center;
  margin-bottom: 2rem;
}

.signup-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.signup-subtitle {
  color: #718096;
  font-size: 1.1rem;
}

.signup-form {
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

.signup-button {
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

.signup-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(1, 96, 100, 0.3);
}

.signup-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.login-link {
  text-align: center;
  margin-top: 2rem;
}

.login-text {
  color: #718096;
  font-size: 1rem;
}

.login-button-link {
  background: none;
  border: none;
  color: #48AAAD;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.3s ease;
  margin-left: 0.5rem;
}

.login-button-link:hover {
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
  .signup-card {
    padding: 2rem;
    margin: 1rem;
  }
  
  .signup-title {
    font-size: 2rem;
  }
}
</style> 