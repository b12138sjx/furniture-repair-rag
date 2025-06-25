<template>
  <el-card class="wood-card" style="width: 100%; max-width: 600px;">
    <h2>智能问答</h2>
    <el-input
      v-model="question"
      placeholder="请输入您的问题"
      style="margin-bottom: 18px;"
      clearable
    />
    <el-button type="primary" @click="ask" style="margin-bottom: 18px;">提问</el-button>
    <el-divider />
    <div v-if="answer" class="qa-answer">
      <el-alert title="回答" type="success" :closable="false" show-icon>
        <div style="margin-top: 10px;">{{ answer }}</div>
      </el-alert>
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
.wood-card {
  background: #f5e9da;
  border: 1px solid #c8ad7f;
  border-radius: 16px;
  box-shadow: 0 4px 16px #c8ad7f33;
  padding: 40px 32px;
  min-width: 320px;
  text-align: center;
}
.qa-answer {
  margin-top: 16px;
  color: #5c4033;
}
</style>