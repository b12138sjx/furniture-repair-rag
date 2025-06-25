<template>
  <el-card class="wood-card">
    <h2>智能问答</h2>
    <el-input v-model="question" placeholder="请输入您的问题" />
    <el-button type="primary" @click="ask">提问</el-button>
    <div v-if="answer" class="qa-answer">
      <strong>回答：</strong>{{ answer }}
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const question = ref('')
const answer = ref('')
function ask() {
  // 这里应调用后端接口
  answer.value = '（示例回答）这是一个家具维修相关的智能回答。'
}
</script>

<style scoped>
.qa-answer {
  margin-top: 16px;
  color: #5c4033;
}
</style>