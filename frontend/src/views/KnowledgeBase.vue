<template>
  <el-card>
    <h2>知识库管理</h2>
    <el-button type="primary" @click="refresh">刷新</el-button>
    <el-table :data="kbList" style="width: 100%; margin-top: 16px;">
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="count" label="条目数" width="100" />
      <el-table-column prop="status" label="向量化状态" width="120">
        <template #default="scope">
          <el-tag v-if="scope.row.status==='done'" type="success">已完成</el-tag>
          <el-tag v-else-if="scope.row.status==='processing'" type="warning">处理中</el-tag>
          <el-tag v-else type="info">未开始</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220">
        <template #default="scope">
          <el-button size="small" @click="viewDetail(scope.row)">详情</el-button>
          <el-button size="small" @click="startVectorize(scope.row)" :loading="scope.row.status==='processing'">向量化</el-button>
          <el-button size="small" type="danger" @click="remove(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="showDetail" title="知识库详情">
      <el-table :data="detailChunks" style="width: 100%">
        <el-table-column prop="index" label="块编号" width="80" />
        <el-table-column prop="content" label="内容" />
        <el-table-column prop="meta" label="元数据" />
      </el-table>
    </el-dialog>
    <el-dialog v-model="showVectorize" title="向量化进度" width="400px">
      <el-progress :percentage="vectorizeProgress" />
      <div v-if="vectorizeStatus" style="margin-top: 12px;">
        <el-alert :title="vectorizeStatus" type="success" v-if="vectorizeProgress===100" />
      </div>
    </el-dialog>
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