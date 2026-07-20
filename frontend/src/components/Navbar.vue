<template>
  <header class="navbar">
    <div class="navbar-container">
      <div class="brand">
        <div class="brand-text">
          <span class="app-title">TellMe <span class="accent">TTS</span></span>
          <span class="app-badge">Vieneu Engine v3</span>
        </div>
      </div>

      <div class="navbar-actions">
        <div class="status-indicator" :class="{ online: isBackendOnline }">
          <span class="dot"></span>
          <span class="status-text">{{ isBackendOnline ? 'Backend Ready' : 'Connecting...' }}</span>
        </div>

        <button class="btn-secondary" @click="$emit('open-history')">
          History
          <span class="history-count" v-if="historyCount > 0">{{ historyCount }}</span>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
defineProps({
  isBackendOnline: {
    type: Boolean,
    default: true
  },
  historyCount: {
    type: Number,
    default: 0
  }
})

defineEmits(['open-history'])
</script>

<style scoped>
.navbar {
  background-color: var(--color-canvas-white);
  border-bottom: 1px solid var(--color-border-light);
  position: sticky;
  top: 0;
  z-index: 40;
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.app-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-slate-dark);
  letter-spacing: -0.01em;
}

.accent {
  color: var(--color-electric-indigo);
}

.app-badge {
  font-size: 11px;
  font-weight: 500;
  color: var(--color-muted-slate);
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-muted-slate);
  background-color: var(--color-panel-gray);
  padding: 4px 10px;
  border-radius: var(--radius-full);
  border: 1px solid var(--color-border-light);
}

.status-indicator .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ef4444;
}

.status-indicator.online .dot {
  background-color: #10b981;
}

.btn-secondary {
  background-color: var(--color-panel-gray);
  color: var(--color-slate-dark);
  border: 1px solid var(--color-border-light);
  padding: 8px 14px;
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.15s ease;
}

.btn-secondary:hover {
  background-color: var(--color-canvas-white);
  border-color: var(--color-border-hover);
}

.history-count {
  background-color: var(--color-electric-indigo);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: var(--radius-full);
}
</style>
