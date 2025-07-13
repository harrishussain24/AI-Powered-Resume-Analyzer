<script setup>
import { ref, onMounted } from 'vue'
import { useResumeStore } from '../stores/parseddatastore'
import axios from 'axios'

const store = useResumeStore()
const resume = store.resumeData
const jobDesc = store.jobDescriptionData

const matchResult = ref(null)
const error = ref(null)

onMounted(async () => {
  if (!resume?.analysis || !jobDesc) {
    error.value = 'Missing resume or job description data.'
    console.warn('❌ resume or job description is missing')
    return
  }

  console.log('📄 Resume data being sent:', resume.analysis)
  console.log('📝 Job description being sent:', jobDesc)

  try {
    const response = await axios.post('https://ai-powered-resume-analyzer-u0hx.onrender.com/match', {
      resume: resume.analysis,
      job: jobDesc.analysis || jobDesc,
    })

    if (response.data.match) {
      matchResult.value = response.data.match
      console.log('✅ Match result received:', response.data.match)
    } else {
      error.value = response.data.detail || 'Matching failed.'
      console.error('❌ API error:', response.data)
    }
  } catch (err) {
    error.value = err.response?.data?.message || err.message
    console.error('❌ Network error:', err)
  }
})
</script>

<style scoped>
/* Heading Section */
.heading-section {
  background-color: #016064;
  color: white;
  padding: 1rem 1.5rem;
  width: 100vw;
  margin-bottom: 2rem;
}

/* Loading State */
.loading-container {
  width: 80%;
  margin: 4rem auto;
  text-align: center;
  padding: 3rem;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #016064;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 2rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: #6b7280;
  font-size: 1.125rem;
  font-weight: 500;
}

/* Error State */
.error-container {
  width: 80%;
  margin: 4rem auto;
  text-align: center;
  padding: 3rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 0.75rem;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #dc2626;
  margin-bottom: 1rem;
}

.error-message {
  color: #7f1d1d;
  font-size: 1rem;
}

/* Results Container */
.results-container {
  width: 80%;
  margin: 2rem auto;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.results-header {
  padding: 1.5rem 2rem 1rem 2rem;
}

.results-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #016064;
  margin: 0 0 0.5rem 0;
}

.results-subtitle {
  font-size: 1rem;
  color: #48AAAD;
  margin: 0;
}

.results-divider {
  height: 1px;
  background: #48AAAD;
  margin: 0;
}

.results-content {
  padding: 2rem;
}

/* Overall Score Section */
.score-section {
  margin-bottom: 2rem;
}

.overall-score {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 2rem;
  border-radius: 1rem;
  border: 2px solid #e2e8f0;
}

.score-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.score-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.score-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #016064 0%, #48AAAD 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(1, 96, 100, 0.3);
}

.score-value {
  color: white;
  font-size: 1.25rem;
  font-weight: 700;
}

.score-bar {
  height: 12px;
  background: #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  background: linear-gradient(90deg, #016064 0%, #48AAAD 100%);
  border-radius: 6px;
  transition: width 1s ease-in-out;
}

/* Scores Grid */
.scores-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.score-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.score-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.score-card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.score-icon {
  font-size: 1.5rem;
}

.score-card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.score-card-value {
  font-size: 2rem;
  font-weight: 700;
  color: #016064;
  margin-bottom: 1rem;
  text-align: center;
}

.score-card-bar {
  height: 8px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
}

.score-card-fill {
  height: 100%;
  background: linear-gradient(90deg, #48AAAD 0%, #016064 100%);
  border-radius: 4px;
  transition: width 1s ease-in-out;
}

/* Skills Section */
.skills-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e5e7eb;
}

