<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api, setAuthToken } from '@/services/api'

const email = ref('')
const password = ref('')

async function loginUser() {
  try {
    const res = await api.post('/login', {
      email: email.value,
      password: password.value
    })
    const token = res.data.token
    localStorage.setItem('token', token)
    setAuthToken(token)
    alert('Login successful!')
    window.location.href = '/home'
  } catch (err) {
    alert('Invalid email or password')
  }
}
</script>

<style scoped>
.login {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-top: 100px;
}
input {
  padding: 8px;
  width: 200px;
}
button {
  padding: 8px 16px;
}
</style>
