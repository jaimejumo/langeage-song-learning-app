<template>
  <div class="lyrics">
    <div v-for="(line, index) in visibleLines" :key="index"
      :class="{ active: line.index === currentLineIndex }">
      <span v-if="line.index === currentLineIndex && line.blank && !answered">
        <span>{{ line.before }}</span>
        <input
          data-cy="blankInput"
          v-model="userInput"
          @keyup.enter="checkAnswer"
        />
        <button data-cy="skip" @click="skip">Skip</button>
        <span>{{ line.after }}</span>
      </span>
      <span v-else>{{ line.text }}</span>
    </div>
    <div v-if="summary" class="summary">
      <p>Correct answers: {{ summary.correct }} - Wrong answers: {{ summary.wrong }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  song: Object,
  currentTime: Number,
  audioEnded: Boolean
})

watch(() => props.audioEnded, (val) => {
  if (val) endSong()
})

const emit = defineEmits(['stopAudio', 'startAudio', 'summary'])

const lines = ref([])
const currentLineIndex = ref(-1)
const userInput = ref('')
const answered = ref(false)
const correctGuesses = ref(0)
const wrongGuesses = ref(0)
const finished = ref(false)
const summary = ref(null)
const waitingForInput = ref(false)

async function loadLyrics() {
  if (!props.song || !props.song.lrc_file) return
  const res = await fetch(props.song.lrc_file)
  const text = await res.text()
  const parsed = []
  const lineRegex = /\[(\d+):(\d+\.\d+)\](.*)/
  for (const line of text.split('\n')) {
    const match = line.match(lineRegex)
    if (!match) continue
    const minutes = parseInt(match[1])
    const seconds = parseFloat(match[2])
    const time = minutes * 60 + seconds
    const content = match[3].trim()
    const blankMatch = content.match(/^(.*?)\{([^}]+)\}(.*)$/)
    if (blankMatch) {
      parsed.push({
        time,
        text: content.replace(/\{(\w+)\}/, '_____'),
        blank: true,
        before: blankMatch[1],
        answer: blankMatch[2],
        after: blankMatch[3]
      })
    } else {
      parsed.push({ time, text: content, blank: false })
    }
  }
  lines.value = parsed.map((l, i) => ({ ...l, index: i }))
}

watch(() => props.song, loadLyrics, { immediate: true })

watch(() => props.currentTime, (time) => {
  if (finished.value) return

  // find current line
  let newIndex = -1
  for (let i = lines.value.length - 1; i >= 0; i--) {
    if (time >= lines.value[i].time) {
      newIndex = i
      break
    }
  }

  if (newIndex === -1) return

  // check if we moved to a new line
  if (newIndex !== currentLineIndex.value) {
    // if previous line had blank and wasn't answered, count as wrong
    if (currentLineIndex.value >= 0) {
      const prev = lines.value[currentLineIndex.value]
      if (prev && prev.blank && !answered.value && waitingForInput.value) {
        wrongGuesses.value++
      }
    }
    currentLineIndex.value = newIndex
    answered.value = false
    userInput.value = ''
    waitingForInput.value = false
  }

  // check if next line exists and if we are close to it
  const nextLine = lines.value[newIndex + 1]
  const currentLine = lines.value[newIndex]

  if (currentLine && currentLine.blank && !answered.value && !waitingForInput.value) {
    // stop audio just before the next line starts
    if (!nextLine || time >= nextLine.time - 0.5) {
      waitingForInput.value = true
      emit('stopAudio')
    }
  }

  // check if song finished (last line passed by 3 seconds)
  if (newIndex === lines.value.length - 1 && nextLine === undefined) {
    const lastLine = lines.value[lines.value.length - 1]
    if (time >= lastLine.time + 3) {
      endSong()
    }
  }
})

const visibleLines = computed(() => {
  const idx = currentLineIndex.value
  if (idx === -1) return []
  return lines.value.filter(l => l.index >= idx - 1 && l.index <= idx + 1)
})

function checkAnswer() {
  const current = lines.value[currentLineIndex.value]
  if (!current || !current.blank) return
  if (userInput.value.trim().toLowerCase() === current.answer.toLowerCase()) {
    correctGuesses.value++
    answered.value = true
    waitingForInput.value = false
    userInput.value = ''
    emit('startAudio')
  } else {
    wrongGuesses.value++
    userInput.value = ''
  }
}

function skip() {
  wrongGuesses.value++
  answered.value = true
  waitingForInput.value = false
  userInput.value = ''
  emit('startAudio')
}

function endSong() {
  if (finished.value) return
  finished.value = true
  const result = {
    correct: correctGuesses.value,
    wrong: wrongGuesses.value
  }
  summary.value = result
  emit('summary', result)
}
</script>

<style scoped>
.lyrics { text-align: center; font-size: 1.1rem; line-height: 2.5; color: white; }
.active { font-weight: bold; font-size: 1.3rem; }
input {
  padding: 4px 8px;
  border: 2px solid #00b894;
  border-radius: 4px;
  margin: 0 8px;
  width: 120px;
  background: rgba(255,255,255,0.9);
}
button {
  padding: 4px 10px;
  background: #636e72;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.summary {
  margin-top: 30px;
  font-size: 1.4rem;
  font-weight: bold;
  color: #00b894;
}
</style>