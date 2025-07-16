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
  <div class="jobdesc-root">
    <!-- Heading Section -->
    <div class="jobdesc-header">
      <h2 class="jobdesc-title">Upload Job Description</h2>
      <div class="jobdesc-header-divider"></div>
    </div>

    <!-- Progress Indicator -->
    <div v-if="showProgress" class="jobdesc-progress-wrap">
      <div class="jobdesc-progress-card">
        <div class="jobdesc-progress-header">
          <div class="jobdesc-progress-icon">🔍</div>
          <h3 class="jobdesc-progress-title">Analyzing Job Description</h3>
        </div>
        <div class="jobdesc-progress-bar-wrap">
          <div class="jobdesc-progress-bar-bg">
            <div class="jobdesc-progress-bar" :style="{ width: analysisProgress + '%' }"></div>
          </div>
          <div class="jobdesc-progress-percent">{{ Math.round(analysisProgress) }}%</div>
        </div>
        <div class="jobdesc-progress-stage">{{ analysisStage }}</div>
        <div class="jobdesc-progress-spinner-wrap">
          <div class="jobdesc-progress-spinner"></div>
        </div>
      </div>
    </div>

    <!-- Job Description Input Section -->
    <div class="jobdesc-form-wrap">
      <div class="jobdesc-form-header">
        <h2 class="jobdesc-form-title">Job Description</h2>
        <p class="jobdesc-form-desc">Paste the job description here</p>
      </div>
      <div class="jobdesc-form-divider"></div>
      <div class="jobdesc-form-body">
        <textarea 
          v-model="jobDescription" 
          rows="12" 
          class="jobdesc-textarea"
          placeholder="Paste the job description here..."
        ></textarea>
        <div class="jobdesc-form-btn-wrap">
          <button 
            @click="analyzeJobDescription" 
            :disabled="isSubmitting" 
            class="jobdesc-analyze-btn"
          >
            <span>{{ isSubmitting ? 'Analyzing...' : 'Analyze Job Description' }}</span>
            <span class="jobdesc-analyze-icon">🔍</span>
          </button>
        </div>
        <div v-if="error" class="jobdesc-error">❌ {{ error }}</div>
      </div>
    </div>

    <!-- Parsed Job Description Section -->
    <div v-if="store.jobDescriptionData" class="jobdesc-parsed-wrap">
      <div class="jobdesc-parsed-header">
        <h2 class="jobdesc-parsed-title">Job Description Information</h2>
        <p class="jobdesc-parsed-desc">Parsed data from your job description</p>
      </div>
      <div class="jobdesc-parsed-divider"></div>
      <div class="jobdesc-parsed-body">
        <div class="jobdesc-details">
          <h3 class="jobdesc-section-title">Job Details</h3>
          <div class="jobdesc-details-grid">
            <div>
              <span class="jobdesc-label">Job Title:</span>
              <span class="jobdesc-value">{{ store.jobDescriptionData.analysis?.title || store.jobDescriptionData.title || 'N/A' }}</span>
            </div>
            <div>
              <span class="jobdesc-label">Experience Required:</span>
              <span class="jobdesc-value">{{ store.jobDescriptionData.analysis?.experience || store.jobDescriptionData.experience || 'N/A' }}</span>
            </div>
          </div>
        </div>
        <div class="jobdesc-skills">
          <h3 class="jobdesc-section-title">Required Skills</h3>
          <div class="jobdesc-skills-list">
            <span v-if="(store.jobDescriptionData.analysis?.skills && store.jobDescriptionData.analysis.skills.length) || (store.jobDescriptionData.skills && store.jobDescriptionData.skills.length)" 
                  class="jobdesc-skill" 
                  v-for="skill in (store.jobDescriptionData.analysis?.skills || store.jobDescriptionData.skills || [])" 
                  :key="skill">
              {{ skill }}
            </span>
            <span v-else class="jobdesc-skill-empty">No skills found</span>
          </div>
        </div>
        <div v-if="(store.jobDescriptionData.analysis?.education && store.jobDescriptionData.analysis.education.length) || (store.jobDescriptionData.education && store.jobDescriptionData.education.length)" class="jobdesc-education">
          <h3 class="jobdesc-section-title">Education Requirements</h3>
          <div class="jobdesc-education-list">
            <span v-for="edu in (store.jobDescriptionData.analysis?.education || store.jobDescriptionData.education || [])" 
                  :key="edu" 
                  class="jobdesc-education-item">
              {{ edu }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Show Final Results Button -->
    <div v-if="store.jobDescriptionData" class="jobdesc-final-btn-wrap">
      <button @click="showFinalResults" class="jobdesc-final-btn">
        <span>Show Final Results</span>
        <span class="jobdesc-final-icon">📊</span>
      </button>
    </div>
  </div>
</template>

