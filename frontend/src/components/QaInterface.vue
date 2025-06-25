<template>
  <div>
    <input v-model="question" placeholder="请输入您的问题" />
    <button @click="getAnswer">提问</button>
    <ResultDisplay :answer="answer" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import furnitureApi from '../api/furnitureApi';
import ResultDisplay from './ResultDisplay.vue';

const question = ref('');
const answer = ref('');

const getAnswer = async () => {
  if (question.value) {
    try {
      const response = await furnitureApi.getAnswer(question.value);
      answer.value = response.data.answer;
    } catch (error) {
      console.error('获取答案失败:', error);
    }
  }
};
</script>