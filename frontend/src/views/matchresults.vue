<script setup>
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
  <div class="matchresults-root">
    <!-- Heading Section -->
    <div class="matchresults-header">
      <h2 class="matchresults-title">Match Results</h2>
      <div class="matchresults-header-divider"></div>
    </div>

    <!-- Progress Indicator -->
    <div v-if="showProgress" class="matchresults-progress-wrap">
      <div class="matchresults-progress-card">
        <div class="matchresults-progress-header">
          <div class="matchresults-progress-icon">🏯</div>
          <h3 class="matchresults-progress-title">Matching Resume to Job</h3>
        </div>
        <div class="matchresults-progress-bar-wrap">
          <div class="matchresults-progress-bar-bg">
            <div class="matchresults-progress-bar" :style="{ width: matchProgress + '%' }"></div>
          </div>
          <div class="matchresults-progress-percent">{{ Math.round(matchProgress) }}%</div>
        </div>
        <div class="matchresults-progress-stage">{{ matchStage }}</div>
        <div class="matchresults-progress-spinner-wrap">
          <div class="matchresults-progress-spinner"></div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="!matchResult && !error && !showProgress" class="matchresults-loading">
      <div class="matchresults-loading-spinner"></div>
      <p class="matchresults-loading-text">Analyzing your resume against the job description...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="matchresults-error-wrap">
      <div class="matchresults-error-icon">❌</div>
      <h3 class="matchresults-error-title">Analysis Failed</h3>
      <p class="matchresults-error-text">{{ error }}</p>
    </div>

    <!-- Results Container -->
    <div v-else-if="matchResult" class="matchresults-results-wrap">
      <div class="matchresults-results-header">
        <h2 class="matchresults-results-title">🏯 Analysis Results</h2>
        <p class="matchresults-results-desc">Your resume match analysis is complete</p>
      </div>
      <div class="matchresults-results-divider"></div>
      <div class="matchresults-results-body">
        <!-- Overall Score Section -->
        <div class="matchresults-score-wrap">
          <div class="matchresults-score-header">
            <h3 class="matchresults-score-title">🏆 Overall Match Score</h3>
            <div class="matchresults-score-circle">
              <span>{{ Math.round(matchResult.overall_score * 100) }}%</span>
            </div>
          </div>
          <div class="matchresults-score-bar-bg">
            <div class="matchresults-score-bar" :style="{ width: matchResult.overall_score * 100 + '%' }"></div>
          </div>
        </div>
        <!-- Detailed Scores Section -->
        <div class="matchresults-details-grid">
          <!-- Skill Match Score -->
          <div class="matchresults-detail-card">
            <div class="matchresults-detail-header">
              <span class="matchresults-detail-icon">💡</span>
              <h4 class="matchresults-detail-title">Skill Match</h4>
            </div>
            <div class="matchresults-detail-score">{{ Math.round(matchResult.skill_match_score * 100) }}%</div>
            <div class="matchresults-detail-bar-bg">
              <div class="matchresults-detail-bar" :style="{ width: matchResult.skill_match_score * 100 + '%' }"></div>
            </div>
          </div>
          <!-- Experience Match Score -->
          <div class="matchresults-detail-card">
            <div class="matchresults-detail-header">
              <span class="matchresults-detail-icon">📈</span>
              <h4 class="matchresults-detail-title">Experience Match</h4>
            </div>
            <div class="matchresults-detail-score">{{ Math.round(matchResult.experience_match_score * 100) }}%</div>
            <div class="matchresults-detail-bar-bg">
              <div class="matchresults-detail-bar" :style="{ width: matchResult.experience_match_score * 100 + '%' }"></div>
            </div>
          </div>
        </div>
        <!-- Matched Skills Section -->
        <div class="matchresults-matched-skills">
          <h3 class="matchresults-section-title">✅ Matched Skills</h3>
          <div class="matchresults-skills-list">
            <span v-if="matchResult.matched_skills && matchResult.matched_skills.length" 
                  class="matchresults-skill" 
                  v-for="skill in matchResult.matched_skills" 
                  :key="skill">
              {{ skill }}
            </span>
            <span v-else class="matchresults-skill-empty">No matching skills found</span>
          </div>
        </div>
        <!-- Missing Requirements Section -->
        <div class="matchresults-missing-reqs">
          <h3 class="matchresults-section-title">❌ Missing Requirements</h3>
          <!-- Missing Skills -->
          <div v-if="matchResult.missing_skills && matchResult.missing_skills.length" class="matchresults-missing-skills">
            <h4 class="matchresults-missing-title">Missing Skills:</h4>
            <div class="matchresults-missing-list">
              <span class="matchresults-missing-item" 
                    v-for="skill in matchResult.missing_skills" 
                    :key="skill">
                {{ skill }}
              </span>
            </div>
          </div>
          <!-- Missing Experience -->
          <div v-if="matchResult.missing_experience && matchResult.missing_experience.length" class="matchresults-missing-experience">
            <h4 class="matchresults-missing-title">Missing Experience:</h4>
            <div class="matchresults-missing-list">
              <span class="matchresults-missing-item" 
                    v-for="exp in matchResult.missing_experience" 
                    :key="exp">
                {{ exp }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
