<template>
  <div v-if="answer">
    <h3>回答结果</h3>
    <p>{{ answer }}</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({ answer: String });
</script>