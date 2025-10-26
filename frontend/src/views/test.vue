<template>
  <div class="login">
    <h2>Sign In</h2>
    <form @submit.prevent="login">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api, setAuthToken } from '../services/api'

const email = ref('')
const password = ref('')

async function login() {
  try {
    const res = await api.post('/login', {
      email: email.value,
      password: password.value
    })

    const token = res.data.token
    localStorage.setItem('token', token)
    setAuthToken(token)
    alert('Login successful!')
    window.location.href = '/home' // redirect
  } catch (err) {
    alert('Invalid credentials')
  }
}
</script>
