import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import InitiatorExchangeView from '../views/InitiatorExchangeView.vue'
import ExchangeCreateView from '../views/ExchangeCreateView.vue'
import ExchangeStartView from '../views/ExchangeStartView.vue'
import ExchangeRespondView from '../views/ExchangeRespondView.vue'
import AboutView from '../views/AboutView.vue'
import { initiatorExchangeKey } from '@/lib/keys'
import { inject } from 'vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/exchange/',
      component: InitiatorExchangeView,
      children: [
        {
          path: '/exchange/create/',
          name: 'exchange-create',
          component: ExchangeCreateView
        },
        {
          path: '/exchange/start/',
          name: 'exchange-start',
          component: ExchangeStartView,
          beforeEnter: (to) => {
            console.log('beforeEnter', to)
            const exchange = inject(initiatorExchangeKey)
            console.log('exchange', exchange)
          }
        }
      ]
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
