<template>
  <div class="login-box">
    <h2>Welcome back</h2>
    <p>Sign in to track your progress</p>
    <input v-model="username" data-cy="username" placeholder="Username" type="text" />
    <input v-model="password" data-cy="password" placeholder="Password" type="password" />
    <button @click="login">LOG IN</button>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const username = ref('')
const password = ref('')
const error = ref('')

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

async function login() {
  error.value = ''
  const res = await fetch(`${API}/api/v1/token/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `username=${username.value}&password=${password.value}`
  })
  const data = await res.json()
  if (data.auth_token) {
    auth.setToken(data.auth_token, username.value)
    router.push('/')
  } else {
    error.value = 'Invalid credentials'
  }
}
</script>

<style scoped>
.login-box { max-width: 380px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); display: flex; flex-direction: column; gap: 14px; }
h2 { text-align: center; }
p { text-align: center; color: #636e72; font-size: 0.9rem; }
input { padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; }
button { padding: 12px; background: #00b894; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem; font-weight: bold; }
.error { color: #d63031; }
</style>