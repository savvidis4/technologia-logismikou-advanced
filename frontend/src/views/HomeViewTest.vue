<template>
  <section v-if="data">
    <h2 style="background-color: black;">Welcome, {{ data.username }}</h2>
    <p style="background-color: black;">Email: {{ data.email }}</p>
    <p style="background-color: black;">Balance: €{{ data.euro_balance }}</p>
    <p style="background-color: black;">IBAN: {{ data.iban }}</p>
    <p style="background-color: black;">Card: {{ data.card_number }}</p>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api, setAuthToken } from '@/services/api'

const data = ref(null)

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    window.location.href = '/login'
    return
  }

  setAuthToken(token)

  try {
    const res = await api.get('/home')
    data.value = res.data
  } catch (err) {
    console.error(err)
    alert('Session expired — please login again')
    localStorage.removeItem('token')
    window.location.href = '/login'
  }
})
</script>
