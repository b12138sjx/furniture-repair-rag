<template>
  <el-card>
    <h2>网页数据爬取</h2>
    <el-form :inline="true" @submit.prevent>
      <el-form-item>
        <el-input v-model="url" placeholder="输入网页URL" style="width: 300px;" />
      </el-form-item>
      <el-form-item>
        <el-button @click="crawl" :loading="loadingCrawl" type="primary">开始爬取</el-button>
      </el-form-item>
    </el-form>
    <el-progress v-if="loadingCrawl" :percentage="crawlProgress" style="width: 300px;" />
    <el-alert v-if="crawlStatus" :title="crawlStatus" :type="crawlSuccess ? 'success' : 'error'" show-icon />
    <el-card v-if="crawlPreview" class="box-card" style="margin-top: 12px;">
      <template #header>文本预览</template>
      <pre style="max-height:200px;overflow:auto;">{{ crawlPreview }}</pre>
    </el-card>

    <el-divider />

    <h2>个人知识库导入</h2>
    <el-upload
      ref="uploadRef"
      :action="uploadAction"
      :headers="uploadHeaders"
      :show-file-list="false"
      :before-upload="beforeUpload"
      :on-progress="handleUploadProgress"
      :on-success="handleUploadSuccess"
      :on-error="handleUploadError"
      :accept="'.txt,.md,.pdf'"
      :data="{}"
      :http-request="customUpload"
    >
      <el-button type="primary">上传文档</el-button>
    </el-upload>
    <el-progress v-if="uploading" :percentage="uploadProgress" style="width: 300px;" />
    <el-alert v-if="uploadStatus" :title="uploadStatus" :type="uploadSuccess ? 'success' : 'error'" show-icon />
    <el-card v-if="chunkPreview.length" class="box-card" style="margin-top: 12px;">
      <template #header>分块预览</template>
      <el-table :data="chunkPreview" style="width: 100%">
        <el-table-column prop="index" label="块编号" width="80" />
        <el-table-column prop="content" label="内容" />
      </el-table>
    </el-card>
  </el-card>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const url = ref('');
const loadingCrawl = ref(false);
const crawlProgress = ref(0);
const crawlStatus = ref('');
const crawlSuccess = ref(false);
const crawlPreview = ref('');

const uploading = ref(false);
const uploadProgress = ref(0);
const uploadStatus = ref('');
const uploadSuccess = ref(false);
const chunkPreview = ref<{index:number,content:string}[]>([]);

const uploadAction = '/api/kb/upload'; // 实际不会用到
const uploadHeaders = {};

function crawl() {
  if (!url.value) {
    ElMessage.warning('请输入URL');
    return;
  }
  loadingCrawl.value = true;
  crawlProgress.value = 10;
  crawlStatus.value = '';
  crawlSuccess.value = false;
  crawlPreview.value = '';
  // 假设后端接口 /api/crawl，POST { url }
  axios.post('/api/crawl', { url: url.value }).then(res => {
    crawlProgress.value = 100;
    crawlSuccess.value = true;
    crawlStatus.value = '爬取成功';
    crawlPreview.value = res.data.text?.slice(0, 1000) || '无内容';
  }).catch(() => {
    crawlProgress.value = 100;
    crawlSuccess.value = false;
    crawlStatus.value = '爬取失败';
  }).finally(() => {
    loadingCrawl.value = false;
  });
}

// 文件上传自定义实现
function beforeUpload() {
  uploading.value = true;
  uploadProgress.value = 0;
  uploadStatus.value = '';
  uploadSuccess.value = false;
  chunkPreview.value = [];
  return true;
}
function handleUploadProgress(event: any) {
  uploading.value = true;
  uploadProgress.value = Math.round(event.percent);
}
function handleUploadSuccess(response: any) {
  uploadProgress.value = 100;
  uploadSuccess.value = true;
  uploadStatus.value = '上传并分块成功';
  // 假设后端返回 { chunks: [{index, content}] }
  chunkPreview.value = (response.chunks || []).map((c: any, i: number) => ({
    index: i + 1,
    content: c.content?.slice(0, 100) || ''
  }));
  uploading.value = false;
}
function handleUploadError() {
  uploadProgress.value = 100;
  uploadSuccess.value = false;
  uploadStatus.value = '上传失败';
  uploading.value = false;
}
// 自定义上传，兼容 axios
function customUpload(option: any) {
  const formData = new FormData();
  formData.append('file', option.file);
  axios.post('/api/kb/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (e) => {
      if (e.total) uploadProgress.value = Math.round((e.loaded / e.total) * 100);
    }
  }).then(res => {
    handleUploadSuccess(res.data);
    option.onSuccess && option.onSuccess(res.data);
  }).catch(err => {
    handleUploadError();
    option.onError && option.onError(err);
  });
}
</script>
