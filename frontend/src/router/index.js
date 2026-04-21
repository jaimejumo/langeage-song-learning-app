import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import LogoutView from '../views/LogoutView.vue'
import PlayView from '../views/PlayView.vue'
import FaqView from '../views/FaqView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: HomeView },
    { path: '/log-in', component: LoginView },
    { path: '/log-out', component: LogoutView },
    { path: '/songs/:id', component: PlayView },
    { path: '/faq', component: FaqView },
  ],
})

export default router

