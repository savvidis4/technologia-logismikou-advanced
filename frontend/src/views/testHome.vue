<template>
  <section v-if="data">
    <h2>Welcome, {{ data.username }}</h2>
    <p>Balance: €{{ data.balance }}</p>
    <p>IBAN: {{ data.iban }}</p>
    <p>Card: {{ data.card_number }}</p>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api, setAuthToken } from '../services/api'

const data = ref(null)

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    window.location.href = '/signin'
    return
  }
  setAuthToken(token)

  try {
    const res = await api.get('/home')
    data.value = res.data
  } catch (err) {
    console.error(err)
    alert('Session expired. Please login again.')
    localStorage.removeItem('token')
    window.location.href = '/signin'
  }
})
</script>
