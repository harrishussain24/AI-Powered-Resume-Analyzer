import { defineStore } from 'pinia'

export const useResumeStore = defineStore('resume', {
  state: () => ({
    resumeData: null,
    jobDescriptionData: null,
  }),
  actions: {
    setResume(data) {
      this.resumeData = data
    },
    setJobDescription(data) {
      this.jobDescriptionData = data
    }
  }
})
