<template>
  <div class="app-layout">
    <!-- Navbar -->
    <Navbar 
      :isBackendOnline="isBackendOnline" 
      :historyCount="history.length"
      @open-history="isHistoryOpen = true"
    />

    <!-- Main Content Container -->
    <main class="main-container">
      <div class="header-section">
        <h1 class="page-title">Text to Speech Converter</h1>
        <p class="page-subtitle">
          Chuyển đổi văn bản thành giọng nói Tiếng Việt tự nhiên & Sao chép giọng mẫu tức thì với Vieneu TTS v3 Turbo.
        </p>
      </div>

      <!-- Settings & Inputs Grid -->
      <div class="workspace-grid">
        <!-- Configuration Column -->
        <div class="config-column">
          <!-- Engine & Voice Selector -->
          <EngineVoiceSelector 
            v-model:selectedEngine="selectedEngine"
            v-model:selectedVoice="selectedVoice"
            :voices="voices"
          />

          <!-- Voice Cloning Panel (when Vieneu is active) -->
          <VoiceCloningPanel 
            v-if="selectedEngine === 'vieneu'"
            v-model:isCloningEnabled="isCloningEnabled"
            v-model:refAudioPath="refAudioPath"
          />

          <!-- Fine-tuning Controls -->
          <AudioControls 
            v-model:speed="speed"
            v-model:pitch="pitch"
            v-model:temperature="temperature"
            :engine="selectedEngine"
          />
        </div>

        <!-- Text Input & Generation Column -->
        <div class="editor-column">
          <TextInputCanvas 
            v-model:text="text"
            :isPlayingWithWords="isPlaying && currentAudio?.words?.length > 0"
            :wordList="currentAudio?.words || []"
            :currentWordIndex="currentWordIndex"
            @stop-highlight-view="isPlaying = false"
          />

          <!-- Main Generate Speech Action Button -->
          <div class="action-bar">
            <button 
              class="btn-generate" 
              :disabled="isGenerating || !text.trim()"
              @click="generateSpeech"
            >
              <div v-if="isGenerating" class="spinner-sm"></div>
              <span>{{ isGenerating ? 'Đang khởi tạo giọng đọc...' : 'Tạo Giọng Nói (Generate Speech)' }}</span>
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Floating Sticky Audio Player Bar -->
    <AudioPlayerBar 
      v-if="currentAudio"
      :audioUrl="currentAudio.url"
      :currentVoice="currentAudio.voice"
      :currentEngine="currentAudio.engine"
      :words="currentAudio.words"
      @time-update="handleTimeUpdate"
      @play-state-change="handlePlayStateChange"
    />

    <!-- History Drawer -->
    <HistoryDrawer 
      :isOpen="isHistoryOpen"
      :history="history"
      @close="isHistoryOpen = false"
      @play-item="playHistoryItem"
      @delete-item="deleteHistoryItem"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Navbar from './components/Navbar.vue'
import EngineVoiceSelector from './components/EngineVoiceSelector.vue'
import VoiceCloningPanel from './components/VoiceCloningPanel.vue'
import AudioControls from './components/AudioControls.vue'
import TextInputCanvas from './components/TextInputCanvas.vue'
import AudioPlayerBar from './components/AudioPlayerBar.vue'
import HistoryDrawer from './components/HistoryDrawer.vue'

const API_BASE = 'http://127.0.0.1:8000/api'

const isBackendOnline = ref(false)
const selectedEngine = ref('vieneu')
const selectedVoice = ref('Phạm Tuyên')
const isCloningEnabled = ref(false)
const refAudioPath = ref(null)

const speed = ref(1.0)
const pitch = ref(0.0)
const temperature = ref(0.8)

const text = ref('"Thọc và kéo," bà lão đang nói, "đó là cách của Nữ hoàng, cũng giống như chính các vị thần vậy." Mụ nghiêng người sang một bên và nhổ bọt, rồi đưa một mảnh vải bẩn lên đôi môi nhăn nheo.')
const isGenerating = ref(false)

const voices = ref({ vieneu: [], edge: [], google: [] })
const currentAudio = ref(null)
const isPlaying = ref(false)
const currentWordIndex = ref(-1)

const history = ref([])
const isHistoryOpen = ref(false)

onMounted(async () => {
  checkBackendHealth()
  fetchVoices()
  fetchHistory()
})

async function checkBackendHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`)
    if (res.ok) {
      isBackendOnline.value = true
    }
  } catch (err) {
    isBackendOnline.value = false
  }
}

async function fetchVoices() {
  try {
    const res = await fetch(`${API_BASE}/voices`)
    if (res.ok) {
      voices.value = await res.json()
    }
  } catch (err) {
    console.error('Failed to fetch voices:', err)
  }
}

async function fetchHistory() {
  try {
    const res = await fetch(`${API_BASE}/tts/history`)
    if (res.ok) {
      history.value = await res.json()
    }
  } catch (err) {
    console.error('Failed to fetch history:', err)
  }
}

async function generateSpeech() {
  if (!text.value.trim()) return

  isGenerating.value = true
  try {
    const payload = {
      text: text.value,
      engine: selectedEngine.value,
      voice_id: selectedVoice.value,
      speed: speed.value,
      pitch: pitch.value,
      temperature: temperature.value,
      ref_audio_path: (selectedEngine.value === 'vieneu' && isCloningEnabled.value) ? refAudioPath.value : null
    }

    const res = await fetch(`${API_BASE}/tts/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!res.ok) {
      const errData = await res.json()
      throw new Error(errData.detail || 'Synthesis failed')
    }

    const data = await res.json()
    currentAudio.value = data
    isPlaying.value = true
    fetchHistory()
  } catch (err) {
    alert('Lỗi tạo giọng nói: ' + err.message)
  } finally {
    isGenerating.value = false
  }
}

function handleTimeUpdate(currentTime) {
  if (!currentAudio.value || !currentAudio.value.words) return
  const wordList = currentAudio.value.words
  const idx = wordList.findIndex(w => currentTime >= w.start && currentTime <= w.end)
  if (idx !== -1) {
    currentWordIndex.value = idx
  }
}

function handlePlayStateChange(playingState) {
  isPlaying.value = playingState
}

function playHistoryItem(item) {
  currentAudio.value = item
  isPlaying.value = true
  isHistoryOpen.value = false
}

async function deleteHistoryItem(id) {
  try {
    const res = await fetch(`${API_BASE}/tts/history/${id}`, { method: 'DELETE' })
    if (res.ok) {
      fetchHistory()
      if (currentAudio.value && currentAudio.value.id === id) {
        currentAudio.value = null
      }
    }
  } catch (err) {
    console.error('Failed to delete item:', err)
  }
}
</script>

<style>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding-bottom: 90px;
}

.main-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 32px 24px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.header-section {
  text-align: center;
  margin-bottom: 8px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-slate-dark);
  letter-spacing: -0.01em;
}

.page-subtitle {
  font-size: 15px;
  color: var(--color-muted-slate);
  margin-top: 6px;
}

.workspace-grid {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 24px;
}

@media (max-width: 860px) {
  .workspace-grid {
    grid-template-columns: 1fr;
  }
}

.config-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.editor-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.action-bar {
  display: flex;
  justify-content: flex-end;
}

.btn-generate {
  width: 100%;
  background-color: var(--color-electric-indigo);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  padding: 14px 24px;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
  transition: all 0.2s ease;
}

.btn-generate:hover:not(:disabled) {
  background-color: var(--color-electric-indigo-hover);
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(79, 70, 229, 0.4);
}

.btn-generate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner-sm {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
</style>
