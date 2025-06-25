<template>
  <el-card class="wood-card" style="width: 100%; max-width: 600px;">
    <h2>📊 数据采集管理</h2>
    
    <!-- 爬虫状态 -->
    <el-card class="status-card" style="margin-bottom: 20px;">
      <template #header>
        <span>🕷️ 爬虫状态</span>
        <el-button size="small" @click="checkCrawlerStatus" :loading="statusLoading">
          刷新状态
        </el-button>
      </template>
      
      <div v-if="crawlerStatus">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="数据文件">
            <el-tag :type="crawlerStatus.data_file_exists ? 'success' : 'danger'">
              {{ crawlerStatus.data_file_exists ? '存在' : '不存在' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="链接文件">
            <el-tag :type="crawlerStatus.urls_file_exists ? 'success' : 'danger'">
              {{ crawlerStatus.urls_file_exists ? '存在' : '不存在' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="数据条数">
            {{ crawlerStatus.data_count }}
          </el-descriptions-item>
          <el-descriptions-item label="链接数量">
            {{ crawlerStatus.urls_count }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
    
    <!-- 爬虫控制 -->
    <el-card style="margin-bottom: 20px;">
      <template #header>
        <span>🚀 启动爬虫</span>
      </template>
      
      <div style="margin-bottom: 15px;">
        <el-alert 
          title="爬虫说明" 
          type="info" 
          :closable="false"
          description="爬虫将自动从iFixit网站获取最新的维修指南，包括华为手机等设备的维修教程。"
        />
      </div>
      
      <el-button 
        type="primary" 
        @click="startCrawler" 
        :loading="crawlerLoading"
        :disabled="crawlerLoading"
        style="width: 100%;"
      >
        {{ crawlerLoading ? '爬虫运行中...' : '🕷️ 启动爬虫采集' }}
      </el-button>
    </el-card>
    
    <!-- 手动URL采集 -->
    <el-card>
      <template #header>
        <span>🔗 手动URL采集</span>
      </template>
      
      <el-form :inline="true" @submit.prevent>
        <el-form-item label="采集网址">
          <el-input 
            v-model="url" 
            placeholder="请输入要采集的网址" 
            style="width: 320px;" 
            :disabled="loading"
          />
        </el-form-item>
        <el-form-item>
          <el-button 
            class="wood-btn" 
            type="primary" 
            @click="collect"
            :loading="loading"
          >
            {{ loading ? '采集中...' : '开始采集' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 错误提示 -->
    <el-alert 
      v-if="error" 
      :title="error" 
      type="error" 
      :closable="true"
      @close="error = ''"
      style="margin-top: 16px;"
    />
    
    <!-- 采集结果 -->
    <div v-if="result" style="margin-top: 16px;">
      <el-alert :title="result" type="success" :closable="false" show-icon />
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { collectData } from '../services/api'
import api from '../services/api'

const url = ref('')
const loading = ref(false)
const result = ref('')
const error = ref('')

const crawlerLoading = ref(false)
const statusLoading = ref(false)
const crawlerStatus = ref<any>(null)

async function checkCrawlerStatus() {
  statusLoading.value = true
  try {
    const response = await api.get('/crawler/status')
    crawlerStatus.value = response.data.crawler_status
  } catch (err: any) {
    error.value = '获取爬虫状态失败'
  } finally {
    statusLoading.value = false
  }
}

async function startCrawler() {
  crawlerLoading.value = true
  error.value = ''
  result.value = ''
  
  try {
    const response = await api.post('/crawl')
    if (response.data.success) {
      result.value = `爬虫运行成功！已更新知识库，包含 ${response.data.knowledge_count} 条维修指南`
      await checkCrawlerStatus() // 刷新状态
    } else {
      error.value = response.data.message || '爬虫运行失败'
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || '爬虫启动失败'
  } finally {
    crawlerLoading.value = false
  }
}

async function collect() {
  if (!url.value.trim()) {
    error.value = '请输入要采集的网址'
    return
  }
  
  if (!url.value.startsWith('http://') && !url.value.startsWith('https://')) {
    error.value = '请输入有效的网址（需以http://或https://开头）'
    return
  }
  
  loading.value = true
  error.value = ''
  result.value = ''
  
  try {
    const response = await collectData(url.value)
    result.value = `成功采集：${url.value} 的网页内容`
  } catch (err: any) {
    error.value = err.message || '采集失败'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  checkCrawlerStatus()
})
</script>

<style scoped>
.status-card :deep(.el-card__header) {
  display: flex;
  justify-content: space-between;
  align-items: center;
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