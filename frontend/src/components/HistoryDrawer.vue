<template>
  <div class="drawer-overlay" v-if="isOpen" @click.self="$emit('close')">
    <div class="drawer-content">
      <div class="drawer-header">
        <div class="drawer-title">
          Lịch sử phát audio
        </div>
        <button class="close-btn" @click="$emit('close')">Đóng</button>
      </div>

      <div class="drawer-body">
        <div v-if="history.length === 0" class="empty-state">
          <span>Chưa có file audio nào được tạo.</span>
        </div>

        <div v-else class="history-list">
          <div 
            v-for="item in history" 
            :key="item.id" 
            class="history-item"
          >
            <div class="item-main">
              <span class="item-text">"{{ item.text }}"</span>
              <div class="item-tags">
                <span class="tag engine-tag">{{ item.engine }}</span>
                <span class="tag voice-tag">{{ item.voice }}</span>
                <span class="tag duration-tag">{{ item.duration }}s</span>
              </div>
            </div>

            <div class="item-actions">
              <button 
                class="action-btn play-btn" 
                @click="$emit('play-item', item)"
                title="Phát audio"
              >
                Phát
              </button>
              <a 
                :href="'http://127.0.0.1:8000' + item.url" 
                download 
                class="action-btn download-btn"
                title="Tải về"
              >
                Tải
              </a>
              <button 
                class="action-btn delete-btn" 
                @click="$emit('delete-item', item.id)"
                title="Xóa"
              >
                Xóa
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  history: {
    type: Array,
    default: () => []
  }
})

defineEmits(['close', 'play-item', 'delete-item'])
</script>

<style scoped>
.drawer-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(2px);
  z-index: 100;
  display: flex;
  justify-content: flex-end;
}

.drawer-content {
  width: 420px;
  max-width: 90vw;
  height: 100%;
  background-color: var(--color-canvas-white);
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
}

.drawer-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.drawer-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-slate-dark);
}

.close-btn {
  background: var(--color-panel-gray);
  border: 1px solid var(--color-border-light);
  padding: 4px 10px;
  border-radius: var(--radius-md);
  font-size: 12px;
  font-weight: 500;
  color: var(--color-slate-dark);
  cursor: pointer;
}

.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
  color: var(--color-muted-slate);
  font-size: 14px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-item {
  background-color: var(--color-panel-gray);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  padding: 12px;
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
}

.item-main {
  display: flex;
  flex-direction: column;
  gap: 6px;
  overflow: hidden;
}

.item-text {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-slate-dark);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-tags {
  display: flex;
  gap: 6px;
}

.tag {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  background-color: var(--color-canvas-white);
  border: 1px solid var(--color-border-light);
  color: var(--color-muted-slate);
}

.item-actions {
  display: flex;
  gap: 6px;
}

.action-btn {
  background-color: var(--color-canvas-white);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-sm);
  padding: 4px 8px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  color: var(--color-slate-dark);
}

.action-btn:hover {
  border-color: var(--color-electric-indigo);
  color: var(--color-electric-indigo);
}

.delete-btn:hover {
  border-color: #ef4444;
  color: #ef4444;
}
</style>
