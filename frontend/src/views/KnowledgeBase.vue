<template>
  <el-card class="wood-card" style="width: 100%; max-width: 600px;">
    <h2>知识库管理</h2>
    <p style="margin: 24px 0 32px 0; color: #7c5b3a;">
      上传、管理你的家具维修文档，丰富你的DIY知识库。
    </p>
    <el-button type="primary" disabled>上传文档（开发中）</el-button>
    <el-divider />
    <el-table :data="kbList" style="width: 100%; margin-top: 16px;" border>
      <el-table-column prop="name" label="知识库名称" />
      <el-table-column prop="count" label="文档数" width="90" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'done' ? 'success' : row.status === 'processing' ? 'warning' : 'info'">
            {{ row.status === 'done' ? '已完成' : row.status === 'processing' ? '处理中' : '未处理' }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const kbList = ref([
  { name: '家具维修知识库', count: 120, status: 'done' },
  { name: '沙发保养', count: 45, status: 'processing' },
  { name: '地板修复', count: 30, status: 'none' }
])
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