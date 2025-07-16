<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useResumeStore } from '../stores/parseddatastore'
import axios from 'axios'
// import '../assets/uploadresume.css'  // Remove custom CSS import

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
    <!-- Header Bar: Heading and Auth Button -->
    <div class="flex items-start justify-between bg-[#016064] px-10 py-6 mb-8 rounded-xl">
      <h2 class="text-white text-3xl font-bold tracking-tight m-0 p-0">Upload Your Resume</h2>
      <div class="flex items-start">
        <div v-if="user" class="flex items-center gap-3 bg-white px-4 py-2 rounded-lg shadow border-2 border-[#48AAAD] mt-1 mr-1">
          <span class="text-[#016064] font-semibold text-base">Welcome, {{ user.name || user.email }}</span>
          <button @click="logout" class="bg-gradient-to-r from-red-600 to-red-400 text-white px-3 py-1.5 rounded-md text-sm font-semibold transition hover:from-red-700 hover:to-red-500 shadow">
            Logout
          </button>
        </div>
        <div v-else class="flex items-center mt-1 mr-1">
          <button
            @click="router.push('/login')"
            class="bg-gradient-to-r from-[#48AAAD] to-[#016064] text-white px-8 py-3 min-w-[170px] rounded-lg text-lg font-semibold shadow transition hover:from-[#3a8a8d] hover:to-[#014d50]"
          >
            Login / Signup
          </button>
        </div>
      </div>
    </div>

    <div class="h-px bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 ml-8 mr-8 mb-8"></div>

    <div class="flex flex-col items-center justify-center bg-white border-2 border-[#48AAAD] rounded-2xl shadow-md py-12 px-8 mb-8 w-4/5 mx-auto cursor-pointer transition hover:border-[#016064] hover:shadow-lg" @click="triggerFileSelect">
      <span class="text-5xl text-[#a084e8] mb-4">📄</span>
      <div class="text-[#6c6f93] text-lg mb-2">Click here to upload your file or drag.</div>
      <span class="text-[#48AAAD] font-semibold cursor-pointer transition hover:text-[#016064]">Supported Format: <u>PDF (5mb max)</u></span>
    </div>

    <input type="file" accept=".pdf" ref="fileInput" @change="handleFileChange" class="hidden" />

    <!-- Progress Indicator -->
    <div v-if="showProgress" class="flex justify-center w-4/5 mx-auto my-8">
      <div class="bg-white rounded-xl shadow-lg p-8 w-full max-w-xl text-center border-2 border-[#016064]">
        <div class="flex items-center justify-center gap-4 mb-6">
          <div class="text-3xl animate-bounce">📄</div>
          <h3 class="text-xl font-semibold text-[#016064] m-0">Processing Resume</h3>
        </div>
        <div class="flex items-center gap-4 mb-4">
          <div class="flex-1 h-3 bg-gray-200 rounded-full overflow-hidden relative">
            <div class="h-full bg-gradient-to-r from-[#016064] to-[#48AAAD] rounded-full transition-all duration-300" :style="{ width: uploadProgress + '%' }"></div>
          </div>
          <div class="font-semibold text-[#016064] min-w-[50px] text-lg">{{ Math.round(uploadProgress) }}%</div>
        </div>
        <div class="text-gray-500 text-base font-medium mb-6">{{ uploadStage }}</div>
        <div class="flex justify-center">
          <div class="w-10 h-10 border-4 border-gray-200 border-t-[#016064] rounded-full animate-spin"></div>
        </div>
      </div>
    </div>

    <!-- Attached Files Section -->
    <div class="w-4/5 mx-auto my-8 bg-white rounded-lg shadow overflow-hidden">
      <div class="px-8 pt-6 pb-2">
        <h2 class="text-xl font-semibold text-[#016064] mb-1">Attached File</h2>
        <p class="text-base text-[#48AAAD] m-0">Here you can see your uploaded file</p>
      </div>
      <div class="h-px bg-[#48AAAD] m-0"></div>
      <div class="grid grid-cols-4 gap-4 px-8 py-4 bg-gray-50 font-semibold text-gray-700 text-sm">
        <div>File Name</div>
        <div>Size</div>
        <div>Uploaded At</div>
        <div>Action</div>
      </div>
      <div class="h-px bg-[#48AAAD] m-0"></div>
      <div class="px-8 py-4">
        <div v-for="(file, index) in uploadedFiles" :key="index" class="grid grid-cols-4 gap-4 items-center py-2 border-b last:border-b-0">
          <div>{{ file.name }}</div>
          <div>{{ file.size }}</div>
          <div>{{ file.uploadedAt }}</div>
          <div>
            <button class="bg-red-100 text-red-600 px-4 py-1 rounded-md font-semibold hover:bg-red-200 transition" @click="deleteFile(index)">Delete</button>
          </div>
        </div>
        <div v-if="!uploadedFiles.length" class="text-gray-400 text-center py-4">No files uploaded yet.</div>
      </div>
    </div>

    <!-- Resume Data Section -->
    <div v-if="resumeData" class="w-4/5 mx-auto my-8 bg-white rounded-lg shadow">
      <div class="px-8 pt-6 pb-2">
        <h2 class="text-xl font-semibold text-[#016064] mb-1">Resume Information</h2>
        <p class="text-base text-[#48AAAD] m-0">Parsed data from your uploaded resume</p>
      </div>
      <div class="h-px bg-[#48AAAD] m-0"></div>
      <div class="px-8 py-6">
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-[#016064] mb-2">Personal Information</h3>
          <div class="grid grid-cols-3 gap-6">
            <div>
              <span class="font-semibold text-gray-700">Name:</span>
              <span class="ml-2 text-gray-800">{{ resumeData.analysis.name || 'N/A' }}</span>
            </div>
            <div>
              <span class="font-semibold text-gray-700">Email:</span>
              <span class="ml-2 text-gray-800">{{ resumeData.analysis.email || 'N/A' }}</span>
            </div>
            <div>
              <span class="font-semibold text-gray-700">Phone:</span>
              <span class="ml-2 text-gray-800">{{ resumeData.analysis.phone || 'N/A' }}</span>
            </div>
          </div>
        </div>
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-[#016064] mb-2">Skills</h3>
          <div class="flex flex-wrap gap-2">
            <span v-if="resumeData.analysis.skills?.length" class="bg-[#48AAAD] text-white px-3 py-1 rounded-full text-sm font-medium" v-for="skill in resumeData.analysis.skills" :key="skill">
              {{ skill }}
            </span>
            <span v-else class="text-gray-400">No skills found</span>
          </div>
        </div>
        <div v-if="resumeData.analysis.experience?.length" class="mb-6">
          <h3 class="text-lg font-semibold text-[#016064] mb-2">Work Experience</h3>
          <div class="space-y-4">
            <div v-for="(exp, index) in resumeData.analysis.experience" :key="index" class="bg-gray-50 rounded-lg p-4 shadow-sm">
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-bold text-base text-[#016064]">{{ exp.title }}</h4>
                <span class="text-[#48AAAD] font-semibold">{{ exp.company }}</span>
              </div>
              <div class="flex items-center gap-6 mb-2">
                <span class="text-gray-500">{{ exp.location }}</span>
                <span class="text-gray-400">{{ exp.dates }}</span>
              </div>
              <ul class="list-disc list-inside ml-4 text-gray-700">
                <li v-for="(bullet, i) in exp.bullets" :key="i">{{ bullet }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="resumeData" class="flex justify-center w-4/5 mx-auto my-8">
      <button @click="goToJobDescriptionView" class="bg-gradient-to-r from-[#016064] to-[#48AAAD] text-white rounded-full px-8 py-3 text-lg font-semibold shadow transition hover:from-[#014d50] hover:to-[#3a8a8d] flex items-center gap-3 relative overflow-hidden">
        <span class="font-semibold tracking-wide">Continue to Job Description</span>
        <span class="text-xl font-bold transition-transform">→</span>
      </button>
    </div>

    <div v-if="uploadError" class="mt-4 text-red-600 text-sm">
      ❌ {{ uploadError }}
    </div>
  </div>
</template>

