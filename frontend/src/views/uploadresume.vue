<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useResumeStore } from '../stores/parseddatastore'
import axios from 'axios'
import '../assets/uploadresume.css'

const resumeStore = useResumeStore()
const router = useRouter()
const selectedFile = ref(null)
const fileInput = ref(null)
const isSubmitting = ref(false)
const uploadResult = ref(null)
const uploadError = ref(null)
const resumeData = ref(null)
const uploadedFiles = ref([])
const uploadProgress = ref(0)
const uploadStage = ref('')
const showProgress = ref(false)
const user = ref(null)
isSubmitting.value = false

// Check if user is logged in
const checkAuthStatus = () => {
  const authToken = localStorage.getItem('authToken')
  const userData = localStorage.getItem('user')
  
  if (authToken && userData) {
    try {
      user.value = JSON.parse(userData)
    } catch (e) {
      // Clear invalid data
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
      user.value = null
    }
  } else {
    user.value = null
  }
}

const logout = () => {
  localStorage.removeItem('authToken')
  localStorage.removeItem('user')
  user.value = null
}

// Check auth status on component mount
checkAuthStatus()

const goToJobDescriptionView = () => {
  if (!resumeData.value) return
  resumeStore.setResume(resumeData.value)
  router.push('/job-description')
}

const triggerFileSelect = () => {
  fileInput.value?.click()
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file && file.type === 'application/pdf') {
    selectedFile.value = file
    uploadError.value = null
    handleSubmit() // Auto submit after selection
  } else {
    selectedFile.value = null
    uploadError.value = 'Please select a valid PDF file.'
  }
}

const handleSubmit = async () => {
  if (!selectedFile.value) return

  isSubmitting.value = true
  showProgress.value = true
  uploadError.value = null
  uploadResult.value = null
  uploadProgress.value = 0
  uploadStage.value = 'Preparing file...'

  try {
    // Simulate upload progress
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += Math.random() * 15
        if (uploadProgress.value < 30) {
          uploadStage.value = 'Uploading file...'
        } else if (uploadProgress.value < 60) {
          uploadStage.value = 'Processing PDF...'
        } else if (uploadProgress.value < 90) {
          uploadStage.value = 'Analyzing resume content...'
        }
      }
    }, 200)

    const formData = new FormData()
    formData.append('file', selectedFile.value)

    const response = await axios.post('https://ai-powered-resume-analyzer-u0hx.onrender.com/upload-resume/', formData)

    clearInterval(progressInterval)
    uploadProgress.value = 100
    uploadStage.value = 'Analysis complete!'

    // Small delay to show completion
    setTimeout(() => {
      showProgress.value = false
    }, 1000)

    resumeData.value = response.data
    uploadedFiles.value = [{
      name: selectedFile.value.name,
      size: (selectedFile.value.size / 1024 / 1024).toFixed(2) + ' MB',
      uploadedAt: new Date().toLocaleDateString(),
    }]
    uploadResult.value = response.data
  } catch (err) {
    uploadError.value = err.response?.data?.message || err.message
    showProgress.value = false
  } finally {
    isSubmitting.value = false
  }
}

