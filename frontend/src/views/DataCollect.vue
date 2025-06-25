<template>
  <el-card class="wood-card" style="width: 100%; max-width: 600px;">
    <h2>数据采集</h2>
    <el-form :inline="true" @submit.prevent>
      <el-form-item label="采集网址">
        <el-input v-model="url" placeholder="请输入要采集的网址" style="width: 320px;" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="collect">开始采集</el-button>
      </el-form-item>
    </el-form>
    <el-divider />
    <div v-if="loading">
      <el-icon><i class="el-icon-loading"></i></el-icon> 正在采集数据...
    </div>
    <div v-else-if="result">
      <el-alert title="采集结果" type="success" :closable="false" show-icon>
        <div style="margin-top: 10px;">{{ result }}</div>
      </el-alert>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const url = ref('')
const loading = ref(false)
const result = ref('')

function collect() {
  if (!url.value) return
  loading.value = true
  result.value = ''
  // 模拟采集过程，实际应调用后端API
  setTimeout(() => {
    loading.value = false
    result.value = `已成功采集：${url.value} 的网页内容（示例数据）`
  }, 1500)
}
</script>

<style scoped>
.wood-card {
  background: #f5e9da;
  border: 1px solid #c8ad7f;
  border-radius: 16px;
  box-shadow: 0 4px 16px #c8ad7f33;
  padding: 40px 32px;
  min-width: 320px;
  text-align: center;
}
</style>