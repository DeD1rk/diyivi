import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import InitiatorView from '../views/exchange/InitiatorView.vue'
import RespondView from '../views//exchange/RespondView.vue'
import AboutView from '../views/AboutView.vue'
import CreateSignatureView from '@/views/signature/CreateSignatureView.vue'
import VerifySignatureView from '@/views/signature/VerifySignatureView.vue'
import RequestSignatureView from '@/views/signature/RequestSignatureView.vue'
import RespondSignatureView from '@/views/signature/RespondSignatureView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomeView
    },
    {
      path: '/exchange/start/',
      component: InitiatorView
    },
    {
      path: '/exchange/respond/:exchangeId/',
      name: 'exchange-respond',
      component: RespondView,
      props: true
    },
    {
      path: '/signature/create/',
      component: CreateSignatureView
    },
    {
      path: '/signature/verify/',
      component: VerifySignatureView
    },
    {
      path: '/signature/request/create/',
      component: RequestSignatureView
    },
    {
      path: '/signature/request/respond/:requestId/',
      component: RespondSignatureView,
      props: true
    },
    {
      path: '/about',
      component: AboutView
    }
  ]
})

export default router
