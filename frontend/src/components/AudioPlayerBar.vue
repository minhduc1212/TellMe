<template>
  <div class="audio-player-bar" v-if="audioUrl">
    <div class="player-container">
      <!-- Left: Big Play/Pause Button (Text Only) -->
      <button 
        class="play-circle-btn" 
        :class="{ playing: isPlaying }"
        @click="togglePlay"
      >
        <span>{{ isPlaying ? 'Tạm dừng' : 'Phát' }}</span>
      </button>

      <!-- Center: Track Info & Waveform Audio Progress -->
      <div class="player-center">
        <div class="track-meta">
          <span class="voice-tag">{{ currentVoice }}</span>
          <span class="engine-tag">{{ currentEngine }}</span>
        </div>

        <div class="waveform-progress-row">
          <span class="time-label">{{ formatTime(currentTime) }}</span>
          
          <!-- Animated Canvas/SVG Waveform Track -->
          <div class="waveform-track" @click="seekAudio">
            <div class="waveform-bars">
              <div 
                v-for="(height, i) in waveformHeights" 
                :key="i"
                class="bar"
                :class="{ active: (i / waveformHeights.length) <= progressRatio, playing: isPlaying }"
                :style="{ height: height + 'px' }"
              ></div>
            </div>
            <div class="progress-line" :style="{ width: (progressRatio * 100) + '%' }"></div>
          </div>

          <span class="time-label">{{ formatTime(duration) }}</span>
        </div>
      </div>

      <!-- Right Actions: Speed & Download -->
      <div class="player-actions">
        <!-- Speed Multiplier -->
        <button class="speed-btn" @click="cyclePlaybackRate">
          {{ playbackRate }}x
        </button>

        <!-- Download Audio File Button -->
        <a 
          :href="fullAudioUrl" 
          download 
          class="download-btn"
          title="Tải xuống audio"
        >
          Tải file
        </a>
      </div>
    </div>

    <!-- Hidden HTML5 Audio Element -->
    <audio 
      ref="audioRef" 
      :src="fullAudioUrl" 
      @timeupdate="onTimeUpdate" 
      @loadedmetadata="onLoadedMetadata" 
      @ended="onEnded"
    ></audio>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  audioUrl: {
    type: String,
    default: null
  },
  currentVoice: {
    type: String,
    default: 'Phạm Tuyên'
  },
  currentEngine: {
    type: String,
    default: 'Vieneu'
  },
  words: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['time-update', 'play-state-change'])

const audioRef = ref(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const playbackRate = ref(1.0)

const waveformHeights = [12, 24, 16, 32, 20, 28, 14, 36, 22, 18, 30, 26, 12, 24, 34, 18, 28, 16, 22, 30, 14, 26, 32, 20, 18, 28, 14, 30, 22, 16]

const fullAudioUrl = computed(() => {
  if (!props.audioUrl) return ''
  if (props.audioUrl.startsWith('http')) return props.audioUrl
  return `http://127.0.0.1:8000${props.audioUrl}`
})

const progressRatio = computed(() => {
  if (!duration.value) return 0
  return currentTime.value / duration.value
})

watch(() => props.audioUrl, (newUrl) => {
  if (newUrl) {
    setTimeout(() => {
      if (audioRef.value) {
        audioRef.value.play().then(() => {
          isPlaying.value = true
          emit('play-state-change', true)
        }).catch(() => {})
      }
    }, 100)
  }
})

function togglePlay() {
  if (!audioRef.value) return
  if (isPlaying.value) {
    audioRef.value.pause()
    isPlaying.value = false
    emit('play-state-change', false)
  } else {
    audioRef.value.play()
    isPlaying.value = true
    emit('play-state-change', true)
  }
}

function onTimeUpdate() {
  if (!audioRef.value) return
  currentTime.value = audioRef.value.currentTime
  emit('time-update', currentTime.value)
}

function onLoadedMetadata() {
  if (!audioRef.value) return
  duration.value = audioRef.value.duration
}

function onEnded() {
  isPlaying.value = false
  currentTime.value = 0
  emit('play-state-change', false)
}

function seekAudio(e) {
  if (!audioRef.value || !duration.value) return
  const rect = e.currentTarget.getBoundingClientRect()
  const clickX = e.clientX - rect.left
  const ratio = clickX / rect.width
  audioRef.value.currentTime = ratio * duration.value
}

function cyclePlaybackRate() {
  const rates = [1.0, 1.25, 1.5, 2.0]
  const nextIdx = (rates.indexOf(playbackRate.value) + 1) % rates.length
  playbackRate.value = rates[nextIdx]
  if (audioRef.value) {
    audioRef.value.playbackRate = playbackRate.value
  }
}

function formatTime(secs) {
  if (!secs || isNaN(secs)) return '0:00'
  const m = Math.floor(secs / 60)
  const s = Math.floor(secs % 60)
  return `${m}:${s < 10 ? '0' : ''}${s}`
}
</script>

<style scoped>
.audio-player-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--color-canvas-white);
  border-top: 1px solid var(--color-border-light);
  box-shadow: var(--shadow-sticky);
  z-index: 50;
  padding: 14px 24px;
}

.player-container {
  max-width: 1024px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 20px;
}

.play-circle-btn {
  padding: 10px 20px;
  border-radius: var(--radius-md);
  background-color: var(--color-electric-indigo);
  color: white;
  border: none;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.play-circle-btn:hover {
  transform: scale(1.04);
}

.play-circle-btn.playing {
  background-color: var(--color-cyan-signal);
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.4);
}

.player-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.track-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.voice-tag {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-slate-dark);
}

.engine-tag {
  font-size: 11px;
  font-weight: 500;
  color: var(--color-muted-slate);
  background-color: var(--color-panel-gray);
  padding: 1px 6px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border-light);
}

.waveform-progress-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.time-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--color-muted-slate);
  width: 34px;
}

.waveform-track {
  flex: 1;
  height: 36px;
  position: relative;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.waveform-bars {
  display: flex;
  align-items: center;
  gap: 3px;
  width: 100%;
  height: 100%;
}

.bar {
  flex: 1;
  background-color: var(--color-border-hover);
  border-radius: var(--radius-full);
  transition: background-color 0.15s ease, height 0.15s ease;
}

.bar.active {
  background-color: var(--color-electric-indigo);
}

.bar.active.playing {
  background-color: var(--color-cyan-signal);
}

.progress-line {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 2px;
  background-color: var(--color-cyan-signal);
  transition: width 0.1s linear;
}

.player-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.speed-btn {
  background-color: var(--color-panel-gray);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-slate-dark);
  cursor: pointer;
  transition: all 0.15s ease;
}

.speed-btn:hover {
  border-color: var(--color-electric-indigo);
  color: var(--color-electric-indigo);
}

.download-btn {
  background-color: var(--color-electric-indigo);
  color: white;
  text-decoration: none;
  border-radius: var(--radius-md);
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  transition: all 0.15s ease;
}

.download-btn:hover {
  background-color: var(--color-electric-indigo-hover);
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25);
}
</style>
