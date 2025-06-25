import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('../components/HelloWorld.vue'), name: 'Home' },
  { path: '/collect', component: () => import('../views/DataCollect.vue'), name: 'DataCollect' },
  { path: '/kb', component: () => import('../views/KnowledgeBase.vue'), name: 'KnowledgeBase' },
  { path: '/qa', component: () => import('../views/QA.vue'), name: 'QA' },
  // 可选：微调页
  // { path: '/finetune', component: () => import('../views/Finetune.vue'), name: 'Finetune' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
