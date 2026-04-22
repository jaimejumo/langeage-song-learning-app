<template>
  <div class="audio-player">
    <p>{{ song.title }} - {{ song.artist }}</p>
    <audio
      id="my-audio"
      ref="audio"
      :src="song.audio_file"
      @timeupdate="emitTimeUpdate"
      @ended="emitEnded"
      controls
    ></audio>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  song: Object,
  stopAudio: Boolean
})

const emit = defineEmits(['onTimeUpdate', 'onEnded'])

const audio = ref(null)

watch(() => props.stopAudio, (val) => {
  if (!audio.value) return
  if (val) {
    audio.value.pause()
  } else {
    audio.value.play()
  }
})

function emitTimeUpdate() {
  emit('onTimeUpdate', audio.value.currentTime)
}

function emitEnded() {
  emit('onEnded')
}
</script>

<style scoped>
.audio-player {
  text-align: center;
  margin-bottom: 20px;
}
p {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
}
audio {
  width: 100%;
}
</style>