<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useResumeStore } from '../stores/resumeStore'

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
    const response = await fetch('http://127.0.0.1:8000/analyze-job', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: jobDescription.value })
    })

    const result = await response.json()

    if (response.ok) {
      store.setJobDescription(result)
      //router.push('/match-results')
    } else {
      error.value = 'API error: ' + response.status
    }
  } catch (err) {
    error.value = err.message
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto p-6">
    <h2 class="text-xl font-bold mb-4">Paste Job Description</h2>
    <textarea v-model="jobDescription" rows="10" class="w-full border p-3 rounded mb-4"></textarea>
    <button @click="analyzeJobDescription" :disabled="isSubmitting" class="bg-blue-600 text-white px-4 py-2 rounded">
      {{ isSubmitting ? 'Analyzing...' : 'Analyze Job Description' }}
    </button>
    <p v-if="error" class="text-red-500 mt-2">{{ error }}</p>
  </div>
  <div v-if="store.jobDescriptionData" class="mt-6 p-4 bg-gray-100 rounded">
  <h3 class="text-lg font-semibold mb-2">Parsed Job Description</h3>
  <p><strong>Title:</strong> {{ store.jobDescriptionData.title || 'N/A' }}</p>
  <p>
    <strong>Skills:</strong>
    <span v-if="store.jobDescriptionData.skills && store.jobDescriptionData.skills.length">
      {{ store.jobDescriptionData.skills.join(', ') }}
    </span>
    <span v-else>N/A</span>
  </p>
  <p>
    <strong>Experience:</strong>
    {{ store.jobDescriptionData.experience || 'N/A' }}
  </p>
  <p>
    <strong>Education:</strong>
    <span v-if="store.jobDescriptionData.education && store.jobDescriptionData.education.length">
      {{ store.jobDescriptionData.education.join(', ') }}
    </span>
    <span v-else>N/A</span>
  </p>
</div>
</template>
