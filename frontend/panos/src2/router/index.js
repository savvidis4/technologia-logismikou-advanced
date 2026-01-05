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
import ChangePasswordView from '../views/ChangePasswordView.vue'
import ChangePinView from '../views/ChangePinView.vue'
import ChangeEmailView from '../views/ChangeEmailView.vue'

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
    { path: '/signup', component: SignUpView },
    { path: '/change-password', component: ChangePasswordView },
    { path: '/change-pin', component: ChangePinView },
    { path: '/change-email', component: ChangeEmailView },
  ]
})

/* ----------------------------------------------------------
   ROUTE GUARD: ΑΠΑΓΟΡΕΥΕΙ ΠΡΟΣΒΑΣΗ ΧΩΡΙΣ LOGIN TOKEN
----------------------------------------------------------- */
router.beforeEach((to, from, next) => {

  // Αυτές είναι δημόσιες σελίδες
  const publicPages = ['/signin', '/signup'];

  // Αν η σελίδα δεν είναι public → χρειάζεται login
  const authRequired = !publicPages.includes(to.path);

  // Παίρνουμε το token που βάλαμε στο localStorage μετά το login
  const token = localStorage.getItem('token');

  // Αν χρειάζεται login ΚΑΙ δεν υπάρχει token → redirect στο sign in
  if (authRequired && !token) {
    return next('/signin');
  }

  // Αλλιώς, άφησέ τον να περάσει
  next();
});

export default router
