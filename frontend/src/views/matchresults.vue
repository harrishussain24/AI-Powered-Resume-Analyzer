<script setup>
defineOptions({
  name: 'MatchResultsView'
})
import { ref, onMounted } from 'vue'
import { useResumeStore } from '../stores/parseddatastore'
import axios from 'axios'
import '../assets/matchresults.css'

const store = useResumeStore()
const resume = store.resumeData
const jobDesc = store.jobDescriptionData

const matchResult = ref(null)
const error = ref(null)
const isLoading = ref(true)
const matchProgress = ref(0)
const matchStage = ref('')
const showProgress = ref(false)

onMounted(async () => {
  if (!resume?.analysis || !jobDesc) {
    error.value = 'Missing resume or job description data.'
    console.warn('❌ resume or job description is missing')
    isLoading.value = false
    return
  }

  console.log('📄 Resume data being sent:', resume.analysis)
  console.log('📝 Job description being sent:', jobDesc)

  showProgress.value = true
  matchProgress.value = 0
  matchStage.value = 'Preparing analysis...'

  try {
    // Simulate matching progress
    const progressInterval = setInterval(() => {
      if (matchProgress.value < 90) {
        matchProgress.value += Math.random() * 20
        if (matchProgress.value < 30) {
          matchStage.value = 'Comparing skills...'
        } else if (matchProgress.value < 60) {
          matchStage.value = 'Analyzing experience...'
        } else if (matchProgress.value < 90) {
          matchStage.value = 'Calculating match score...'
        }
      }
    }, 150)

    // Prepare the data properly
    const requestData = {
      resume: resume.analysis,
      job: jobDesc.analysis || jobDesc
    }

    console.log('🔍 Sending match request:', requestData)

    // First try the test endpoint to see if backend is working
    try {
      const testResponse = await axios.get('https://ai-powered-resume-analyzer-u0hx.onrender.com/test-match', {
        timeout: 10000
      })
      console.log('✅ Backend test successful:', testResponse.data)
    } catch (testErr) {
      console.warn('⚠️ Backend test failed:', testErr.message)
    }

    // Retry mechanism for the match request
    let response
    let retryCount = 0
    const maxRetries = 2
    
    while (retryCount <= maxRetries) {
      try {
        response = await axios.post('https://ai-powered-resume-analyzer-u0hx.onrender.com/match', requestData, {
          timeout: 30000 // 30 second timeout
        })
        break // Success, exit retry loop
      } catch (retryErr) {
        retryCount++
        console.warn(`⚠️ Attempt ${retryCount} failed:`, retryErr.message)
        
        if (retryCount > maxRetries) {
          throw retryErr // Re-throw the last error
        }
        
        // Wait before retrying (exponential backoff)
        await new Promise(resolve => setTimeout(resolve, 1000 * retryCount))
      }
    }

    clearInterval(progressInterval)
    matchProgress.value = 100
    matchStage.value = 'Analysis complete!'

    // Small delay to show completion
    setTimeout(() => {
      showProgress.value = false
    }, 1000)

    if (response.data.match) {
      matchResult.value = response.data.match
      console.log('✅ Match result received:', response.data.match)
    } else {
      error.value = response.data.detail || 'Matching failed.'
      console.error('❌ API error:', response.data)
    }
  } catch (err) {
    console.error('❌ Network error:', err)
    if (err.code === 'ECONNABORTED') {
      error.value = 'Request timed out. Please try again.'
    } else if (err.response?.status === 500) {
      error.value = 'Server error. Please try again later.'
    } else if (err.response?.status === 422) {
      error.value = 'Invalid data format. Please check your resume and job description.'
    } else {
      error.value = err.response?.data?.detail || err.message || 'Network error occurred.'
    }
    showProgress.value = false
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <!-- Main Content -->
  <div>
    <!-- Heading Section -->
    <div class="heading-section">
      <h2>Match Results</h2>
    </div>

    <!-- Progress Indicator -->
    <div v-if="showProgress" class="progress-container">
      <div class="progress-card">
        <div class="progress-header">
          <div class="progress-icon">🏯</div>
          <h3 class="progress-title">Matching Resume to Job</h3>
        </div>
        <div class="progress-bar-container">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: matchProgress + '%' }"></div>
          </div>
          <div class="progress-text">{{ Math.round(matchProgress) }}%</div>
        </div>
        <div class="progress-stage">{{ matchStage }}</div>
        <div class="progress-spinner">
          <div class="spinner"></div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="!matchResult && !error && !showProgress" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">Analyzing your resume against the job description...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">❌</div>
      <h3 class="error-title">Analysis Failed</h3>
      <p class="error-message">{{ error }}</p>
    </div>

    <!-- Results Container -->
    <div v-else-if="matchResult" class="results-container">
      <div class="results-header">
        <h2 class="results-title">🏯 Analysis Results</h2>
        <p class="results-subtitle">Your resume match analysis is complete</p>
      </div>
      <div class="results-divider"></div>
      <div class="results-content">
        <!-- Overall Score Section -->
        <div class="score-section">
          <div class="overall-score">
            <div class="score-header">
              <h3 class="score-title">🏆 Overall Match Score</h3>
              <div class="score-circle">
                <span class="score-value">{{ Math.round(matchResult.overall_score * 100) }}%</span>
              </div>
            </div>
            <div class="score-bar">
              <div class="score-fill" :style="{ width: matchResult.overall_score * 100 + '%' }"></div>
            </div>
          </div>
        </div>
        <!-- Detailed Scores Section -->
        <div class="scores-grid">
          <!-- Skill Match Score -->
          <div class="score-card">
            <div class="score-card-header">
              <span class="score-icon">💡</span>
              <h4 class="score-card-title">Skill Match</h4>
            </div>
            <div class="score-card-value">{{ Math.round(matchResult.skill_match_score * 100) }}%</div>
            <div class="score-card-bar">
              <div class="score-card-fill" :style="{ width: matchResult.skill_match_score * 100 + '%' }"></div>
            </div>
          </div>
          <!-- Experience Match Score -->
          <div class="score-card">
            <div class="score-card-header">
              <span class="score-icon">📈</span>
              <h4 class="score-card-title">Experience Match</h4>
            </div>
            <div class="score-card-value">{{ Math.round(matchResult.experience_match_score * 100) }}%</div>
            <div class="score-card-bar">
              <div class="score-card-fill" :style="{ width: matchResult.experience_match_score * 100 + '%' }"></div>
            </div>
          </div>
        </div>
        <!-- Matched Skills Section -->
        <div class="skills-section">
          <h3 class="section-title">✅ Matched Skills</h3>
          <div class="matched-skills-container">
            <template v-if="matchResult.matched_skills && matchResult.matched_skills.length">
              <span 
                class="matched-skill-tag" 
                v-for="skill in matchResult.matched_skills" 
                :key="skill"
              >
                {{ skill }}
              </span>
            </template>
            <span v-else class="no-skills-message">No matching skills found</span>
          </div>
        </div>
        <!-- Missing Requirements Section -->
        <div class="skills-section">
          <h3 class="section-title">❌ Missing Requirements</h3>
          <!-- Missing Skills -->
          <div v-if="matchResult.missing_skills && matchResult.missing_skills.length" class="missing-skills-container">
            <h4 class="missing-subtitle">Missing Skills:</h4>
            <template v-for="skill in matchResult.missing_skills" :key="skill">
              <span class="missing-skill-tag">{{ skill }}</span>
            </template>
          </div>
          <!-- Missing Experience -->
          <div v-if="matchResult.missing_experience && matchResult.missing_experience.length" class="missing-experience-container">
            <h4 class="missing-subtitle">Missing Experience:</h4>
            <template v-for="exp in matchResult.missing_experience" :key="exp">
              <span class="missing-experience-tag">{{ exp }}</span>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