.matched-skills-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.matched-skill-tag {
  background: linear-gradient(135deg, #016064 0%, #48AAAD 100%);
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 500;
  display: inline-block;
  box-shadow: 0 2px 8px rgba(1, 96, 100, 0.2);
  transition: transform 0.2s;
}

.matched-skill-tag:hover {
  transform: translateY(-1px);
}

/* Missing Skills */
.missing-skills-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.missing-skill-tag {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 500;
  display: inline-block;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
  transition: transform 0.2s;
  border: 1px solid #fecaca;
}

.missing-skill-tag:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

/* Missing Requirements Subsection */
.missing-subsection {
  margin-bottom: 1.5rem;
}

.missing-subsection:last-child {
  margin-bottom: 0;
}

.missing-subtitle {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 0.75rem 0;
}

/* Missing Experience */
.missing-experience-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.missing-experience-tag {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 500;
  display: inline-block;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);
  transition: transform 0.2s;
  border: 1px solid #fed7aa;
}

.missing-experience-tag:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.no-skills-message {
  color: #9ca3af;
  font-style: italic;
  padding: 1rem;
}

/* Recommendations Section */
.recommendations-section {
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1.5rem;
  border-left: 4px solid #016064;
}

.recommendations-content {
  margin-top: 1rem;
}

.recommendation-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.recommendation-icon {
  font-size: 1.5rem;
  margin-top: 0.25rem;
}

.recommendation-text {
  color: #374151;
  font-size: 1rem;
  line-height: 1.6;
  margin: 0;
}
</style>

<template>
  <!-- Main Content -->
  <div class="max-w-5xl mx-auto mt-24 p-6 bg-white rounded-lg shadow">
    <!-- Heading Section -->
    <div class="heading-section">
      <h2 class="text-3xl font-bold text-gray-800 mb-4 ml-8">Match Results</h2>
      <div class="h-px bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 ml-8 mr-8"></div>
    </div>

    <!-- Loading State -->
    <div v-if="!matchResult && !error" class="loading-container">
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
        <h2 class="results-title">🎯 Analysis Results</h2>
        <p class="results-subtitle">Your resume match analysis is complete</p>
      </div>
      
      <div class="results-divider"></div>
      
      <div class="results-content">
        <!-- Overall Score Section -->
        <div class="score-section overall-score">
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
            <span v-if="matchResult.matched_skills && matchResult.matched_skills.length" 
                  class="matched-skill-tag" 
                  v-for="skill in matchResult.matched_skills" 
                  :key="skill">
              {{ skill }}
            </span>
            <span v-else class="no-skills-message">No matching skills found</span>
          </div>
        </div>

        <!-- Missing Requirements Section -->
        <div class="skills-section">
          <h3 class="section-title">❌ Missing Requirements</h3>
          
          <!-- Missing Skills -->
          <div v-if="matchResult.missing_skills && matchResult.missing_skills.length" class="missing-subsection">
            <h4 class="missing-subtitle">Missing Skills:</h4>
            <div class="missing-skills-container">
              <span class="missing-skill-tag" 
                    v-for="skill in matchResult.missing_skills" 
                    :key="skill">
                {{ skill }}
              </span>
            </div>
          </div>

          <!-- Missing Experience -->
          <div v-if="matchResult.missing_experience && matchResult.missing_experience.length" class="missing-subsection">
            <h4 class="missing-subtitle">Missing Experience:</h4>
            <div class="missing-experience-container">
              <span class="missing-experience-tag" 
                    v-for="exp in matchResult.missing_experience" 
                    :key="exp">
                {{ exp }}
              </span>
            </div>
          </div>

          <!-- No Missing Requirements -->
          <div v-if="(!matchResult.missing_skills || !matchResult.missing_skills.length) && 
                      (!matchResult.missing_experience || !matchResult.missing_experience.length)" 
               class="no-skills-message">
            No missing requirements found
          </div>
        </div>

        <!-- Recommendations Section -->
        <div class="recommendations-section">
          <h3 class="section-title">💡 Recommendations</h3>
          <div class="recommendations-content">
            <div class="recommendation-item">
              <span class="recommendation-icon">📝</span>
              <p class="recommendation-text">
                Based on your {{ Math.round(matchResult.overall_score * 100) }}% match score, 
                {{ matchResult.overall_score >= 0.7 ? 'you have a strong alignment with this position!' : 
                   matchResult.overall_score >= 0.5 ? 'you have moderate alignment with this position.' : 
                   'you may need to enhance your skills or experience for this position.' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
