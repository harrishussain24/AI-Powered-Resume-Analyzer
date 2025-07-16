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
        <div class="header-auth">
          <div v-if="user" class="user-info">
            <span class="user-welcome">Welcome, {{ user.name || user.email }}</span>
            <button @click="logout" class="logout-btn">Logout</button>
          </div>
          <div v-else class="login-btn-wrap">
            <button @click="router.push('/login')" class="login-btn">Login / Signup</button>
          </div>
        </div>
      </div>

      <!-- Upload Area -->
      <div class="upload-area" @click="triggerFileSelect">
        <span class="upload-icon">📄</span>
        <div class="upload-instructions">Click here to upload your file or drag.</div>
        <span class="upload-format">Supported Format: <u>PDF (5mb max)</u></span>
      </div>
      <input type="file" accept=".pdf" ref="fileInput" @change="handleFileChange" class="file-input" />

      <!-- Progress Indicator -->
      <div v-if="showProgress" class="progress-wrap">
        <div class="progress-card">
          <div class="progress-header">
            <div class="progress-icon">📄</div>
            <h3 class="progress-title">Processing Resume</h3>
          </div>
          <div class="progress-bar-wrap">
            <div class="progress-bar-bg">
              <div class="progress-bar" :style="{ width: uploadProgress + '%' }"></div>
            </div>
            <div class="progress-percent">{{ Math.round(uploadProgress) }}%</div>
          </div>
          <div class="progress-stage">{{ uploadStage }}</div>
          <div class="progress-spinner-wrap">
            <div class="progress-spinner"></div>
          </div>
        </div>
      </div>

      <!-- Attached Files Section -->
      <div class="file-table-wrap">
        <div class="file-table-header">
          <h2 class="file-table-title">Attached File</h2>
          <p class="file-table-desc">Here you can see your uploaded file</p>
        </div>
        <div class="file-table-divider"></div>
        <div class="file-table-row file-table-row-head">
          <div>File Name</div>
          <div>Size</div>
          <div>Uploaded At</div>
          <div>Action</div>
        </div>
        <div class="file-table-divider"></div>
        <div class="file-table-body">
          <div v-for="(file, index) in uploadedFiles" :key="index" class="file-table-row">
            <div>{{ file.name }}</div>
            <div>{{ file.size }}</div>
            <div>{{ file.uploadedAt }}</div>
            <div>
              <button class="delete-btn" @click="deleteFile(index)">Delete</button>
            </div>
          </div>
          <div v-if="!uploadedFiles.length" class="file-table-empty">No files uploaded yet.</div>
        </div>
      </div>

      <!-- Resume Data Section -->
      <div v-if="resumeData" class="resume-data-wrap">
        <div class="resume-data-header">
          <h2 class="resume-data-title">Resume Information</h2>
          <p class="resume-data-desc">Parsed data from your uploaded resume</p>
        </div>
        <div class="resume-data-divider"></div>
        <div class="resume-data-body">
          <div class="resume-personal-info">
            <h3 class="resume-section-title">Personal Information</h3>
            <div class="resume-personal-grid">
              <div>
                <span class="resume-label">Name:</span>
                <span class="resume-value">{{ resumeData.analysis.name || 'N/A' }}</span>
              </div>
              <div>
                <span class="resume-label">Email:</span>
                <span class="resume-value">{{ resumeData.analysis.email || 'N/A' }}</span>
              </div>
              <div>
                <span class="resume-label">Phone:</span>
                <span class="resume-value">{{ resumeData.analysis.phone || 'N/A' }}</span>
              </div>
            </div>
          </div>
          <div class="resume-skills">
            <h3 class="resume-section-title">Skills</h3>
            <div class="resume-skills-list">
              <span v-if="resumeData.analysis.skills?.length" class="resume-skill" v-for="skill in resumeData.analysis.skills" :key="skill">
                {{ skill }}
              </span>
              <span v-else class="resume-skill-empty">No skills found.</span>
            </div>
          </div>
          <!-- Add more parsed data sections as needed -->
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="uploadError" class="error-message">
        {{ uploadError }}
      </div>
    </div>
  </div>
</template>
