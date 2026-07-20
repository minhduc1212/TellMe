<template>
  <div class="audio-controls">
    <div class="control-group">
      <div class="control-header">
        <label class="control-label">Speed / Rate</label>
        <span class="control-value">{{ speed }}x</span>
      </div>
      <input 
        type="range" 
        min="0.5" 
        max="2.0" 
        step="0.05" 
        :value="speed"
        @input="$emit('update:speed', parseFloat($event.target.value))"
        class="custom-slider" 
      />
      <div class="preset-chips">
        <button 
          v-for="s in [0.75, 1.0, 1.25, 1.5, 2.0]" 
          :key="s" 
          class="chip"
          :class="{ active: speed === s }"
          @click="$emit('update:speed', s)"
        >
          {{ s }}x
        </button>
      </div>
    </div>

    <!-- Pitch Control (for Edge TTS) -->
    <div class="control-group" v-if="engine === 'edge'">
      <div class="control-header">
        <label class="control-label">Pitch Adjustment</label>
        <span class="control-value">{{ pitch > 0 ? '+' : '' }}{{ pitch }} Hz</span>
      </div>
      <input 
        type="range" 
        min="-50" 
        max="50" 
        step="1" 
        :value="pitch"
        @input="$emit('update:pitch', parseFloat($event.target.value))"
        class="custom-slider" 
      />
    </div>

    <!-- Temperature Control (for Vieneu) -->
    <div class="control-group" v-if="engine === 'vieneu'">
      <div class="control-header">
        <label class="control-label">Creativity / Temperature</label>
        <span class="control-value">{{ temperature }}</span>
      </div>
      <input 
        type="range" 
        min="0.2" 
        max="1.2" 
        step="0.05" 
        :value="temperature"
        @input="$emit('update:temperature', parseFloat($event.target.value))"
        class="custom-slider" 
      />
    </div>
  </div>
</template>

<script setup>
defineProps({
  speed: {
    type: Number,
    default: 1.0
  },
  pitch: {
    type: Number,
    default: 0
  },
  temperature: {
    type: Number,
    default: 0.8
  },
  engine: {
    type: String,
    default: 'vieneu'
  }
})

defineEmits(['update:speed', 'update:pitch', 'update:temperature'])
</script>

<style scoped>
.audio-controls {
  background-color: var(--color-canvas-white);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.control-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.control-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-slate-dark);
}

.control-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-electric-indigo);
}

.custom-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 6px;
  border-radius: 9999px;
  background: var(--color-border-light);
  outline: none;
}

.custom-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--color-electric-indigo);
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(79, 70, 229, 0.3);
  transition: transform 0.1s ease;
}

.custom-slider::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}

.preset-chips {
  display: flex;
  gap: 6px;
}

.chip {
  background-color: var(--color-panel-gray);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-sm);
  padding: 2px 8px;
  font-size: 11px;
  font-weight: 500;
  color: var(--color-slate-dark);
  cursor: pointer;
  transition: all 0.15s ease;
}

.chip:hover {
  border-color: var(--color-electric-indigo);
}

.chip.active {
  background-color: var(--color-electric-indigo);
  color: white;
  border-color: var(--color-electric-indigo);
}
</style>
