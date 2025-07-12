<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useResumeStore } from '../stores/parseddatastore'
import axios from 'axios'

const store = useResumeStore()
const router = useRouter()

const jobDescription = ref('')
const isSubmitting = ref(false)
const error = ref(null)

const analyzeJobDescription = async () => {
  if (!jobDescription.value.trim()) return

  isSubmitting.value = true
  error.value = null

  try {
    const response = await axios.post('http://127.0.0.1:8000/analyze-job', {
      description: jobDescription.value
    })

    store.setJobDescription(response.data)
    // Don't navigate to next page, just store the result
  } catch (err) {
    error.value = err.response?.data?.message || err.message
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
  <div class="max-w-5xl mx-auto mt-24 p-6 bg-white rounded-lg shadow">
    <!-- Heading Section -->
    <div class="heading-section">
      <h2 class="text-3xl font-bold text-gray-800 mb-4 ml-8">Upload Job Description</h2>
      <div class="h-px bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 ml-8 mr-8"></div>
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
        
        <div v-if="error" class="error-message">
          ❌ {{ error }}
        </div>
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


<style scoped>
/* Heading Section */
.heading-section {
  background-color: #016064;
  color: white;
  padding: 1rem 1.5rem;
  width: 100vw;
  margin-bottom: 2rem;
}

/* Job Description Input Section */
.job-description-container {
  width: 80%;
  margin: 2rem auto;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.job-description-header {
  padding: 1.5rem 2rem 1rem 2rem;
}

.job-description-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #016064;
  margin: 0 0 0.5rem 0;
}

.job-description-subtitle {
  font-size: 1rem;
  color: #48AAAD;
  margin: 0;
}

.job-description-divider {
  height: 1px;
  background: #48AAAD;
  margin: 0;
}

.job-description-content {
  padding: 2rem;
}

.job-description-textarea {
  width: 100%;
  min-height: 300px;
  padding: 1.5rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 1rem;
  line-height: 1.6;
  color: #374151;
  background: #f9fafb;
  transition: border-color 0.2s, box-shadow 0.2s;
  resize: vertical;
  font-family: inherit;
}

.job-description-textarea:focus {
  outline: none;
  border-color: #48AAAD;
  box-shadow: 0 0 0 3px rgba(72, 170, 173, 0.1);
  background: white;
}

.job-description-textarea::placeholder {
  color: #9ca3af;
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.analyze-button {
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

.analyze-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.analyze-button:hover::before {
  left: 100%;
}

.analyze-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(1, 96, 100, 0.4);
  background: linear-gradient(135deg, #014d50 0%, #3a8a8d 100%);
}

.analyze-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(1, 96, 100, 0.3);
}

.analyze-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.button-text {
  font-weight: 600;
  letter-spacing: 0.025em;
}

.button-icon {
  font-size: 1.25rem;
  transition: transform 0.3s ease;
}

.analyze-button:hover .button-icon {
  transform: scale(1.1);
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 0.5rem;
  color: #dc2626;
  text-align: center;
  font-weight: 500;
}

/* Job Data Section */
.job-data-container {
  width: 80%;
  margin: 2rem auto;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.job-data-header {
  padding: 1.5rem 2rem 1rem 2rem;
}

.job-data-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #016064;
  margin: 0 0 0.5rem 0;
}

.job-data-subtitle {
  font-size: 1rem;
  color: #48AAAD;
  margin: 0;
}

.job-data-divider {
  height: 1px;
  background: #48AAAD;
  margin: 0;
}

.job-data-content {
  padding: 2rem;
}

.job-section {
  margin-bottom: 2rem;
}

.job-section:last-child {
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

.education-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.education-tag {
  background: #48AAAD;
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

.continue-button .button-text {
  font-weight: 600;
  letter-spacing: 0.025em;
}

.continue-button .button-icon {
  font-size: 1.25rem;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.continue-button:hover .button-icon {
  transform: translateX(4px);
}
</style>
