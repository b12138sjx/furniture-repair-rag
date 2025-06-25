<template>
  <el-card class="wood-card" style="width: 100%; max-width: 600px;">
    <h2>欢迎使用diy家具维修</h2>
    <p style="margin: 24px 0 32px 0; color: #7c5b3a;">
      这里为你提供专业、开放、简洁的家具维修知识与工具，助你轻松DIY修复家居。
    </p>
    <el-button type="primary" @click="$emit('showAbout')">了解更多</el-button>
  </el-card>
</template>

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
