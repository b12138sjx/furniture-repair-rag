<template>
  <el-card>
    <h2>智能问答</h2>
    <el-input v-model="question" placeholder="请输入您的问题" style="width: 400px;" />
    <el-button @click="ask" :loading="loading">提交</el-button>
    <el-divider />
    <div v-if="retrieved.length">
      <h4>相关知识块：</h4>
      <el-timeline>
        <el-timeline-item v-for="(item, idx) in retrieved" :key="idx">
          <span style="color: #409EFF">{{ item.source }}</span>：
          <span v-html="highlight(item.content)"></span>
        </el-timeline-item>
      </el-timeline>
    </div>
    <el-divider />
    <div v-if="answer">
      <h4>AI答案：</h4>
      <el-card>
        <span>{{ answer }}</span>
        <el-button type="primary" size="small" @click="copyAnswer">复制</el-button>
      </el-card>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';

const question = ref('');
const loading = ref(false);
const retrieved = ref<any[]>([]);
const answer = ref('');
function ask() {
  loading.value = true;
  // ...实际应请求后端接口...
  setTimeout(() => {
    retrieved.value = [
      { source: '知识库1', content: '家具维修时应<b style="color:red;">安全</b>断电...' },
      { source: '知识库2', content: '如遇损坏，先<b style="color:red;">安全</b>检查...' }
    ];
    answer.value = '建议维修前务必断电，确保安全。';
    loading.value = false;
  }, 1000);
}
function copyAnswer() {
  navigator.clipboard.writeText(answer.value);
  ElMessage.success('已复制');
}
function highlight(text: string) {
  if (!question.value) return text;
  // 简单高亮匹配
  return text.replace(new RegExp(question.value, 'gi'), m => `<b style="color:red;">${m}</b>`);
}
</script>