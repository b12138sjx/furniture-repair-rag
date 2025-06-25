<template>
  <el-card class="wood-card">
    <h2>知识库管理</h2>
    <p>这里可以上传、管理家具维修相关文档。</p>
    <!-- 可扩展上传、列表等功能 -->
  </el-card>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';

const kbList = ref([
  { name: '家具维修知识库', count: 120, status: 'done' },
  { name: '沙发保养', count: 45, status: 'processing' },
  { name: '地板修复', count: 30, status: 'none' }
]);
const showDetail = ref(false);
const detailChunks = ref<any[]>([]);
const showVectorize = ref(false);
const vectorizeProgress = ref(0);
const vectorizeStatus = ref('');
function refresh() {
  // ...实际应请求后端获取知识库列表...
  ElMessage.success('已刷新');
}
function viewDetail(row: any) {
  // ...实际应请求后端获取详情...
  detailChunks.value = [
    { index: 1, content: '块内容示例1', meta: '来源A, 摘要...' },
    { index: 2, content: '块内容示例2', meta: '来源B, 摘要...' }
  ];
  showDetail.value = true;
}
function remove(row: any) {
  kbList.value = kbList.value.filter(item => item !== row);
  ElMessage.success('已删除');
}
function startVectorize(row: any) {
  showVectorize.value = true;
  vectorizeProgress.value = 0;
  vectorizeStatus.value = '';
  row.status = 'processing';
  let timer = setInterval(() => {
    if (vectorizeProgress.value < 100) {
      vectorizeProgress.value += 20;
    } else {
      clearInterval(timer);
      row.status = 'done';
      vectorizeStatus.value = '向量化完成';
    }
  }, 400);
}
</script>