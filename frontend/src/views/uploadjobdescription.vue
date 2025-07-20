<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useResumeStore } from '../stores/parseddatastore'
import axios from 'axios'
import '../assets/uploadjobdescription.css'

const store = useResumeStore()
const router = useRouter()

const jobDescription = ref('')
const isSubmitting = ref(false)
const error = ref(null)
const analysisProgress = ref(0)
const analysisStage = ref('')
const showProgress = ref(false)

const analyzeJobDescription = async () => {
  if (!jobDescription.value.trim()) return

  isSubmitting.value = true
  showProgress.value = true
  error.value = null
  analysisProgress.value = 0
  analysisStage.value = 'Preparing analysis...'

  try {
    // Simulate analysis progress
    const progressInterval = setInterval(() => {
      if (analysisProgress.value < 90) {
        analysisProgress.value += Math.random() * 20
        if (analysisProgress.value < 40) {
          analysisStage.value = 'Extracting job details...'
        } else if (analysisProgress.value < 70) {
          analysisStage.value = 'Identifying required skills...'
        } else if (analysisProgress.value < 90) {
          analysisStage.value = 'Analyzing requirements...'
        }
      }
    }, 150)

    const response = await axios.post('https://ai-powered-resume-analyzer-u0hx.onrender.com/analyze-job', {
      description: jobDescription.value
    })

    clearInterval(progressInterval)
    analysisProgress.value = 100
    analysisStage.value = 'Analysis complete!'

    // Small delay to show completion
    setTimeout(() => {
      showProgress.value = false
    }, 1000)

    store.setJobDescription(response.data)
    // Don't navigate to next page, just store the result
  } catch (err) {
    error.value = err.response?.data?.message || err.message
    showProgress.value = false
  } finally {
    isSubmitting.value = false
  }
}

const showFinalResults = () => {
  router.push('/match-results')
}
</script>

<template>
  <!-- Main Content -->
  <div>
    <!-- Heading Section -->
    <div class="heading-section">
      <h2>Upload Job Description</h2>
    </div>

    <!-- Progress Indicator -->
    <div v-if="showProgress" class="progress-container">
      <div class="progress-card">
        <div class="progress-header">
          <div class="progress-icon">🔍</div>
          <h3 class="progress-title">Analyzing Job Description</h3>
        </div>
        <div class="progress-bar-container">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: analysisProgress + '%' }"></div>
          </div>
          <div class="progress-text">{{ Math.round(analysisProgress) }}%</div>
        </div>
        <div class="progress-stage">{{ analysisStage }}</div>
        <div class="progress-spinner">
          <div class="spinner"></div>
        </div>
      </div>
    </div>

    <!-- Job Description Input Section -->
    <div class="job-description-container">
      <div class="job-description-header">
        <h2 class="job-description-title">Job Description</h2>
        <p class="job-description-subtitle">Paste the job description here</p>
      </div>
      <div class="job-description-divider"></div>
      <div class="job-description-content">
        <textarea 
          v-model="jobDescription" 
          rows="12" 
          class="job-description-textarea"
          placeholder="Paste the job description here..."
        ></textarea>
        <div class="button-container">
          <button 
            @click="analyzeJobDescription" 
            :disabled="isSubmitting" 
            class="analyze-button"
          >
            <span class="button-text">{{ isSubmitting ? 'Analyzing...' : 'Analyze Job Description' }}</span>
            <span class="button-icon">🔍</span>
          </button>
        </div>
        <div v-if="error" class="error-message">❌ {{ error }}</div>
      </div>
    </div>

    <!-- Parsed Job Description Section -->
    <div v-if="store.jobDescriptionData" class="job-data-container">
      <div class="job-data-header">
        <h2 class="job-data-title">Job Description Information</h2>
        <p class="job-data-subtitle">Parsed data from your job description</p>
      </div>
      <div class="job-data-divider"></div>
      <div class="job-data-content">
        <div class="job-section">
          <h3 class="section-title">Job Details</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">Job Title:</span>
              <span class="info-value">{{ store.jobDescriptionData.analysis?.title || store.jobDescriptionData.title || 'N/A' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Experience Required:</span>
              <span class="info-value">{{ store.jobDescriptionData.analysis?.experience || store.jobDescriptionData.experience || 'N/A' }}</span>
            </div>
          </div>
        </div>
        <div class="job-section">
          <h3 class="section-title">Required Skills</h3>
          <div class="skills-container">
            <span v-if="(store.jobDescriptionData.analysis?.skills && store.jobDescriptionData.analysis.skills.length) || (store.jobDescriptionData.skills && store.jobDescriptionData.skills.length)" 
                  class="skill-tag" 
                  v-for="skill in (store.jobDescriptionData.analysis?.skills || store.jobDescriptionData.skills || [])" 
                  :key="skill">
              {{ skill }}
            </span>
            <span v-else class="no-data">No skills found</span>
          </div>
        </div>
        <div v-if="(store.jobDescriptionData.analysis?.education && store.jobDescriptionData.analysis.education.length) || (store.jobDescriptionData.education && store.jobDescriptionData.education.length)" class="job-section">
          <h3 class="section-title">Education Requirements</h3>
          <div class="education-container">
            <span v-for="edu in (store.jobDescriptionData.analysis?.education || store.jobDescriptionData.education || [])" 
                  :key="edu" 
                  class="education-tag">
              {{ edu }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Show Final Results Button -->
    <div v-if="store.jobDescriptionData" class="continue-button-container">
      <button @click="showFinalResults" class="continue-button">
        <span class="button-text">Show Final Results</span>
        <span class="button-icon">📊</span>
      </button>
    </div>
  </div>
</template>

