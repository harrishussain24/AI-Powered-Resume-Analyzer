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
  <div class="max-w-5xl mx-auto mt-24 p-6 bg-white rounded-lg shadow">
    <!-- Heading Section -->
    <div class="bg-[#016064] rounded-xl px-10 py-6 mb-8">
      <h2 class="text-3xl font-bold text-white m-0 p-0">Match Results</h2>
      <div class="h-px bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 mt-4"></div>
    </div>

    <!-- Progress Indicator -->
    <div v-if="showProgress" class="flex justify-center w-4/5 mx-auto my-8">
      <div class="bg-white rounded-xl shadow-lg p-8 w-full max-w-xl text-center border-2 border-[#016064]">
        <div class="flex items-center justify-center gap-4 mb-6">
          <div class="text-3xl animate-bounce">🏯</div>
          <h3 class="text-xl font-semibold text-[#016064] m-0">Matching Resume to Job</h3>
        </div>
        <div class="flex items-center gap-4 mb-4">
          <div class="flex-1 h-3 bg-gray-200 rounded-full overflow-hidden relative">
            <div class="h-full bg-gradient-to-r from-[#016064] to-[#48AAAD] rounded-full transition-all duration-300" :style="{ width: matchProgress + '%' }"></div>
          </div>
          <div class="font-semibold text-[#016064] min-w-[50px] text-lg">{{ Math.round(matchProgress) }}%</div>
        </div>
        <div class="text-gray-500 text-base font-medium mb-6">{{ matchStage }}</div>
        <div class="flex justify-center">
          <div class="w-10 h-10 border-4 border-gray-200 border-t-[#016064] rounded-full animate-spin"></div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="!matchResult && !error && !showProgress" class="flex flex-col items-center justify-center py-12">
      <div class="w-10 h-10 border-4 border-gray-200 border-t-[#48AAAD] rounded-full animate-spin mb-4"></div>
      <p class="text-[#016064] text-lg font-semibold">Analyzing your resume against the job description...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex flex-col items-center justify-center py-12">
      <div class="text-4xl mb-2">❌</div>
      <h3 class="text-xl font-bold text-red-600 mb-2">Analysis Failed</h3>
      <p class="text-red-500 text-base">{{ error }}</p>
    </div>

    <!-- Results Container -->
    <div v-else-if="matchResult" class="w-4/5 mx-auto my-8 bg-white rounded-lg shadow">
      <div class="px-8 pt-6 pb-2">
        <h2 class="text-xl font-semibold text-[#016064] mb-1">🏯 Analysis Results</h2>
        <p class="text-base text-[#48AAAD] m-0">Your resume match analysis is complete</p>
      </div>
      <div class="h-px bg-[#48AAAD] m-0"></div>
      <div class="px-8 py-6">
        <!-- Overall Score Section -->
        <div class="mb-8">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-lg font-semibold text-[#016064]">🏆 Overall Match Score</h3>
            <div class="w-16 h-16 rounded-full bg-gradient-to-br from-[#48AAAD] to-[#016064] flex items-center justify-center text-2xl font-bold text-white shadow-inner">
              <span>{{ Math.round(matchResult.overall_score * 100) }}%</span>
            </div>
          </div>
          <div class="w-full h-4 bg-gray-200 rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r from-[#48AAAD] to-[#016064] rounded-full transition-all duration-300" :style="{ width: matchResult.overall_score * 100 + '%' }"></div>
          </div>
        </div>
        <!-- Detailed Scores Section -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <!-- Skill Match Score -->
          <div class="bg-gray-50 rounded-lg p-6 shadow-sm">
            <div class="flex items-center gap-2 mb-2">
              <span class="text-xl">💡</span>
              <h4 class="text-base font-semibold text-[#016064]">Skill Match</h4>
            </div>
            <div class="text-2xl font-bold text-[#48AAAD] mb-2">{{ Math.round(matchResult.skill_match_score * 100) }}%</div>
            <div class="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
              <div class="h-full bg-gradient-to-r from-[#48AAAD] to-[#016064] rounded-full transition-all duration-300" :style="{ width: matchResult.skill_match_score * 100 + '%' }"></div>
            </div>
          </div>
          <!-- Experience Match Score -->
          <div class="bg-gray-50 rounded-lg p-6 shadow-sm">
            <div class="flex items-center gap-2 mb-2">
              <span class="text-xl">📈</span>
              <h4 class="text-base font-semibold text-[#016064]">Experience Match</h4>
            </div>
            <div class="text-2xl font-bold text-[#48AAAD] mb-2">{{ Math.round(matchResult.experience_match_score * 100) }}%</div>
            <div class="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
              <div class="h-full bg-gradient-to-r from-[#48AAAD] to-[#016064] rounded-full transition-all duration-300" :style="{ width: matchResult.experience_match_score * 100 + '%' }"></div>
            </div>
          </div>
        </div>
        <!-- Matched Skills Section -->
        <div class="mb-8">
          <h3 class="text-lg font-semibold text-[#016064] mb-2">✅ Matched Skills</h3>
          <div class="flex flex-wrap gap-2">
            <span v-if="matchResult.matched_skills && matchResult.matched_skills.length" 
                  class="bg-[#48AAAD] text-white px-3 py-1 rounded-full text-sm font-medium" 
                  v-for="skill in matchResult.matched_skills" 
                  :key="skill">
              {{ skill }}
            </span>
            <span v-else class="text-gray-400">No matching skills found</span>
          </div>
        </div>
        <!-- Missing Requirements Section -->
        <div class="mb-8">
          <h3 class="text-lg font-semibold text-[#016064] mb-2">❌ Missing Requirements</h3>
          <!-- Missing Skills -->
          <div v-if="matchResult.missing_skills && matchResult.missing_skills.length" class="mb-4">
            <h4 class="text-base font-semibold text-[#48AAAD] mb-1">Missing Skills:</h4>
            <div class="flex flex-wrap gap-2">
              <span class="bg-red-100 text-red-600 px-3 py-1 rounded-full text-sm font-medium" 
                    v-for="skill in matchResult.missing_skills" 
                    :key="skill">
                {{ skill }}
              </span>
            </div>
          </div>
          <!-- Missing Experience -->
          <div v-if="matchResult.missing_experience && matchResult.missing_experience.length" class="mb-4">
            <h4 class="text-base font-semibold text-[#48AAAD] mb-1">Missing Experience:</h4>
            <div class="flex flex-wrap gap-2">
              <span class="bg-red-100 text-red-600 px-3 py-1 rounded-full text-sm font-medium" 
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
