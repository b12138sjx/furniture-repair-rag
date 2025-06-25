<template>
  <div class="qa-container">
    <!-- 顶部工具栏 -->
    <div class="qa-header">
      <div class="header-left">
        <h2>🔧 智能问答</h2>
        <div class="header-stats">
          <el-tag size="small" effect="light" type="success">
            <el-icon><Document /></el-icon>
            {{ knowledgeInfo.total_documents }} 篇文档
          </el-tag>
          <el-tag size="small" effect="light" type="info">
            <el-icon><Tools /></el-icon>
            {{ knowledgeInfo.total_tools }} 种工具
          </el-tag>
        </div>
      </div>
      <div class="header-right">
        <!-- 回答模式选择 -->
        <div class="control-group">
          <label class="control-label">回答模式</label>
          <el-select 
            v-model="answerMode" 
            class="control-select"
            @change="onAnswerModeChange"
          >
            <el-option value="auto" label="智能模式">
              <div class="mode-option">
                <span class="mode-name">🧠 智能模式</span>
                <span class="mode-desc">AI + 知识库</span>
              </div>
            </el-option>
            <el-option value="llm_only" label="大模型模式">
              <div class="mode-option">
                <span class="mode-name">🤖 大模型模式</span>
                <span class="mode-desc">仅使用AI回答</span>
              </div>
            </el-option>
            <el-option value="kb_only" label="知识库模式">
              <div class="mode-option">
                <span class="mode-name">📚 知识库模式</span>
                <span class="mode-desc">仅从文档检索</span>
              </div>
            </el-option>
          </el-select>
        </div>
        
        <!-- 模型选择器 -->
        <div class="control-group" v-if="answerMode !== 'kb_only'">
          <label class="control-label">AI模型</label>
          <el-select 
            v-model="selectedModel" 
            placeholder="选择AI模型"
            class="control-select"
            @change="onModelChange"
          >
            <el-option
              v-for="model in availableModels"
              :key="model.id"
              :label="model.name"
              :value="model.id"
              :disabled="!model.available"
            >
              <div class="model-option">
                <div class="model-info-line">
                  <span class="model-name">{{ model.name }}</span>
                  <el-tag size="small" :type="model.available ? 'success' : 'danger'">
                    {{ model.available ? '可用' : '不可用' }}
                  </el-tag>
                </div>
                <span class="model-provider">{{ model.provider }}</span>
              </div>
            </el-option>
          </el-select>
        </div>
        
        <!-- 高级设置 -->
        <el-popover placement="bottom-end" trigger="click" width="320" :show-arrow="false">
          <template #reference>
            <el-button class="settings-btn" circle>
              <el-icon><Setting /></el-icon>
            </el-button>
          </template>
          <div class="advanced-settings">
            <div class="settings-header">
              <h4>🎛️ 参数设置</h4>
              <p>调整回答行为和质量</p>
            </div>
            
            <div class="setting-item" v-if="answerMode !== 'kb_only'">
              <div class="setting-label">
                <label>创造性 (Temperature)</label>
                <span class="setting-value">{{ temperature }}</span>
              </div>
              <el-slider 
                v-model="temperature" 
                :min="0" 
                :max="1" 
                :step="0.1"
                show-input
                :show-input-controls="false"
                size="small"
              />
              <small class="setting-hint">
                <el-icon><InfoFilled /></el-icon>
                较低值更保守准确，较高值更有创意
              </small>
            </div>
            
            <div class="setting-item" v-if="answerMode !== 'llm_only'">
              <div class="setting-label">
                <label>检索数量</label>
                <span class="setting-value">{{ contextSize }}</span>
              </div>
              <el-input-number 
                v-model="contextSize" 
                :min="1" 
                :max="10" 
                size="small"
                controls-position="right"
                style="width: 100%"
              />
              <small class="setting-hint">
                <el-icon><InfoFilled /></el-icon>
                从知识库检索的文档数量
              </small>
            </div>
          </div>
        </el-popover>
      </div>
    </div>
    
    <!-- 对话区域 -->
    <div class="chat-area">
      <div class="chat-messages" ref="messagesContainer">
        <!-- 欢迎消息 -->
        <div v-if="chatHistory.length === 0" class="welcome-section">
          <div class="welcome-card">
            <div class="welcome-header">
              <div class="welcome-avatar">
                <div class="avatar-icon">🔧</div>
              </div>
              <div class="welcome-text">
                <h3>你好！我是维修助手</h3>
                <div class="current-mode">
                  <span>当前模式：</span>
                  <el-tag :type="getModeTagType(answerMode)" size="small">
                    {{ getModeDisplayName(answerMode) }}
                  </el-tag>
                </div>
              </div>
            </div>
            
            <div class="welcome-content">
              <p class="welcome-description">我可以帮你解决各种设备维修问题，提供专业的维修指导</p>
              
              <div class="example-questions-section">
                <h4>💡 试试这些问题</h4>
                <div class="example-questions">
                  <div 
                    v-for="q in quickQuestions" 
                    :key="q"
                    @click="askQuickQuestion(q)"
                    class="example-question"
                  >
                    <el-icon><ChatDotRound /></el-icon>
                    {{ q }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 对话历史 -->
        <div v-for="(item, index) in chatHistory" :key="index" class="message-group">
          <!-- 用户消息 -->
          <div class="message user-message">
            <div class="message-content user-content">
              <div class="message-text">{{ item.question }}</div>
            </div>
            <div class="message-avatar user-avatar">
              <div class="avatar-text">你</div>
            </div>
          </div>
          
          <!-- AI回复 -->
          <div class="message ai-message">
            <div class="message-avatar ai-avatar">
              <div class="avatar-icon">🔧</div>
            </div>
            <div class="message-content ai-content">
              <div class="message-text" v-html="formatAnswer(item.answer)"></div>
              
              <!-- 回答元信息 -->
              <div class="message-actions">
                <div class="message-meta">
                  <div class="answer-info">
                    <el-tag size="small" :type="getModeTagType(item.answer_mode)" effect="light">
                      {{ getModeDisplayName(item.answer_mode) }}
                    </el-tag>
                    <el-tag v-if="item.model_used && item.answer_mode !== 'kb_only'" size="small" effect="plain">
                      {{ item.model_used }}
                    </el-tag>
                    <span class="confidence" v-if="item.confidence">
                      <el-icon><SuccessFilled /></el-icon>
                      {{ Math.round(item.confidence * 100) }}%
                    </span>
                    <span class="processing-time" v-if="item.processing_time">
                      {{ item.processing_time }}s
                    </span>
                  </div>
                </div>
                <div class="action-buttons">
                  <el-button size="small" text @click="copyAnswer(item.answer)">
                    <el-icon><DocumentCopy /></el-icon>
                    复制
                  </el-button>
                  <el-button size="small" text @click="regenerateAnswer(item.question)">
                    <el-icon><Refresh /></el-icon>
                    重新生成
                  </el-button>
                  <el-rate 
                    v-model="item.rating" 
                    @change="submitRating(item, $event)"
                    size="small"
                    :colors="['#f7ba2a', '#f7ba2a', '#f7ba2a']"
                    show-text
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 加载状态 -->
        <div v-if="loading" class="message ai-message loading-message">
          <div class="message-avatar ai-avatar">
            <div class="avatar-icon loading-avatar">🔧</div>
          </div>
          <div class="message-content ai-content">
            <div class="typing-indicator">
              <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <p class="thinking-text">{{ getLoadingText() }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 底部输入区域 -->
    <div class="input-area">
      <div class="input-wrapper">
        <div class="input-box">
          <el-input
            v-model="question"
            placeholder="描述你遇到的问题，比如：iPhone电池如何更换？"
            :disabled="loading"
            @keyup.enter.exact="ask"
            @keyup.ctrl.enter="addNewline"
            class="chat-input-field"
            type="textarea"
            :autosize="{ minRows: 1, maxRows: 4 }"
            resize="none"
          />
          <div class="input-actions">
            <div class="input-hints">
              <span class="hint-text">Enter 发送 • Ctrl+Enter 换行</span>
            </div>
            <el-button 
              type="primary" 
              @click="ask" 
              :loading="loading"
              :disabled="!question.trim()"
              class="send-button"
              circle
            >
              <el-icon><Promotion /></el-icon>
            </el-button>
          </div>
        </div>
      </div>
      
      <!-- 错误提示 -->
      <transition name="slide-up">
        <div v-if="error" class="error-message">
          <el-alert 
            :title="error" 
            type="error" 
            :closable="true" 
            @close="error = ''"
            show-icon
          />
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { askQuestionV2, getKnowledgeStats, getAvailableModels } from '../services/api'
import type { QAResponse, ModelInfo, QARequest } from '../services/api'

const question = ref('')
const loading = ref(false)
const error = ref('')
const messagesContainer = ref<HTMLElement>()

// 回答模式
const answerMode = ref<'auto' | 'llm_only' | 'kb_only'>('auto')

// 模型相关
const availableModels = ref<ModelInfo[]>([])
const selectedModel = ref('gpt-3.5-turbo')
const temperature = ref(0.7)
const contextSize = ref(3)

const chatHistory = ref<any[]>([])
const knowledgeInfo = ref({
  total_documents: 0,
  total_tools: 0
})

const quickQuestions = ref([
  '如何更换iPhone电池？',
  '笔记本屏幕闪烁怎么办？',
  '手机充电慢的原因？',
  '电脑风扇噪音大如何处理？',
  '显示器花屏如何修复？'
])

function getModeDisplayName(mode: string): string {
  const modeMap = {
    'auto': '智能模式',
    'llm_only': '大模型模式', 
    'kb_only': '知识库模式'
  }
  return modeMap[mode] || mode
}

function getModeTagType(mode: string): string {
  const typeMap = {
    'auto': 'primary',
    'llm_only': 'success',
    'kb_only': 'warning'
  }
  return typeMap[mode] || 'info'
}

function getLoadingText(): string {
  const texts = {
    'auto': '正在智能分析问题...',
    'llm_only': `${selectedModel.value} 正在思考...`,
    'kb_only': '正在检索知识库...'
  }
  return texts[answerMode.value] || '正在处理...'
}

function getSendButtonTooltip(): string {
  return `使用${getModeDisplayName(answerMode.value)}回答`
}

function onAnswerModeChange(mode: string) {
  console.log('切换回答模式:', mode)
}

function onModelChange(modelId: string) {
  console.log('切换模型:', modelId)
}

async function ask() {
  if (!question.value.trim()) {
    error.value = '请输入问题'
    return
  }
  
  loading.value = true
  error.value = ''
  
  // 添加到对话历史
  const newChat = {
    question: question.value,
    answer: '',
    timestamp: new Date().toLocaleString(),
    rating: 0,
    model_used: selectedModel.value,
    answer_mode: answerMode.value,
    confidence: 0,
    processing_time: 0
  }
  chatHistory.value.push(newChat)
  
  const currentQuestion = question.value
  question.value = '' // 清空输入框
  
  // 滚动到底部
  await nextTick()
  scrollToBottom()
  
  try {
    const request: QARequest = {
      query: currentQuestion,
      answer_mode: answerMode.value,
      model: selectedModel.value,
      temperature: temperature.value,
      context_size: contextSize.value
    }
    
    const response: QAResponse = await askQuestionV2(request)
    
    newChat.answer = response.answer
    newChat.model_used = response.model_used || selectedModel.value
    newChat.answer_mode = response.answer_mode
    newChat.confidence = response.confidence || 0
    newChat.processing_time = response.processing_time || 0
    
  } catch (err: any) {
    error.value = err.message || '请求失败，请检查后端服务是否正常运行'
    // 移除失败的对话
    chatHistory.value.pop()
  } finally {
    loading.value = false
    await nextTick()
    scrollToBottom()
  }
}

function askQuickQuestion(q: string) {
  question.value = q
  ask()
}

function askRelatedQuestion(q: string) {
  question.value = q
  ask()
}

function submitRating(item: any, rate: number) {
  console.log('用户评分:', rate)
  // 这里可以发送评分到后端
}

function clearHistory() {
  chatHistory.value = []
}

async function loadKnowledgeInfo() {
  try {
    const stats = await getKnowledgeStats()
    knowledgeInfo.value = {
      total_documents: stats.total_documents || 0,
      total_tools: stats.total_tools || 0
    }
  } catch (err) {
    console.warn('获取知识库信息失败:', err)
  }
}

async function loadAvailableModels() {
  try {
    const models = await getAvailableModels()
    availableModels.value = models
  } catch (err) {
    console.warn('获取可用模型失败:', err)
  }
}

onMounted(() => {
  loadAvailableModels()
  loadKnowledgeInfo()
})

function copyAnswer(answer: string) {
  navigator.clipboard.writeText(answer).then(() => {
    ElMessage.success('已复制到剪贴板')
  })
}

function regenerateAnswer(question: string) {
  this.question = question
  ask()
}

function addNewline() {
  question.value += '\n'
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

function formatAnswer(text: string): string {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/📋|🔧|🛠️|⚠️|💡/g, '<span class="emoji">$&</span>')
    .replace(/\n/g, '<br>')
}
</script>

<style scoped>
.qa-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #ffffff;
}

/* 顶部工具栏 */
.qa-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.header-left h2 {
  margin: 0 0 8px 0;
  color: #8b7355;
  font-size: 20px;
  font-weight: 600;
}

.header-stats {
  display: flex;
  gap: 8px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.control-group {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.control-label {
  font-size: 12px;
  color: #8b7355;
  margin-bottom: 4px;
  font-weight: 500;
}

.control-select {
  width: 160px;
}

.settings-btn {
  background: rgba(139, 115, 85, 0.1);
  border-color: rgba(139, 115, 85, 0.2);
  color: #8b7355;
}

.settings-btn:hover {
  background: rgba(139, 115, 85, 0.2);
  transform: rotate(90deg);
}

/* 对话区域 */
.chat-area {
  flex: 1;
  overflow: hidden;
  background: #f8f9fa;
}

.chat-messages {
  height: 100%;
  padding: 24px;
  overflow-y: auto;
  scroll-behavior: smooth;
}

/* 欢迎区域 */
.welcome-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 500px;
}

.welcome-card {
  background: white;
  padding: 48px;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(139, 115, 85, 0.12);
  border: 1px solid #e4d4c8;
  max-width: 800px;
  width: 100%;
  text-align: center;
}

/* 消息样式 */
.message-group {
  margin-bottom: 32px;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.message {
  display: flex;
  margin-bottom: 24px;
  gap: 16px;
}

.user-message {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 14px;
  font-weight: 600;
}

.user-avatar {
  background: linear-gradient(135deg, #b08968, #a0845c);
  color: white;
}

.ai-avatar {
  background: linear-gradient(135deg, #8b7355, #a0845c);
  color: white;
}

.message-content {
  flex: 1;
  max-width: calc(100% - 120px);
}

.user-content {
  display: flex;
  justify-content: flex-end;
}

.message-text {
  padding: 16px 20px;
  border-radius: 16px;
  line-height: 1.6;
  font-size: 15px;
  word-wrap: break-word;
}

.user-message .message-text {
  background: linear-gradient(135deg, #b08968, #a0845c);
  color: white;
  border-bottom-right-radius: 6px;
  margin-left: auto;
  max-width: 80%;
}

.ai-message .message-text {
  background: white;
  color: #1f2937;
  border: 1px solid #e5e7eb;
  border-bottom-left-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 底部输入区域 */
.input-area {
  padding: 20px 24px;
  background: #ffffff;
  border-top: 1px solid #e5e7eb;
}

.input-wrapper {
  max-width: 900px;
  margin: 0 auto;
}

.input-box {
  position: relative;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 16px;
  transition: all 0.2s ease;
  overflow: hidden;
}

.input-box:focus-within {
  border-color: #8b7355;
  box-shadow: 0 0 0 3px rgba(139, 115, 85, 0.1);
}

.chat-input-field {
  border: none;
  padding: 16px 20px;
}

.chat-input-field :deep(.el-textarea__inner) {
  border: none;
  box-shadow: none;
  padding: 0;
  font-size: 15px;
  line-height: 1.5;
  resize: none;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background: #f8f9fa;
  border-top: 1px solid #f3f4f6;
}

.hint-text {
  font-size: 12px;
  color: #9ca3af;
}

.send-button {
  background: linear-gradient(135deg, #8b7355, #a0845c);
  border: none;
  width: 36px;
  height: 36px;
}

.send-button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(139, 115, 85, 0.3);
}

.error-message {
  margin-top: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .qa-header {
    padding: 12px 16px;
    flex-direction: column;
    gap: 12px;
  }
  
  .header-right {
    width: 100%;
    justify-content: space-between;
    gap: 12px;
  }
  
  .chat-messages {
    padding: 16px;
  }
  
  .input-area {
    padding: 16px;
  }
  
  .welcome-card {
    padding: 32px 24px;
  }
  
  .message-content {
    max-width: calc(100% - 60px);
  }
}

/* 其他样式保持不变 */
/* ...existing code... */
</style>