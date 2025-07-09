<script setup>
import { ref } from 'vue'

const selectedFile = ref(null)
const fileInput = ref(null)
const isSubmitting = ref(false)
const uploadResult = ref(null)
const uploadError = ref(null)
const resumeData = ref(null)

const triggerFileSelect = () => {
  fileInput.value?.click()
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file && file.type === 'application/pdf') {
    selectedFile.value = file
    uploadError.value = null
  } else {
    selectedFile.value = null
    uploadError.value = 'Please select a valid PDF file.'
  }
}

const handleSubmit = async () => {
  if (!selectedFile.value) return

  isSubmitting.value = true
  uploadError.value = null
  uploadResult.value = null

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    console.log("📤 Uploading...")

    const response = await fetch('http://127.0.0.1:8000/upload-resume/', {
      method: 'POST',
      body: formData,
    })

    console.log("📥 Got response:", response)

    const result = await response.json()
    console.log("✅ Parsed JSON:", result)

    if (response.ok) {
        resumeData.value = result
        console.log("✅ Resume data set:", resumeData.value)
    } else {
        uploadError.value = "Upload failed with status " + response.status
        console.log("❌ Upload error set")
    }

    uploadResult.value = result
    } catch (err) {
        console.error("❌ Upload error:", err)
        uploadError.value = err.message
    } finally {
        console.log("🔚 Finally block reached")
        isSubmitting.value = false
  }
}

</script>

<template>
    <form @submit.prevent="handleSubmit" class="p-4 border rounded-lg max-w-md mx-auto mt-10">
      <!-- File upload button -->
      <button 
        type="button" 
        @click="triggerFileSelect"
        class="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Choose Resume (PDF)
      </button>
  
      <!-- Hidden file input -->
      <input 
        type="file" 
        ref="fileInput" 
        accept=".pdf" 
        @change="handleFileChange" 
        class="hidden"
      />
  
      <!-- Show selected file name -->
      <p v-if="selectedFile" class="mt-2 text-sm text-gray-700">
        Selected file: {{ selectedFile.name }}
      </p>
  
      <!-- Submit button -->
      <button 
        type="submit" 
        class="mt-4 bg-green-600 text-white px-4 py-2 rounded"
        :disabled="!selectedFile || isSubmitting"
      >
        {{ isSubmitting ? 'Uploading...' : 'Upload Resume' }}
      </button>
  
      <!-- Display result -->
      <div v-if="uploadResult" class="mt-4 text-green-700 text-sm">
        ✅ Resume uploaded successfully!
      </div>
  
      <div v-if="uploadError" class="mt-4 text-red-600 text-sm">
        ❌ {{ uploadError }}
      </div>
    </form>
    <div v-if="resumeData" class="mt-6 p-4 bg-gray-100 rounded">
  <h2 class="text-lg font-semibold">Parsed Resume Info:</h2>
  <p><strong>Name:</strong> {{ resumeData.analysis.name || 'N/A' }}</p>
  <p><strong>Email:</strong> {{ resumeData.analysis.email || 'N/A' }}</p>
  <p><strong>Phone:</strong> {{ resumeData.analysis.phone || 'N/A' }}</p>
  <p>
    <strong>Skills:</strong>
    <span v-if="resumeData.analysis.skills && resumeData.analysis.skills.length">
      {{ resumeData.analysis.skills.join(', ') }}
    </span>
    <span v-else>N/A</span>
  </p>
</div>
  </template>
  
