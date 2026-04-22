<template>
  <div class="logout-container">
    <h1>Log Out</h1>
    <p>You will be redirected to home in 5 seconds</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

onMounted(async () => {
  if (auth.token) {
    await fetch(`${API}/api/v1/token/logout/`, {
      method: 'POST',
      headers: { 'Authorization': `Token ${auth.token}` }
    })
    auth.clearToken()
  }
  setTimeout(() => {
    router.push('/')
  }, 5000)
})
</script>

<style scoped>
.logout-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
}
h1 { margin-bottom: 15px; }
</style>