<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useResumeStore } from '../stores/parseddatastore'
import axios from 'axios'

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
  <div class="max-w-5xl mx-auto mt-24 p-6 bg-white rounded-lg shadow relative">
    <!-- Heading and Auth Section in Flex Row -->
    <div class="header-auth-row">
      <div class="heading-section mb-0">
        <h2 class="text-3xl font-bold text-gray-800 mb-0 ml-0">Upload Your Resume</h2>
      </div>
      <!-- Auth Section -->
      <div class="auth-container-static">
        <!-- Show user info when logged in -->
        <div v-if="user" class="user-info">
          <span class="user-name">Welcome, {{ user.name || user.email }}</span>
          <button @click="logout" class="logout-button">
            Logout
          </button>
        </div>
        <!-- Show login button when not logged in -->
        <div v-else class="login-button-container-static">
          <button
            @click="router.push('/login')"
            class="login-button-main-static"
          >
            Login / Signup
          </button>
        </div>
      </div>
    </div>

    <div class="h-px bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 ml-8 mr-8 mb-8"></div>

    <div class="upload-area" @click="triggerFileSelect">
      <span class="upload-icon">📄</span>
      <div class="upload-text">Click here to upload your file or drag.</div>
      <span class="upload-link">Supported Format: <u>PDF (5mb max)</u></span>
    </div>

    <input type="file" accept=".pdf" ref="fileInput" @change="handleFileChange" class="hidden" />

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
      
      <div class="attached-files-divider"></div>
      
      <div class="attached-files-content">
        <div v-for="(file, index) in uploadedFiles" :key="index" class="file-row">
          <div class="file-item">{{ file.name }}</div>
          <div class="file-item">{{ file.size }}</div>
          <div class="file-item">{{ file.uploadedAt }}</div>
          <div class="file-item">
            <button class="action-btn delete-btn" @click="deleteFile(index)">Delete</button>
          </div>
        </div>
        <div v-if="!uploadedFiles.length" class="no-files-message">
          No files uploaded yet.
        </div>
      </div>
    </div>

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
            <span v-else class="no-data">No skills found</span>
          </div>
        </div>

        <div v-if="resumeData.analysis.experience?.length" class="resume-section">
          <h3 class="section-title">Work Experience</h3>
          <div class="experience-list">
            <div v-for="(exp, index) in resumeData.analysis.experience" :key="index" class="experience-item">
              <div class="experience-header">
                <h4 class="job-title">{{ exp.title }}</h4>
                <span class="company-name">{{ exp.company }}</span>
              </div>
              <div class="experience-meta">
                <span class="location">{{ exp.location }}</span>
                <span class="dates">{{ exp.dates }}</span>
              </div>
              <ul class="experience-bullets">
                <li v-for="(bullet, i) in exp.bullets" :key="i">{{ bullet }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="resumeData" class="continue-button-container">
      <button @click="goToJobDescriptionView" class="continue-button">
        <span class="button-text">Continue to Job Description</span>
        <span class="button-icon">→</span>
      </button>
    </div>

    <div v-if="uploadError" class="mt-4 text-red-600 text-sm">
      ❌ {{ uploadError }}
    </div>
  </div>
</template>

<style scoped>
.header-auth-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0;
  padding-bottom: 0;
}
.heading-section {
  background-color: #016064;
  color: white;
  padding: 1.25rem 2.5rem;
  border-radius: 1rem;
  margin: 0;
  width: auto;
  display: flex;
  align-items: center;
}
.auth-container-static {
  display: flex;
  align-items: center;
  margin-left: 2rem;
}
.login-button-container-static {
  display: flex;
  align-items: center;
}
.login-button-main-static {
  background: linear-gradient(135deg, #48AAAD 0%, #016064 100%);
  color: white;
  padding: 0.85rem 2.5rem;
  min-width: 160px;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(1, 96, 100, 0.3);
  text-decoration: none;
  display: inline-block;
}
.login-button-main-static:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(1, 96, 100, 0.4);
  background: linear-gradient(135deg, #3a8a8d 0%, #014d50 100%);
}
.login-button-main-static:active {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(1, 96, 100, 0.3);
}
.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 2px solid #48AAAD;
}
.user-name {
  color: #016064;
  font-weight: 600;
  font-size: 0.95rem;
}
.logout-button {
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}
.logout-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
  background: linear-gradient(135deg, #b91c1c 0%, #dc2626 100%);
}
.upload-area {
  background: #fff;
  border: 2px solid #48AAAD;
  border-radius: 1.5rem; /* Large rounded corners */
  box-shadow: 0 4px 24px 0 rgba(30, 34, 90, 0.06);
  padding: 2.0rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: border-color 0.2s, box-shadow 0.2s;
  margin-bottom: 2rem;
  width: 65vw;
  margin-left: auto;
  margin-right: auto;
}

.upload-area:hover, .upload-area:focus-within {
  border-color: #016064; 
  box-shadow: 0 6px 32px 0 rgba(160, 132, 232, 0.12);
}

.upload-area .upload-icon {
  font-size: 2.5rem;
  color: #a084e8;
  margin-bottom: 1rem;
}

.upload-area .upload-text {
  color: #6c6f93;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.upload-area .upload-link {
  color: #48AAAD;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.2s;
}

.upload-area .upload-link:hover {
  color: #016064;
}

