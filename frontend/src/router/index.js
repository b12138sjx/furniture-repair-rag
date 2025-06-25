import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import QaPage from '../views/QaPage.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/qa',
    name: 'QaPage',
    component: QaPage
  },
  {
    path: '/knowledge',
    name: 'KnowledgeBase',
    component: () => import('../views/KnowledgeBase.vue')
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

 export default router;