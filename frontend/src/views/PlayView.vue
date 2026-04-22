<template>
  <div class="play-view" :style="backgroundStyle">
    <div class="overlay">
      <AudioPlayer
        v-if="song"
        :song="song"
        :stopAudio="stopAudio"
        @onTimeUpdate="handleTimeUpdate"
        @onEnded="handleEnded"
      />
      <LyricsDisplay
        v-if="song"
        :song="song"
        :currentTime="currentTime"
        :audioEnded="audioEnded"
        @stopAudio="stopAudio = true"
        @startAudio="stopAudio = false"
        @summary="handleSummary"
      />
      <div v-if="summary" class="summary">
        <p>Correct answers: {{ summary.correct }} - Wrong answers: {{ summary.wrong }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import AudioPlayer from '../components/AudioPlayer.vue'
import LyricsDisplay from '../components/LyricsDisplay.vue'

const route = useRoute()
const auth = useAuthStore()

const song = ref(null)
const stopAudio = ref(false)
const currentTime = ref(0)
const summary = ref(null)
const audioEnded = ref(false)

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

onMounted(async () => {
  const res = await fetch(`${API}/api/v1/songs/${route.params.id}/`)
  song.value = await res.json()
})

const backgroundStyle = computed(() => {
  if (!song.value) return {}
  return {
    backgroundImage: `url(${song.value.background_image})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    minHeight: '100vh'
  }
})

function handleTimeUpdate(time) {
  currentTime.value = time
}

function handleEnded() {
  audioEnded.value = true
}

async function handleSummary(data) {
  summary.value = data
  if (auth.token) {
    await fetch(`${API}/api/v1/songusers/`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${auth.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        song: song.value.id,
        correct_guesses: data.correct,
        wrong_guesses: data.wrong
      })
    })
  }
}
</script>

<style scoped>
.play-view { min-height: 100vh; }
.overlay {
  background: rgba(0,0,0,0.6);
  min-height: 100vh;
  padding: 40px 20px;
  color: white;
}
.summary {
  margin-top: 30px;
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: #00b894;
}
</style>