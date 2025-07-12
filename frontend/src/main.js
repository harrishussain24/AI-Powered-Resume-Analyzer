import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import {createRouter, createWebHistory} from 'vue-router'
import { createPinia } from 'pinia'

// Import your components
import ResumeUploader from './views/uploadresume.vue'
import JobDescriptionUploader from './views/uploadjobdescription.vue'
import MatchResults from './views/matchresults.vue'

const pinia = createPinia()

const routes = [
    { path: '/', component: ResumeUploader },
    { path: '/job-description', component: JobDescriptionUploader, props: true },
    { path: '/match-results', component: MatchResults } 
  ]

const router = createRouter({
    history: createWebHistory(),
    routes
})


createApp(App).use(pinia).use(router).mount('#app')
