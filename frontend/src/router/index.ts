import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('../views/Home.vue'), name: 'Home' },
  { path: '/collect', component: () => import('../views/DataCollect.vue'), name: 'DataCollect' },
  { path: '/kb', component: () => import('../views/KnowledgeBase.vue'), name: 'KnowledgeBase' },
  { path: '/qa', component: () => import('../views/QA.vue'), name: 'QA' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
