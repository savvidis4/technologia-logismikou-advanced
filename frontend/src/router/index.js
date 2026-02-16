import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import HomeView from '@/views/HomeView.vue'
import RegisterView from '@/views/RegisterView.vue'
import TransferView from '@/views/TransferView.vue'
import TransactionsView from '@/views/TransactionsView.vue'
import CurrencyExchangeView from '@/views/CurrencyExchangeView.vue'
import SettingsView from '@/views/SettingsView.vue'
import CardView from '@/views/CardView.vue'
import LogoutView from '@/views/LogoutView.vue'
import GraphsView from '@/views/GraphsView.vue'
import ChangePinView from '@/views/ChangePinView.vue'
import OtpView from '@/views/OtpView.vue'
import ChangeEmailView from '@/views/ChangeEmailView.vue'
import ChangePasswordView from '@/views/ChangePasswordView.vue'
import ForgetPasswordView from '@/views/ForgetPasswordView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', component: LoginView },
    { path: '/logout', component: LogoutView },
    { path: '/home', component: HomeView },
    { path: '/register', component: RegisterView },
    { path: '/transfers', component: TransferView },
    { path: '/transactions', component: TransactionsView },
    { path: '/exchange', component: CurrencyExchangeView },
    { path: '/card', component: CardView },
    { path: '/settings', component: SettingsView },
    { path: '/graphs', component: GraphsView },
    { path: '/change_pin', component: ChangePinView },
    { path: '/otp', component: OtpView },
    { path: '/change_email', component: ChangeEmailView },
    { path: '/change_password', component: ChangePasswordView },
    { path: '/forgot_password', component: ForgetPasswordView }

  ]
})

export default router