const deleteFile = (index) => {
  uploadedFiles.value.splice(index, 1)
  // Clear resume data when file is deleted
  resumeData.value = null
  uploadResult.value = null
  selectedFile.value = null
  // Reset file input
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>

<template>
  <!-- Main Content -->
  <div class="uploadresume-root">
    <!-- Card Container -->
    <div class="upload-container">
      <!-- Header Bar: Heading and Auth Button -->
      <div class="header-bar">
        <h2 class="header-title">Upload Your Resume</h2>
        <div class="auth-container-bar">
          <div v-if="user" class="user-info">
            <span class="user-name">Welcome, {{ user.name || user.email }}</span>
            <button @click="logout" class="logout-button">Logout</button>
          </div>
          <div v-else class="login-button-container-bar">
            <button @click="router.push('/login')" class="login-button-main-bar">Login / Signup</button>
          </div>
        </div>
      </div>

      <!-- Upload Area -->
      <div class="upload-area" @click="triggerFileSelect">
        <span class="upload-icon">📄</span>
        <div class="upload-text">Click here to upload your file or drag.</div>
        <span class="upload-format">Supported Format: <u>PDF (5mb max)</u></span>
        <input ref="fileInput" type="file" accept="application/pdf" class="hidden" @change="handleFileChange" />
      </div>

      <!-- Progress Indicator -->
      <div v-if="showProgress" class="progress-container">
        <div class="progress-card">
          <div class="progress-header">
            <div class="progress-icon">📄</div>
            <h3 class="progress-title">Processing Resume</h3>
          </div>
          <div class="progress-bar-container">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
            </div>
            <div class="progress-text">{{ Math.round(uploadProgress) }}%</div>
          </div>
          <div class="progress-stage">{{ uploadStage }}</div>
          <div class="progress-spinner">
            <div class="spinner"></div>
          </div>
        </div>
      </div>

      <!-- Attached Files Section -->
      <div class="attached-files-container">
        <div class="attached-files-header">
          <h2 class="attached-files-title">Attached File</h2>
          <p class="attached-files-subtitle">Here you can see your uploaded file</p>
        </div>
        <div class="attached-files-divider"></div>
        <div class="attached-files-table-header">
          <div class="file-header-item">File Name</div>
          <div class="file-header-item">Size</div>
          <div class="file-header-item">Uploaded At</div>
          <div class="file-header-item">Action</div>
        </div>
        <div class="attached-files-content">
          <div v-for="(file, index) in uploadedFiles" :key="index" class="file-row">
            <div class="file-item">{{ file.name }}</div>
            <div class="file-item">{{ file.size }}</div>
            <div class="file-item">{{ file.uploadedAt }}</div>
            <div class="file-item">
              <button class="action-btn delete-btn" @click="deleteFile(index)">Delete</button>
            </div>
          </div>
          <div v-if="!uploadedFiles.length" class="no-files-message">No files uploaded yet.</div>
        </div>
      </div>

      <!-- Resume Data Section -->
      <div v-if="resumeData" class="resume-data-container">
        <div class="resume-data-header">
          <h2 class="resume-data-title">Resume Information</h2>
          <p class="resume-data-subtitle">Parsed data from your uploaded resume</p>
        </div>
        <div class="resume-data-divider"></div>
        <div class="resume-data-content">
          <div class="resume-section">
            <h3 class="section-title">Personal Information</h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">Name:</span>
                <span class="info-value">{{ resumeData.analysis.name || 'N/A' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Email:</span>
                <span class="info-value">{{ resumeData.analysis.email || 'N/A' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Phone:</span>
                <span class="info-value">{{ resumeData.analysis.phone || 'N/A' }}</span>
              </div>
            </div>
          </div>
          <div class="resume-section">
            <h3 class="section-title">Skills</h3>
            <div class="skills-container">
              <span v-if="resumeData.analysis.skills?.length" class="skill-tag" v-for="skill in resumeData.analysis.skills" :key="skill">
                {{ skill }}
              </span>
              <span v-else class="no-data">No skills found.</span>
            </div>
          </div>
          <div v-if="resumeData.analysis.experience?.length" class="resume-section">
            <h3 class="section-title">Experience</h3>
            <div class="experience-list">
              <div v-for="(exp, idx) in resumeData.analysis.experience" :key="idx" class="experience-item">
                <div class="experience-header">
                  <span class="job-title">{{ exp.title || 'N/A' }}</span>
                  <span class="company-name">{{ exp.company || '' }}</span>
                </div>
                <div class="experience-meta">
                  <span v-if="exp.location" class="location">{{ exp.location }}</span>
                  <span v-if="exp.dates" class="dates">{{ exp.dates }}</span>
                </div>
                <ul v-if="exp.bullets?.length" class="experience-bullets">
                  <li v-for="(bullet, bidx) in exp.bullets" :key="bidx">{{ bullet }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Go to Job Description Button -->
      <div v-if="resumeData" class="continue-button-container">
        <button @click="goToJobDescriptionView" class="continue-button">
          <span class="button-text">Continue to Job Description</span>
          <span class="button-icon">→</span>
        </button>
      </div>

      <!-- Error Message -->
      <div v-if="uploadError" class="error-message">
        {{ uploadError }}
      </div>
    </div>
  </div>
</template>
