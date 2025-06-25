<template>
  <div class="qa-container">
    <el-card class="wood-card qa-main-card">
      <h2>🔧 家具维修智能助手</h2>
      <p class="subtitle">基于AI的专业维修知识问答系统</p>
      
      <!-- 快捷问题 -->
      <div class="quick-questions" v-if="!loading && !answer">
        <h4>💡 热门问题</h4>
        <div class="question-tags">
          <el-tag 
            v-for="q in quickQuestions" 
            :key="q"
            @click="askQuickQuestion(q)"
            class="quick-tag"
          >
            {{ q }}
          </el-tag>
        </div>
      </div>
      
      <!-- 问答区域 -->
      <div class="qa-input-section">
        <el-input
          v-model="question"
          placeholder="请输入您的维修问题，例如：如何更换iPhone电池？"
          style="margin-bottom: 18px;"
          clearable
          :disabled="loading"
          @keyup.enter="ask"
        />
        <el-button 
          class="wood-btn" 
          type="primary" 
          @click="ask" 
          style="margin-bottom: 18px;"
          :loading="loading"
          size="large"
        >
          {{ loading ? '分析中...' : '🔍 获取解答' }}
        </el-button>
      </div>
      
      <!-- 错误提示 -->
      <el-alert 
        v-if="error" 
        :title="error" 
        type="error" 
        :closable="true"
        @close="error = ''"
        style="margin-bottom: 16px;"
      />
      
      <!-- 回答区域 -->
      <div v-if="answer" class="qa-answer">
        <el-card class="answer-card">
          <template #header>
            <div class="answer-header">
              <span>🤖 AI维修助手</span>
              <el-rate v-model="rating" @change="submitRating" show-text />
            </div>
          </template>
          
          <div class="answer-content" v-html="formatAnswer(answer)"></div>
          
          <!-- 置信度 -->
          <div v-if="confidence" class="confidence-bar">
            <span>回答可信度：</span>
            <el-progress 
              :percentage="confidence * 100" 
              :color="getConfidenceColor(confidence)"
              :show-text="false"
              style="width: 200px; margin-left: 10px;"
            />
            <span>{{ Math.round(confidence * 100) }}%</span>
          </div>
        </el-card>
        
        <!-- 参考来源 -->
        <el-card v-if="sources && sources.length > 0" class="sources-card">
          <template #header>
            <span>📚 参考来源</span>
          </template>
          <ul class="sources-list">
            <li v-for="(source, index) in sources" :key="index">
              <el-link type="primary" :href="source" target="_blank">
                {{ source }}
              </el-link>
            </li>
          </ul>
        </el-card>
        
        <!-- 相关问题 -->
        <el-card v-if="relatedQuestions && relatedQuestions.length > 0" class="related-card">
          <template #header>
            <span>🔗 相关问题</span>
          </template>
          <div class="related-questions">
            <el-tag 
              v-for="q in relatedQuestions" 
              :key="q"
              @click="askRelatedQuestion(q)"
              class="related-tag"
              type="info"
            >
              {{ q }}
            </el-tag>
          </div>
        </el-card>
      </div>
      
      <!-- 对话历史 -->
      <div class="chat-history" v-if="chatHistory.length > 0">
        <el-divider>
          <span>📝 对话历史</span>
          <el-button @click="clearHistory" size="small" text type="danger">
            清空历史
          </el-button>
        </el-divider>
        
        <div class="history-item" v-for="(item, index) in chatHistory.slice(-3)" :key="index">
          <div class="history-question">
            <strong>Q: </strong>{{ item.question }}
          </div>
          <div class="history-answer">
            <strong>A: </strong>{{ item.answer.substring(0, 100) }}...
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { askQuestion } from '../services/api'
import type { QAResponse } from '../services/api'

const question = ref('')
const answer = ref('')
const sources = ref<string[]>([])
const relatedQuestions = ref<string[]>([])
const confidence = ref(0)
const loading = ref(false)
const error = ref('')
const rating = ref(0)
const chatHistory = ref<any[]>([])

const quickQuestions = ref([
  '如何更换手机电池？',
  '屏幕破裂怎么修复？',
  '充电口坏了怎么办？',
  '摄像头模糊如何处理？',
  '扬声器没声音怎么修？'
])

function formatAnswer(text: string): string {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/📋|🔧|🛠️|⚠️|💡/g, '<span class="emoji">$&</span>')
    .replace(/\n/g, '<br>')
}

function getConfidenceColor(conf: number): string {
  if (conf > 0.7) return '#67c23a'
  if (conf > 0.5) return '#e6a23c'
  return '#f56c6c'
}

async function ask() {
  if (!question.value.trim()) {
    error.value = '请输入问题'
    return
  }
  
  loading.value = true
  error.value = ''
  answer.value = ''
  sources.value = []
  relatedQuestions.value = []
  confidence.value = 0
  
  try {
    const response: QAResponse = await askQuestion(question.value)
    answer.value = response.answer
    sources.value = response.sources || []
    relatedQuestions.value = response.related_questions || []
    confidence.value = response.confidence || 0
    
    // 添加到对话历史
    chatHistory.value.push({
      question: question.value,
      answer: response.answer,
      timestamp: new Date().toLocaleString()
    })
    
    // 清空输入
    question.value = ''
  } catch (err: any) {
    error.value = err.message || '请求失败，请检查后端服务是否正常运行'
  } finally {
    loading.value = false
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

function submitRating(rate: number) {
  console.log('用户评分:', rate)
  // 这里可以发送评分到后端
}

function clearHistory() {
  chatHistory.value = []
}

onMounted(() => {
  // 加载对话历史
  // 可以从后端API获取
})
</script>

<style scoped>
.qa-container {
  display: flex;
  justify-content: center;
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f1eb 0%, #e8dcc0 100%);
}

.qa-main-card {
  width: 100%;
  max-width: 800px;
  border-radius: 15px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.subtitle {
  color: #8b7355;
  margin-bottom: 30px;
  text-align: center;
}

.quick-questions {
  margin-bottom: 30px;
  padding: 20px;
  background: #faf8f4;
  border-radius: 10px;
}

.question-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.quick-tag {
  cursor: pointer;
  transition: all 0.3s;
}

.quick-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.qa-input-section {
  margin-bottom: 20px;
}

.answer-card {
  margin-bottom: 20px;
}

.answer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.answer-content {
  line-height: 1.8;
  font-size: 16px;
}

.answer-content .emoji {
  font-size: 1.2em;
  margin-right: 5px;
}

.confidence-bar {
  display: flex;
  align-items: center;
  margin-top: 15px;
  font-size: 14px;
  color: #666;
}

.sources-card, .related-card {
  margin-bottom: 20px;
}

.sources-list {
  list-style: none;
  padding: 0;
}

.sources-list li {
  margin-bottom: 8px;
}

.related-questions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.related-tag {
  cursor: pointer;
  transition: all 0.3s;
}

.related-tag:hover {
  transform: scale(1.05);
}

.chat-history {
  margin-top: 30px;
}

.history-item {
  margin-bottom: 15px;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 8px;
  border-left: 4px solid #8B7355;
}

.history-question {
  margin-bottom: 8px;
  color: #333;
}

.history-answer {
  color: #666;
  font-size: 14px;
}

.wood-btn {
  background: linear-gradient(135deg, #8B7355 0%, #A0845C 100%);
  border: none;
  border-radius: 25px;
  padding: 12px 30px;
  font-weight: bold;
  transition: all 0.3s;
}

.wood-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 115, 85, 0.4);
}
</style>