<template>
  <div class="text-canvas-card">
    <!-- Quick Sample Prompts Bar -->
    <div class="sample-prompts-bar">
      <span class="bar-label">Mẫu văn bản:</span>
      <div class="prompt-chips">
        <button 
          v-for="sample in samples" 
          :key="sample.title" 
          class="prompt-chip"
          @click="$emit('update:text', sample.content)"
        >
          {{ sample.title }}
        </button>
      </div>
    </div>

    <!-- Text Input Area or Word Highlight Display -->
    <div class="editor-container">
      <!-- Standard Textarea when NOT playing with timestamps -->
      <textarea 
        v-if="!isPlayingWithWords"
        class="canvas-textarea" 
        :value="text"
        @input="$emit('update:text', $event.target.value)"
        placeholder="Nhập hoặc dán đoạn văn bản Tiếng Việt cần đọc tại đây..."
      ></textarea>

      <!-- Dynamic Word Highlight View during Playback -->
      <div v-else class="playback-highlight-view">
        <div class="highlight-words-wrapper">
          <span 
            v-for="(item, idx) in wordList" 
            :key="idx" 
            class="word-span"
            :class="{ active: idx === currentWordIndex }"
          >{{ item.word }} </span>
        </div>
        <div class="highlight-action-bar">
          <button class="edit-text-btn" @click="$emit('stop-highlight-view')">Sửa văn bản</button>
        </div>
      </div>
    </div>

    <!-- Footer Stats & Actions -->
    <div class="canvas-footer">
      <div class="stats">
        <span>{{ text.length }} ký tự</span>
        <span class="dot">•</span>
        <span>{{ wordCount }} từ</span>
      </div>

      <div class="actions">
        <button class="tool-btn" @click="$emit('update:text', '')" title="Xóa văn bản">
          Xóa
        </button>

        <button class="tool-btn" @click="copyText" title="Sao chép">
          {{ isCopied ? 'Đã chép!' : 'Sao chép' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  text: {
    type: String,
    default: ''
  },
  isPlayingWithWords: {
    type: Boolean,
    default: false
  },
  wordList: {
    type: Array,
    default: () => []
  },
  currentWordIndex: {
    type: Number,
    default: -1
  }
})

const emit = defineEmits(['update:text', 'stop-highlight-view'])

const isCopied = ref(false)

const wordCount = computed(() => {
  if (!props.text) return 0
  const trimmed = props.text.trim()
  return trimmed ? trimmed.split(/\s+/).length : 0
})

const samples = [
  {
    title: 'Truyện cổ tích',
    content: '"Thọc và kéo," bà lão đang nói, "đó là cách của Nữ hoàng, cũng giống như chính các vị thần vậy." Mụ nghiêng người sang một bên và nhổ bọt, rồi đưa một mảnh vải bẩn lên đôi môi nhăn nheo.'
  },
  {
    title: 'Tin tức',
    content: 'Chào mừng quý vị và các bạn đến với bản tin công nghệ hàng ngày. Công nghệ trí tuệ nhân tạo đang giúp việc chuyển đổi văn bản thành giọng nói trở nên mượt mà và tự nhiên hơn bao giờ hết.'
  },
  {
    title: 'Hội thoại',
    content: 'Xin chào Đức! Hôm nay bạn thế nào? Hãy thử nghe giọng đọc tiếng Việt cực kỳ mượt mà từ hệ thống TellMe TTS xem sao nhé!'
  }
]

function copyText() {
  if (!props.text) return
  navigator.clipboard.writeText(props.text)
  isCopied.value = true
  setTimeout(() => {
    isCopied.value = false
  }, 2000)
}
</script>

<style scoped>
.text-canvas-card {
  background-color: var(--color-canvas-white);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.sample-prompts-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  background-color: var(--color-panel-gray);
  border-bottom: 1px solid var(--color-border-light);
  max-width: 100%;
  box-sizing: border-box;
}

.bar-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-muted-slate);
  white-space: nowrap;
}

.prompt-chips {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.prompt-chip {
  background-color: var(--color-canvas-white);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-full);
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-slate-dark);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
}

.prompt-chip:hover {
  border-color: var(--color-electric-indigo);
  color: var(--color-electric-indigo);
}

.editor-container {
  padding: 24px 32px;
  min-height: 220px;
  display: flex;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.canvas-textarea {
  width: 100%;
  max-width: 100%;
  border: none;
  outline: none;
  font-family: var(--font-inter);
  font-size: 18px;
  line-height: 1.75;
  color: var(--color-slate-dark);
  resize: vertical;
  background: transparent;
  min-height: 180px;
  box-sizing: border-box;
  word-break: break-word;
  white-space: pre-wrap;
}

.canvas-textarea::placeholder {
  color: var(--color-muted-slate);
  opacity: 0.6;
}

.playback-highlight-view {
  font-family: var(--font-inter);
  font-size: 18px;
  line-height: 1.8;
  color: var(--color-slate-dark);
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  word-break: break-word;
  white-space: normal;
  overflow-wrap: break-word;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.highlight-words-wrapper {
  width: 100%;
  max-width: 100%;
  word-break: break-word;
  white-space: normal;
  overflow-wrap: break-word;
  line-height: 1.8;
}

.word-span {
  display: inline-block;
  padding: 2px 4px;
  border-radius: var(--radius-sm);
  transition: background-color 0.12s ease, color 0.12s ease;
  margin-right: 2px;
  margin-bottom: 4px;
}

.word-span.active {
  background-color: var(--color-cyan-light);
  color: var(--color-slate-dark);
  font-weight: 600;
}

.highlight-action-bar {
  display: flex;
  justify-content: flex-end;
}

.edit-text-btn {
  background-color: var(--color-panel-gray);
  border: 1px solid var(--color-border-light);
  padding: 6px 14px;
  border-radius: var(--radius-md);
  font-size: 12px;
  font-weight: 600;
  color: var(--color-slate-dark);
  cursor: pointer;
  transition: all 0.15s ease;
}

.edit-text-btn:hover {
  border-color: var(--color-electric-indigo);
  color: var(--color-electric-indigo);
}

.canvas-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  border-top: 1px solid var(--color-border-light);
  background-color: var(--color-canvas-white);
  max-width: 100%;
  box-sizing: border-box;
}

.stats {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-muted-slate);
}

.dot {
  font-size: 10px;
}

.actions {
  display: flex;
  gap: 8px;
}

.tool-btn {
  background: var(--color-panel-gray);
  border: 1px solid var(--color-border-light);
  font-size: 13px;
  font-weight: 500;
  color: var(--color-slate-dark);
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: var(--radius-md);
  transition: all 0.15s ease;
}

.tool-btn:hover {
  border-color: var(--color-electric-indigo);
  color: var(--color-electric-indigo);
}
</style>
