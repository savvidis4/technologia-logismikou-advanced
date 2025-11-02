import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import TransfersView from '../views/TransfersView.vue'
import TransactionsView from '../views/TransactionsView.vue'
import CurrencyExchangeView from '../views/CurrencyExchangeView.vue'
import CardView from '../views/CardView.vue'
import GraphsView from '../views/GraphsView.vue'
import SettingsView from '../views/SettingsView.vue'
import LogoutView from '../views/LogoutView.vue'
import SignInView from '../views/SignInView.vue'
import SignUpView from '../views/SignUpView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: HomeView },        
    { path: '/transfers', component: TransfersView },
    { path: '/transactions', component: TransactionsView },
    { path: '/currency', component: CurrencyExchangeView },
    { path: '/card', component: CardView },
    { path: '/graphs', component: GraphsView },
    { path: '/settings', component: SettingsView },
    { path: '/logout', component: LogoutView },
    { path: '/signin', component: SignInView },
    { path: '/signup', component: SignUpView }
  ]
})

export default router
