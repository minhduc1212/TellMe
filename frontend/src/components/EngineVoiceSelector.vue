<template>
  <div class="engine-voice-selector">
    <!-- Engine Selector Tabs -->
    <div class="section-label">TTS Engine Provider</div>
    <div class="engine-tabs">
      <button 
        class="tab-btn" 
        :class="{ active: selectedEngine === 'vieneu' }"
        @click="selectEngine('vieneu')"
      >
        <span class="tab-title">Vieneu TTS</span>
        <span class="tab-tag">High Quality</span>
      </button>

      <button 
        class="tab-btn" 
        :class="{ active: selectedEngine === 'edge' }"
        @click="selectEngine('edge')"
      >
        <span class="tab-title">Edge Neural</span>
        <span class="tab-tag">Multi-language</span>
      </button>

      <button 
        class="tab-btn" 
        :class="{ active: selectedEngine === 'google' }"
        @click="selectEngine('google')"
      >
        <span class="tab-title">Google TTS</span>
        <span class="tab-tag">Standard</span>
      </button>
    </div>

    <!-- Voice Selection -->
    <div class="voice-dropdown-wrapper">
      <div class="section-label flex-between">
        <span>Voice Speaker</span>
        <span v-if="selectedVoiceObj?.supports_cloning" class="clone-badge">
          Hỗ trợ Sao chép Giọng
        </span>
      </div>

      <select 
        class="voice-select" 
        :value="selectedVoice"
        @change="$emit('update:selectedVoice', $event.target.value)"
      >
        <option 
          v-for="voice in filteredVoices" 
          :key="voice.id" 
          :value="voice.voice_id"
        >
          {{ voice.name }} ({{ voice.gender || 'Standard' }} - {{ voice.accent || voice.lang }})
        </option>
      </select>
      
      <div class="voice-description" v-if="selectedVoiceObj">
        <span class="desc-text">{{ selectedVoiceObj.description }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  selectedEngine: {
    type: String,
    default: 'vieneu'
  },
  selectedVoice: {
    type: String,
    default: 'Phạm Tuyên'
  },
  voices: {
    type: Object,
    default: () => ({ vieneu: [], edge: [], google: [] })
  }
})

const emit = defineEmits(['update:selectedEngine', 'update:selectedVoice'])

function selectEngine(engineKey) {
  emit('update:selectedEngine', engineKey)
  const available = props.voices[engineKey] || []
  if (available.length > 0) {
    emit('update:selectedVoice', available[0].voice_id)
  }
}

const filteredVoices = computed(() => {
  return props.voices[props.selectedEngine] || []
})

const selectedVoiceObj = computed(() => {
  return filteredVoices.value.find(v => v.voice_id === props.selectedVoice) || filteredVoices.value[0]
})
</script>

<style scoped>
.engine-voice-selector {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--color-muted-slate);
}

.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.engine-tabs {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  background-color: var(--color-panel-gray);
  padding: 4px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
}

.tab-btn {
  background: transparent;
  border: none;
  padding: 10px 8px;
  border-radius: var(--radius-sm);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.tab-btn:hover {
  background-color: rgba(255, 255, 255, 0.6);
}

.tab-btn.active {
  background-color: var(--color-canvas-white);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
}

.tab-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-slate-dark);
}

.tab-tag {
  font-size: 10px;
  color: var(--color-muted-slate);
}

.tab-btn.active .tab-title {
  color: var(--color-electric-indigo);
}

.voice-dropdown-wrapper {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.voice-select {
  width: 100%;
  padding: 10px 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-hover);
  background-color: var(--color-canvas-white);
  font-family: var(--font-inter);
  font-size: 14px;
  font-weight: 500;
  color: var(--color-slate-dark);
  outline: none;
  cursor: pointer;
  transition: border-color 0.15s ease;
}

.voice-select:focus {
  border-color: var(--color-electric-indigo);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12);
}

.clone-badge {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-cyan-signal);
  background-color: var(--color-cyan-light);
  padding: 2px 8px;
  border-radius: var(--radius-full);
}

.voice-description {
  font-size: 12px;
  color: var(--color-muted-slate);
  padding-left: 2px;
}
</style>
