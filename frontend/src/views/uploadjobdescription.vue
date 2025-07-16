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
  <div class="max-w-5xl mx-auto mt-24 p-6 bg-white rounded-lg shadow">
    <!-- Heading Section -->
    <div class="bg-[#016064] rounded-xl px-10 py-6 mb-8">
      <h2 class="text-3xl font-bold text-white m-0 p-0">Upload Job Description</h2>
      <div class="h-px bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 mt-4"></div>
    </div>

    <!-- Progress Indicator -->
    <div v-if="showProgress" class="flex justify-center w-4/5 mx-auto my-8">
      <div class="bg-white rounded-xl shadow-lg p-8 w-full max-w-xl text-center border-2 border-[#016064]">
        <div class="flex items-center justify-center gap-4 mb-6">
          <div class="text-3xl animate-bounce">🔍</div>
          <h3 class="text-xl font-semibold text-[#016064] m-0">Analyzing Job Description</h3>
        </div>
        <div class="flex items-center gap-4 mb-4">
          <div class="flex-1 h-3 bg-gray-200 rounded-full overflow-hidden relative">
            <div class="h-full bg-gradient-to-r from-[#016064] to-[#48AAAD] rounded-full transition-all duration-300" :style="{ width: analysisProgress + '%' }"></div>
          </div>
          <div class="font-semibold text-[#016064] min-w-[50px] text-lg">{{ Math.round(analysisProgress) }}%</div>
        </div>
        <div class="text-gray-500 text-base font-medium mb-6">{{ analysisStage }}</div>
        <div class="flex justify-center">
          <div class="w-10 h-10 border-4 border-gray-200 border-t-[#016064] rounded-full animate-spin"></div>
        </div>
      </div>
    </div>

    <!-- Job Description Input Section -->
    <div class="w-4/5 mx-auto my-8 bg-white rounded-lg shadow">
      <div class="px-8 pt-6 pb-2">
        <h2 class="text-xl font-semibold text-[#016064] mb-1">Job Description</h2>
        <p class="text-base text-[#48AAAD] m-0">Paste the job description here</p>
      </div>
      <div class="h-px bg-[#48AAAD] m-0"></div>
      <div class="px-8 py-6">
        <textarea 
          v-model="jobDescription" 
          rows="12" 
          class="w-full bg-white border-2 border-[#48AAAD] rounded-xl p-4 text-[#016064] text-base focus:outline-none focus:border-[#016064] focus:bg-[#f4f8f8] transition mb-4 resize-none shadow"
          placeholder="Paste the job description here..."
        ></textarea>
        <div class="flex justify-end mb-2">
          <button 
            @click="analyzeJobDescription" 
            :disabled="isSubmitting" 
            class="bg-gradient-to-r from-[#016064] to-[#48AAAD] text-white rounded-full px-8 py-3 text-lg font-semibold shadow transition hover:from-[#014d50] hover:to-[#3a8a8d] flex items-center gap-3 relative overflow-hidden disabled:opacity-60 disabled:cursor-not-allowed"
          >
            <span class="font-semibold tracking-wide">{{ isSubmitting ? 'Analyzing...' : 'Analyze Job Description' }}</span>
            <span class="text-xl font-bold transition-transform">🔍</span>
          </button>
        </div>
        <div v-if="error" class="text-red-600 text-sm mt-2">❌ {{ error }}</div>
      </div>
    </div>

    <!-- Parsed Job Description Section -->
    <div v-if="store.jobDescriptionData" class="w-4/5 mx-auto my-8 bg-white rounded-lg shadow">
      <div class="px-8 pt-6 pb-2">
        <h2 class="text-xl font-semibold text-[#016064] mb-1">Job Description Information</h2>
        <p class="text-base text-[#48AAAD] m-0">Parsed data from your job description</p>
      </div>
      <div class="h-px bg-[#48AAAD] m-0"></div>
      <div class="px-8 py-6">
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-[#016064] mb-2">Job Details</h3>
          <div class="grid grid-cols-2 gap-6">
            <div>
              <span class="font-semibold text-gray-700">Job Title:</span>
              <span class="ml-2 text-gray-800">{{ store.jobDescriptionData.analysis?.title || store.jobDescriptionData.title || 'N/A' }}</span>
            </div>
            <div>
              <span class="font-semibold text-gray-700">Experience Required:</span>
              <span class="ml-2 text-gray-800">{{ store.jobDescriptionData.analysis?.experience || store.jobDescriptionData.experience || 'N/A' }}</span>
            </div>
          </div>
        </div>
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-[#016064] mb-2">Required Skills</h3>
          <div class="flex flex-wrap gap-2">
            <span v-if="(store.jobDescriptionData.analysis?.skills && store.jobDescriptionData.analysis.skills.length) || (store.jobDescriptionData.skills && store.jobDescriptionData.skills.length)" 
                  class="bg-[#48AAAD] text-white px-3 py-1 rounded-full text-sm font-medium" 
                  v-for="skill in (store.jobDescriptionData.analysis?.skills || store.jobDescriptionData.skills || [])" 
                  :key="skill">
              {{ skill }}
            </span>
            <span v-else class="text-gray-400">No skills found</span>
          </div>
        </div>
        <div v-if="(store.jobDescriptionData.analysis?.education && store.jobDescriptionData.analysis.education.length) || (store.jobDescriptionData.education && store.jobDescriptionData.education.length)" class="mb-6">
          <h3 class="text-lg font-semibold text-[#016064] mb-2">Education Requirements</h3>
          <div class="flex flex-wrap gap-2">
            <span v-for="edu in (store.jobDescriptionData.analysis?.education || store.jobDescriptionData.education || [])" 
                  :key="edu" 
                  class="bg-[#48AAAD] text-white px-3 py-1 rounded-full text-sm font-medium">
              {{ edu }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Show Final Results Button -->
    <div v-if="store.jobDescriptionData" class="flex justify-center w-4/5 mx-auto my-8">
      <button @click="showFinalResults" class="bg-gradient-to-r from-[#016064] to-[#48AAAD] text-white rounded-full px-8 py-3 text-lg font-semibold shadow transition hover:from-[#014d50] hover:to-[#3a8a8d] flex items-center gap-3 relative overflow-hidden">
        <span class="font-semibold tracking-wide">Show Final Results</span>
        <span class="text-xl font-bold transition-transform">📊</span>
      </button>
    </div>
  </div>
</template>

