<template>
  <el-card class="wood-card" style="width: 100%; max-width: 600px;">
    <h2>📊 数据采集</h2>
    <p style="margin: 16px 0; color: #7c5b3a;">
      从维修网站采集最新的维修指南和技术文档
    </p>
    
    <!-- 爬虫状态 -->
    <el-alert 
      v-if="crawlerStatus"
      :title="crawlerStatus.message"
      :type="crawlerStatus.status === 'ready' ? 'success' : 'info'"
      :closable="false"
      style="margin-bottom: 16px;"
    >
      <div>已爬取文档: {{ crawlerStatus.total_crawled }} 篇</div>
    </el-alert>
    
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
    
    <!-- 预设网址 -->
    <div class="preset-urls" style="margin: 16px 0;">
      <h4>🔗 推荐采集网址</h4>
      <el-tag 
        v-for="presetUrl in presetUrls" 
        :key="presetUrl.url"
        @click="usePresetUrl(presetUrl.url)"
        class="preset-tag"
        style="margin: 4px;"
      >
        {{ presetUrl.name }}
      </el-tag>
    </div>
    
    <el-divider />
    
    <!-- 错误提示 -->
    <el-alert 
      v-if="error" 
      :title="error" 
      type="error" 
      :closable="true"
      @close="error = ''"
      style="margin-bottom: 16px;"
    />
    
    <!-- 采集结果 -->
    <div v-if="result">
      <el-alert title="采集结果" type="success" :closable="false" show-icon>
        <div style="margin-top: 10px;">{{ result }}</div>
      </el-alert>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { collectData, getCrawlerStatus } from '../services/api'

const url = ref('')
const loading = ref(false)
const result = ref('')
const error = ref('')
const crawlerStatus = ref(null)

const presetUrls = ref([
  { name: 'iFixit 手机维修', url: 'https://zh.ifixit.com/Device/Phone' },
  { name: 'iFixit 电脑维修', url: 'https://zh.ifixit.com/Device/Laptop' },
  { name: '维修指南示例', url: 'https://example-repair-guide.com' }
])

async function collect() {
  if (!url.value.trim()) {
    error.value = '请输入要采集的网址'
    return
  }
  
  // 简单URL验证
  if (!url.value.startsWith('http://') && !url.value.startsWith('https://')) {
    error.value = '请输入有效的网址（需以http://或https://开头）'
    return
  }
  
  loading.value = true
  error.value = ''
  result.value = ''
  
  try {
    const response = await collectData(url.value)
    result.value = `成功启动采集任务：${response.message}，任务ID：${response.task_id || 'N/A'}`
    
    // 刷新状态
    await loadCrawlerStatus()
  } catch (err: any) {
    error.value = err.message || '采集失败，请检查网址是否正确或后端服务是否正常运行'
  } finally {
    loading.value = false
  }
}

function usePresetUrl(presetUrl: string) {
  url.value = presetUrl
}

async function loadCrawlerStatus() {
  try {
    crawlerStatus.value = await getCrawlerStatus()
  } catch (err) {
    console.warn('获取爬虫状态失败:', err)
  }
}

onMounted(() => {
  loadCrawlerStatus()
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

.preset-urls {
  background: #faf8f4;
  padding: 16px;
  border-radius: 8px;
}

.preset-tag {
  cursor: pointer;
  transition: all 0.3s;
}

.preset-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
</style>