/* Attached Files Section */
.attached-files-container {
  width: 80%;
  margin: 2rem auto;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.attached-files-header {
  padding: 1.5rem 2rem 1rem 2rem;
}

.attached-files-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #016064;
  margin: 0 0 0.5rem 0;
}

.attached-files-subtitle {
  font-size: 1rem;
  color: #48AAAD;
  margin: 0;
}

.attached-files-divider {
  height: 1px;
  background: #48AAAD;
  margin: 0;
}

.attached-files-table-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem 2rem;
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.file-header-item {
  text-align: left;
}

.file-header-item:last-child {
  text-align: right;
}

.attached-files-content {
  padding: 0 2rem;
}

.file-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #f3f4f6;
  align-items: center;
}

.file-row:last-child {
  border-bottom: none;
}

.file-item {
  font-size: 0.875rem;
  color: #374151;
}

.file-item:last-child {
  text-align: right;
}

.action-btn {
  padding: 0.25rem 0.75rem;
  border: none;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.delete-btn {
  background: #ef4444;
  color: white;
}

.delete-btn:hover {
  background: #dc2626;
}

.no-files-message {
  text-align: center;
  color: #9ca3af;
  padding: 2rem;
  font-style: italic;
}

/* Resume Data Section */
.resume-data-container {
  width: 80%;
  margin: 2rem auto;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.resume-data-header {
  padding: 1.5rem 2rem 1rem 2rem;
}

.resume-data-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #016064;
  margin: 0 0 0.5rem 0;
}

.resume-data-subtitle {
  font-size: 1rem;
  color: #48AAAD;
  margin: 0;
}

.resume-data-divider {
  height: 1px;
  background: #48AAAD;
  margin: 0;
}

.resume-data-content {
  padding: 2rem;
}

.resume-section {
  margin-bottom: 2rem;
}

.resume-section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e5e7eb;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-weight: 600;
  color: #6b7280;
  font-size: 0.875rem;
}

.info-value {
  color: #374151;
  font-size: 1rem;
  word-break: break-word;
}

.skills-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tag {
  background: #016064;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 1.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  display: inline-block;
}

.no-data {
  color: #9ca3af;
  font-style: italic;
}

.experience-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.experience-item {
  padding: 1.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  background: #f9fafb;
}

.experience-header {
  margin-bottom: 0.75rem;
}

.job-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 0.25rem 0;
}

.company-name {
  font-size: 1rem;
  color: #016064;
  font-weight: 500;
}

.experience-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.location::before {
  content: "📍 ";
}

.dates::before {
  content: "📅 ";
}

.experience-bullets {
  margin: 0;
  padding-left: 1.5rem;
}

.experience-bullets li {
  color: #374151;
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.experience-bullets li:last-child {
  margin-bottom: 0;
}

/* Continue Button */
.continue-button-container {
  width: 80%;
  margin: 2rem auto;
  display: flex;
  justify-content: center;
  padding: 1rem 0;
}

.continue-button {
  background: linear-gradient(135deg, #016064 0%, #48AAAD 100%);
  color: white;
  border: none;
  border-radius: 2rem;
  padding: 1rem 2.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(1, 96, 100, 0.3);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  position: relative;
  overflow: hidden;
}

.continue-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.continue-button:hover::before {
  left: 100%;
}

.continue-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(1, 96, 100, 0.4);
  background: linear-gradient(135deg, #014d50 0%, #3a8a8d 100%);
}

.continue-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(1, 96, 100, 0.3);
}

.button-text {
  font-weight: 600;
  letter-spacing: 0.025em;
}

.button-icon {
  font-size: 1.25rem;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.continue-button:hover .button-icon {
  transform: translateX(4px);
}

/* Progress Indicator Styles */
.progress-container {
  width: 80%;
  margin: 2rem auto;
  display: flex;
  justify-content: center;
}

.progress-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 500px;
  text-align: center;
  border: 2px solid #016064;
}

.progress-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.progress-icon {
  font-size: 2rem;
  animation: bounce 2s infinite;
}

.progress-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #016064;
  margin: 0;
}

.progress-bar-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.progress-bar {
  flex: 1;
  height: 12px;
  background: #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #016064, #48AAAD);
  border-radius: 6px;
  transition: width 0.3s ease;
  position: relative;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 2s infinite;
}

.progress-text {
  font-weight: 600;
  color: #016064;
  min-width: 50px;
  font-size: 1.1rem;
}

.progress-stage {
  color: #6b7280;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

.progress-spinner {
  display: flex;
  justify-content: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #016064;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* Auth Section Styles */
.auth-container {
  position: absolute;
  top: 2.5rem;
  right: 1.5rem;
  z-index: 10;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 2px solid #48AAAD;
}

.user-name {
  color: #016064;
  font-weight: 600;
  font-size: 0.95rem;
}

.logout-button {
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
  background: linear-gradient(135deg, #b91c1c 0%, #dc2626 100%);
}

/* Login Button Styles */
.login-button-container {
  position: absolute;
  top: 2.5rem;
  right: 1.5rem;
  z-index: 10;
}

.login-button-main {
  background: linear-gradient(135deg, #48AAAD 0%, #016064 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(1, 96, 100, 0.3);
  text-decoration: none;
  display: inline-block;
}

.login-button-main:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(1, 96, 100, 0.4);
  background: linear-gradient(135deg, #3a8a8d 0%, #014d50 100%);
}

.login-button-main:active {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(1, 96, 100, 0.3);
}
</style>