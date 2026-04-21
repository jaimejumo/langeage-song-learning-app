<template>
  <div>
    <div class="hero">
      <h1>Learn languages through music 🎵</h1>
      <p>Listen to songs and fill in the missing words in real time</p>
      <button @click="goToRandom">Random song</button>
    </div>

    <h2>Top Songs</h2>
    <div class="song-grid">
      <router-link
        v-for="song in topSongs"
        :key="song.id"
        :to="`/songs/${song.id}`"
        :data-cy="song.title"
        class="song-card"
      >
        <img :src="song.background_image" :alt="song.title" />
        <div class="song-info">
          <strong>{{ song.title }}</strong>
          <span>{{ song.artist }}</span>
        </div>
      </router-link>
    </div>

    <div class="search-bar">
      <input
        v-model="searchText"
        data-cy="search_text"
        placeholder="Search by title..."
        @keyup.enter="searchSongs"
      />
      <button data-cy="search_button" @click="searchSongs">Search</button>
    </div>

    <div v-if="searchResults.length" class="song-grid">
      <router-link
        v-for="song in searchResults"
        :key="song.id"
        :to="`/songs/${song.id}`"
        :data-cy="song.title"
        class="song-card"
      >
        <img :src="song.background_image" :alt="song.title" />
        <div class="song-info">
          <strong>{{ song.title }}</strong>
          <span>{{ song.artist }}</span>
        </div>
      </router-link>
    </div>

    <p v-if="searchResults.length === 0 && searched" class="no-results">No songs found</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const topSongs = ref([])
const searchText = ref('')
const searchResults = ref([])
const searched = ref(false)

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

onMounted(async () => {
  const res = await fetch(`${API}/api/v1/songs/top/?n=3`)
  topSongs.value = await res.json()
})

async function goToRandom() {
  const res = await fetch(`${API}/api/v1/songs/random/`)
  const song = await res.json()
  router.push(`/songs/${song.id}`)
}

async function searchSongs() {
  if (!searchText.value) return
  searched.value = true
  const res = await fetch(`${API}/api/v1/songs/search/?title=${searchText.value}`)
  const data = await res.json()
  searchResults.value = Array.isArray(data) ? data : []
}
</script>

<style scoped>
.hero { text-align: center; padding: 40px 0; }
h1 { font-size: 2rem; margin-bottom: 10px; }
p { color: #636e72; margin-bottom: 20px; }
h2 { margin: 30px 0 15px; font-size: 1.3rem; }
button { background: #00b894; color: white; border: none; padding: 10px 24px; border-radius: 6px; cursor: pointer; font-size: 1rem; }
.song-grid { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 30px; }
.song-card { width: 200px; background: white; border-radius: 8px; overflow: hidden; text-decoration: none; color: inherit; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.2s; }
.song-card:hover { transform: translateY(-4px); }
.song-card img { width: 100%; height: 130px; object-fit: cover; }
.song-info { padding: 10px; display: flex; flex-direction: column; gap: 4px; }
.song-info span { color: #636e72; font-size: 0.85rem; }
.search-bar { display: flex; gap: 10px; margin-bottom: 20px; }
input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; }
.no-results { color: #636e72; text-align: center; }
</style>