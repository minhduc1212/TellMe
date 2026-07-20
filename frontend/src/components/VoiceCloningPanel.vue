<template>
  <div class="voice-cloning-panel">
    <div class="cloning-header">
      <div class="header-left">
        <span class="cloning-title">Sao chép giọng mẫu (Zero-shot Voice Cloning)</span>
      </div>
      <label class="toggle-switch">
        <input 
          type="checkbox" 
          :checked="isCloningEnabled" 
          @change="$emit('update:isCloningEnabled', $event.target.checked)" 
        />
        <span class="slider"></span>
      </label>
    </div>

    <div class="cloning-body" v-if="isCloningEnabled">
      <p class="cloning-desc">
        Tải lên clip âm thanh mẫu (3–10 giây) hoặc chọn mẫu có sẵn để sao chép giọng nói tức thì bằng Vieneu v3.
      </p>

      <!-- Drag & Drop Audio Upload -->
      <div 
        class="upload-dropzone" 
        :class="{ dragging: isDragging, 'has-file': uploadedFile }"
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="handleDrop"
        @click="triggerFileInput"
      >
        <input 
          type="file" 
          ref="fileInputRef" 
          accept="audio/*" 
          class="hidden-file-input" 
          @change="handleFileSelect" 
        />

        <div v-if="!uploadedFile && !isUploading" class="upload-placeholder">
          <span class="upload-text">Kéo thả file âm thanh mẫu (.wav, .mp3) hoặc <span class="browse-link">chọn file</span></span>
          <span class="upload-hint">Khuyên dùng: clip 5 giây phát âm rõ tiếng Việt</span>
        </div>

        <div v-else-if="isUploading" class="upload-loading">
          <div class="spinner"></div>
          <span>Đang tải lên và phân tích giọng mẫu...</span>
        </div>

        <div v-else class="upload-success">
          <div class="file-info">
            <span class="file-name">{{ uploadedFile.name }}</span>
            <span class="file-status">Đã sẵn sàng sao chép giọng</span>
          </div>
          <button class="remove-btn" @click.stop="removeFile">Xóa mẫu</button>
        </div>
      </div>

      <!-- Sample Audio Reference Shortcuts -->
      <div class="samples-row">
        <span class="samples-label">Mẫu sẵn:</span>
        <button 
          class="sample-chip" 
          @click="selectSample('output.wav')"
        >
          Mẫu output.wav
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  isCloningEnabled: {
    type: Boolean,
    default: false
  },
  refAudioPath: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['update:isCloningEnabled', 'update:refAudioPath'])

const fileInputRef = ref(null)
const isDragging = ref(false)
const isUploading = ref(false)
const uploadedFile = ref(null)

function triggerFileInput() {
  fileInputRef.value?.click()
}

function handleFileSelect(e) {
  const files = e.target.files
  if (files && files.length > 0) {
    uploadAudioFile(files[0])
  }
}

function handleDrop(e) {
  isDragging.value = false
  const files = e.dataTransfer.files
  if (files && files.length > 0) {
    uploadAudioFile(files[0])
  }
}

async function uploadAudioFile(file) {
  isUploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)

    const res = await fetch('http://127.0.0.1:8000/api/audio/upload-ref', {
      method: 'POST',
      body: formData
    })

    if (!res.ok) throw new Error('Upload reference audio failed')
    const data = await res.json()
    
    uploadedFile.value = {
      name: file.name,
      path: data.filepath,
      url: data.url
    }

    emit('update:refAudioPath', data.filepath)
  } catch (err) {
    alert('Lỗi tải lên audio mẫu: ' + err.message)
  } finally {
    isUploading.value = false
  }
}

function selectSample(samplePath) {
  uploadedFile.value = {
    name: 'Sample Output Wav',
    path: samplePath
  }
  emit('update:refAudioPath', samplePath)
}

function removeFile() {
  uploadedFile.value = null
  emit('update:refAudioPath', null)
  if (fileInputRef.value) fileInputRef.value.value = ''
}
</script>

<style scoped>
.voice-cloning-panel {
  background-color: var(--color-canvas-white);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cloning-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.cloning-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-slate-dark);
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 22px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: var(--color-border-hover);
  transition: .2s;
  border-radius: 9999px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .2s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: var(--color-electric-indigo);
}

input:checked + .slider:before {
  transform: translateX(18px);
}

.cloning-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-top: 8px;
  border-top: 1px dashed var(--color-border-light);
}

.cloning-desc {
  font-size: 12px;
  color: var(--color-muted-slate);
}

.upload-dropzone {
  border: 2px dashed var(--color-border-hover);
  border-radius: var(--radius-md);
  padding: 16px;
  text-align: center;
  cursor: pointer;
  background-color: var(--color-panel-gray);
  transition: all 0.2s ease;
}

.upload-dropzone:hover, .upload-dropzone.dragging {
  border-color: var(--color-electric-indigo);
  background-color: rgba(79, 70, 229, 0.03);
}

.hidden-file-input {
  display: none;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  color: var(--color-muted-slate);
}

.upload-text {
  font-size: 13px;
  color: var(--color-slate-dark);
}

.browse-link {
  color: var(--color-electric-indigo);
  font-weight: 600;
  text-decoration: underline;
}

.upload-hint {
  font-size: 11px;
}

.upload-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 13px;
  color: var(--color-electric-indigo);
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid var(--color-border-hover);
  border-top-color: var(--color-electric-indigo);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.upload-success {
  display: flex;
  align-items: center;
  gap: 12px;
  text-align: left;
  justify-content: space-between;
}

.file-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.file-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-slate-dark);
}

.file-status {
  font-size: 11px;
  color: var(--color-cyan-signal);
}

.remove-btn {
  background-color: var(--color-panel-gray);
  border: 1px solid var(--color-border-light);
  font-size: 12px;
  font-weight: 500;
  color: var(--color-muted-slate);
  cursor: pointer;
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  transition: all 0.15s ease;
}

.remove-btn:hover {
  color: #ef4444;
  border-color: #ef4444;
}

.samples-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.samples-label {
  color: var(--color-muted-slate);
}

.sample-chip {
  background-color: var(--color-panel-gray);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-sm);
  padding: 4px 10px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.sample-chip:hover {
  border-color: var(--color-electric-indigo);
  color: var(--color-electric-indigo);
}
</style>
