<template>
  <div>
    <input type="file" @change="handleFileUpload" />
    <button @click="uploadFile">上传文档</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import furnitureApi from '../api/furnitureApi';

const file = ref(null);

const handleFileUpload = (event) => {
  file.value = event.target.files[0];
};

const uploadFile = async () => {
  if (file.value) {
    try {
      const response = await furnitureApi.uploadDocument(file.value);
      console.log(response.data.message);
    } catch (error) {
      console.error('上传失败:', error);
    }
  }
};
</script>