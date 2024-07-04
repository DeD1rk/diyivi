import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ExchangeStartView from '../views/ExchangeStartView.vue'
import ExchangeRespondView from '../views/ExchangeRespondView.vue'
import AboutView from '../views/AboutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/exchange/start/',
      name: 'exchange-start',
      component: ExchangeStartView
    },
    {
      path: '/exchange/respond/:id/',
      name: 'exchange-respond',
      component: ExchangeRespondView,
      props: true
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    }
  ]
})

export default router
