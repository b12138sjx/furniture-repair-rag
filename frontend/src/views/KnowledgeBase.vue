<template>
  <el-card class="wood-card knowledge-container">
    <h2>📚 知识库管理</h2>
    <p style="margin: 24px 0 32px 0; color: #7c5b3a;">
      管理你的维修知识库：上传文档或采集在线资源，构建个性化的维修指南库。
    </p>
    
    <!-- 功能选项卡 -->
    <el-tabs v-model="activeTab" class="knowledge-tabs">
      <!-- 文件上传 -->
      <el-tab-pane label="📄 文档上传" name="upload">
        <div class="tab-content">
          <div class="upload-section">
            <el-upload
              ref="uploadRef"
              :before-upload="handleUpload"
              :show-file-list="false"
              accept=".pdf,.txt,.md,.doc,.docx"
              drag
              class="upload-dragger"
            >
              <el-icon class="upload-icon"><Upload /></el-icon>
              <div class="upload-text">
                <p>将文件拖拽到此处，或<em>点击上传</em></p>
                <p class="upload-hint">支持 PDF、TXT、MD、DOC、DOCX 格式</p>
              </div>
            </el-upload>
            
            <el-button 
              class="wood-btn upload-btn" 
              type="primary" 
              :loading="uploading"
              @click="triggerUpload"
            >
              {{ uploading ? '上传中...' : '📂 选择文件上传' }}
            </el-button>
          </div>
        </div>
      </el-tab-pane>
      
      <!-- URL采集 -->
      <el-tab-pane label="🌐 在线采集" name="collect">
        <div class="tab-content">
          <div class="collect-section">
            <div class="collect-form">
              <el-input
                v-model="collectUrl"
                placeholder="请输入要采集的网页URL，如：https://zh.ifixit.com/Guide/xxx"
                class="url-input"
                :disabled="collecting"
              >
                <template #prepend>🔗 URL</template>
              </el-input>
              
              <el-button 
                class="wood-btn collect-btn" 
                type="primary" 
                @click="startCollect"
                :loading="collecting"
              >
                {{ collecting ? '采集中...' : '🚀 开始采集' }}
              </el-button>
            </div>
            
            <!-- 预设采集源 -->
            <div class="preset-sources">
              <h4>🔥 热门采集源</h4>
              <div class="source-tags">
                <el-tag 
                  v-for="source in presetSources" 
                  :key="source.url"
                  @click="usePresetSource(source.url)"
                  class="source-tag"
                  effect="plain"
                >
                  {{ source.name }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>
      
      <!-- 知识库状态 -->
      <el-tab-pane label="📊 库存状态" name="status">
        <div class="tab-content">
          <div class="status-section">
            <!-- 统计卡片 -->
            <div class="stats-grid">
              <div class="stat-card">
                <div class="stat-icon">📄</div>
                <div class="stat-info">
                  <div class="stat-number">{{ knowledgeStats.total_documents || 0 }}</div>
                  <div class="stat-label">总文档数</div>
                </div>
              </div>
              
              <div class="stat-card">
                <div class="stat-icon">📱</div>
                <div class="stat-info">
                  <div class="stat-number">{{ knowledgeStats.types?.phone_repair || 0 }}</div>
                  <div class="stat-label">手机维修</div>
                </div>
              </div>
              
              <div class="stat-card">
                <div class="stat-icon">🔧</div>
                <div class="stat-info">
                  <div class="stat-number">{{ knowledgeStats.total_tools || 0 }}</div>
                  <div class="stat-label">工具种类</div>
                </div>
              </div>
              
              <div class="stat-card">
                <div class="stat-icon">⚠️</div>
                <div class="stat-info">
                  <div class="stat-number">{{ knowledgeStats.total_warnings || 0 }}</div>
                  <div class="stat-label">安全提醒</div>
                </div>
              </div>
            </div>
            
            <!-- 文档类型分布 -->
            <div class="type-distribution">
              <h4>📋 文档类型分布</h4>
              <div class="type-list">
                <div 
                  v-for="(count, type) in knowledgeStats.types" 
                  :key="type"
                  class="type-item"
                >
                  <span class="type-name">{{ formatTypeName(type) }}</span>
                  <span class="type-count">{{ count }} 篇</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 操作结果提示 -->
    <div class="result-section" v-if="successMessage || error">
      <el-alert 
        v-if="error" 
        :title="error" 
        type="error" 
        :closable="true"
        @close="error = ''"
        style="margin-bottom: 16px;"
      />
      
      <el-alert 
        v-if="successMessage" 
        :title="successMessage" 
        type="success" 
        :closable="true"
        @close="successMessage = ''"
        style="margin-bottom: 16px;"
      />
    </div>
    
    <!-- 最近活动 -->
    <div class="recent-activity" v-if="recentActivity.length > 0">
      <el-divider>📝 最近活动</el-divider>
      <div class="activity-list">
        <div 
          v-for="(activity, index) in recentActivity" 
          :key="index"
          class="activity-item"
        >
          <div class="activity-icon">{{ activity.type === 'upload' ? '📄' : '🌐' }}</div>
          <div class="activity-content">
            <div class="activity-title">{{ activity.title }}</div>
            <div class="activity-time">{{ activity.time }}</div>
          </div>
          <div class="activity-status">
            <el-tag :type="activity.status === 'success' ? 'success' : 'warning'" size="small">
              {{ activity.status === 'success' ? '成功' : '处理中' }}
            </el-tag>
          </div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { uploadFile, getKnowledgeStats, getRecentActivity, collectDataEnhanced } from '../services/api'
import type { UploadResponse } from '../services/api'

const activeTab = ref('upload')
const uploading = ref(false)
const collecting = ref(false)
const collectUrl = ref('')
const error = ref('')
const successMessage = ref('')
const uploadRef = ref()

const knowledgeStats = ref({
  total_documents: 0,
  types: {},
  total_tools: 0,
  total_warnings: 0
})

const recentActivity = ref([
  {
    type: 'upload',
    title: '上传维修手册.pdf',
    time: '2分钟前',
    status: 'success'
  }
])

const presetSources = ref([
  { name: 'iFixit 手机维修', url: 'https://zh.ifixit.com/Device/Phone' },
  { name: 'iFixit 笔记本维修', url: 'https://zh.ifixit.com/Device/Laptop' },
  { name: 'iFixit 平板维修', url: 'https://zh.ifixit.com/Device/Tablet' },
  { name: '华为维修指南', url: 'https://zh.ifixit.com/Device/Huawei' }
])

function triggerUpload() {
  uploadRef.value?.$el.querySelector('input[type="file"]').click()
}

async function handleUpload(file: File) {
  if (file.size > 10 * 1024 * 1024) {
    error.value = '文件大小不能超过10MB'
    return false
  }
  
  uploading.value = true
  error.value = ''
  successMessage.value = ''
  
  try {
    const response: UploadResponse = await uploadFile(file)
    if (response.success) {
      successMessage.value = `✅ ${response.message}`
      
      // 添加到最近活动
      recentActivity.value.unshift({
        type: 'upload',
        title: file.name,
        time: '刚刚',
        status: 'success'
      })
      
      // 刷新统计
      await loadKnowledgeStats()
    } else {
      error.value = response.message || '上传失败'
    }
  } catch (err: any) {
    error.value = err.message || '上传失败，请检查后端服务是否正常运行'
  } finally {
    uploading.value = false
  }
  
  return false
}

async function startCollect() {
  if (!collectUrl.value.trim()) {
    error.value = '请输入要采集的网址'
    return
  }
  
  if (!collectUrl.value.startsWith('http://') && !collectUrl.value.startsWith('https://')) {
    error.value = '请输入有效的网址（需以http://或https://开头）'
    return
  }
  
  collecting.value = true
  error.value = ''
  successMessage.value = ''
  
  try {
    const response = await collectDataEnhanced(collectUrl.value)
    successMessage.value = `🎉 ${response.message}，任务ID：${response.task_id}`
    
    // 添加到最近活动
    recentActivity.value.unshift({
      type: 'collect',
      title: `采集：${collectUrl.value}`,
      time: '刚刚',
      status: 'success'
    })
    
    collectUrl.value = ''
    
    // 延时刷新统计（模拟采集完成）
    setTimeout(async () => {
      await loadKnowledgeStats()
      await loadRecentActivity()
    }, 2000)
    
  } catch (err: any) {
    error.value = err.message || '采集失败，请检查网址是否正确'
  } finally {
    collecting.value = false
  }
}

async function loadKnowledgeStats() {
  try {
    const stats = await getKnowledgeStats()
    knowledgeStats.value = stats
    console.log('✅ 知识库统计加载成功:', stats)
  } catch (err) {
    console.warn('⚠️ 获取统计信息失败:', err)
  }
}

async function loadRecentActivity() {
  try {
    const response = await getRecentActivity(5)
    recentActivity.value = response.activities || []
    console.log('✅ 最近活动加载成功')
  } catch (err) {
    console.warn('⚠️ 获取活动记录失败:', err)
  }
}

function usePresetSource(url: string) {
  collectUrl.value = url
  activeTab.value = 'collect'
}

onMounted(() => {
  loadKnowledgeStats()
  loadRecentActivity()
})
</script>

<style scoped>
.knowledge-container {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.knowledge-tabs {
  margin-top: 20px;
}

.tab-content {
  padding: 20px 0;
}

/* 上传部分 */
.upload-section {
  text-align: center;
}

.upload-dragger {
  margin-bottom: 20px;
}

.upload-icon {
  font-size: 60px;
  color: #8b7355;
  margin-bottom: 16px;
}

.upload-text p {
  margin: 8px 0;
  color: #666;
}

.upload-hint {
  font-size: 12px;
  color: #999;
}

.upload-btn {
  padding: 12px 30px;
  font-size: 16px;
}

/* 采集部分 */
.collect-section {
  max-width: 600px;
  margin: 0 auto;
}

.collect-form {
  display: flex;
  gap: 12px;
  margin-bottom: 30px;
}

.url-input {
  flex: 1;
}

.collect-btn {
  padding: 0 24px;
}

.preset-sources {
  text-align: center;
}

.preset-sources h4 {
  margin-bottom: 16px;
  color: #7c5b3a;
}

.source-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
}

.source-tag {
  cursor: pointer;
  padding: 8px 16px;
  transition: all 0.3s;
}

.source-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* 状态部分 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #faf8f4;
  border-radius: 12px;
  border: 1px solid #e4d4c8;
}

.stat-icon {
  font-size: 32px;
  margin-right: 16px;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #8b7355;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.type-distribution {
  background: #faf8f4;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e4d4c8;
}

.type-distribution h4 {
  margin: 0 0 16px 0;
  color: #7c5b3a;
}

.type-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.type-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: white;
  border-radius: 6px;
}

.type-name {
  color: #333;
}

.type-count {
  color: #8b7355;
  font-weight: 500;
}

/* 最近活动 */
.recent-activity {
  margin-top: 30px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #faf8f4;
  border-radius: 8px;
  border: 1px solid #e4d4c8;
}

.activity-icon {
  font-size: 24px;
  margin-right: 16px;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: #999;
}

.wood-btn {
  background: linear-gradient(135deg, #8B7355 0%, #A0845C 100%);
  border: none;
  border-radius: 25px;
  font-weight: bold;
  transition: all 0.3s;
}

.wood-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 115, 85, 0.4);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .collect-form {
    flex-direction: column;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .source-tags {
    flex-direction: column;
  }
}
</style>