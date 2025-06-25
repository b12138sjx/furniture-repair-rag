<script setup lang="ts">
import { ref } from 'vue'
const dialogVisible = ref(false)
</script>

<template>
  <div class="wood-theme">
    <header class="wood-header">
      <h1>家具维修 RAG 系统</h1>
    </header>
    <main class="wood-main">
      <el-card class="wood-card">
        <h2>欢迎使用家具维修智能问答系统</h2>
        <el-button type="primary" class="wood-btn" @click="dialogVisible = true">
          了解更多
        </el-button>
        <el-dialog v-model="dialogVisible" title="关于本系统" width="400px">
          <span>
            本系统基于原木风格设计，致力于为用户提供温馨、专业的家具维修知识问答体验。
          </span>
        </el-dialog>
      </el-card>
    </main>
    <footer class="wood-footer">
      <span>© 2024 家具维修 RAG 系统</span>
    </footer>
  </div>
</template>

<style scoped>
.wood-theme {
  min-height: 100vh;
  background: linear-gradient(135deg, #e4d4c8 0%, #f5e9da 100%);
  font-family: 'Avenir', 'Helvetica Neue', Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  color: #5c4033;
  display: flex;
  flex-direction: column;
}
.wood-header {
  background: #c8ad7f;
  color: #fff;
  padding: 24px 0 12px 0;
  text-align: center;
  box-shadow: 0 2px 8px #e4d4c880;
}
.logo {
  width: 48px;
  vertical-align: middle;
  margin-right: 10px;
}
.wood-main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
.wood-card {
  background: #f5e9da;
  border: 1px solid #c8ad7f;
  border-radius: 16px;
  box-shadow: 0 4px 16px #c8ad7f33;
  padding: 40px 32px;
  min-width: 320px;
  text-align: center;
}
.wood-btn {
  background: #b08968;
  border-color: #b08968;
  color: #fff;
  margin-top: 24px;
  transition: background 0.2s;
}
.wood-btn:hover {
  background: #a1744a;
  border-color: #a1744a;
}
.wood-footer {
  background: #c8ad7f;
  color: #fff;
  text-align: center;
  padding: 12px 0;
  font-size: 14px;
  letter-spacing: 1px;
}
.el-dialog__header {
  background: #e4d4c8;
  color: #5c4033;
}
.el-dialog__body {
  background: #f5e9da;
  color: #5c4033;
}
</style>