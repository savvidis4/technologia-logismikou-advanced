import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import HomeView from '@/views/HomeView.vue'
import RegisterView from '@/views/RegisterView.vue'
import TransferView from '@/views/TransferView.vue'
import TransactionsView from '@/views/TransactionsView.vue'
import CurrencyExchangeView from '@/views/CurrencyExchangeView.vue'
import SettingsView from '@/views/SettingsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', component: LoginView },
    { path: '/home', component: HomeView },
    { path: '/register', component: RegisterView },
    { path: '/transfers', component: TransferView },
    { path: '/transactions', component: TransactionsView },
    { path: '/currency-exchange', component: CurrencyExchangeView },
    { path: '/settings', component: SettingsView },
  ]
})

export default router
