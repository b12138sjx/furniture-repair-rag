<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const dialogVisible = ref(false)
const router = useRouter()
</script>

<template>
  <div class="ifixit-root">
    <header class="ifixit-header">
      <div class="ifixit-logo" @click="router.push('/')">
        <img src="/wrench.svg" alt="diy家具维修" class="ifixit-logo-img" />
        <span class="ifixit-logo-title">diy家具维修</span>
      </div>
      <nav class="ifixit-nav">
        <el-button type="text" @click="router.push('/')">首页</el-button>
        <el-button type="text" @click="router.push('/kb')">知识库</el-button>
        <el-button type="text" @click="router.push('/qa')">问答</el-button>
        <el-button type="text" @click="router.push('/collect')">数据采集</el-button>
        <el-button type="text" @click="dialogVisible = true">关于</el-button>
      </nav>
    </header>
    <main class="ifixit-main">
      <router-view />
    </main>
    <footer class="ifixit-footer">
      <span>© 2024 diy家具维修</span>
    </footer>
    <el-dialog v-model="dialogVisible" title="关于本系统" width="400px">
      <span>
        本系统致力于为用户提供专业、开放、简洁的家具维修知识与工具，灵感来自 ifixit。
      </span>
    </el-dialog>
  </div>
</template>

<style scoped>
/* 主色调原木色，风格简洁大气，参考 ifixit */
.ifixit-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f7f5f2;
  font-family: 'Avenir', 'Helvetica Neue', Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  color: #4b3a2f;
}
.ifixit-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1.5px solid #e4d4c8;
  box-shadow: 0 2px 8px #e4d4c880;
  padding: 0 40px;
  height: 64px;
  position: sticky;
  top: 0;
  z-index: 10;
}
.ifixit-logo {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}
.ifixit-logo-img {
  width: 36px;
  height: 36px;
  margin-right: 10px;
  filter: drop-shadow(0 2px 4px #b0896833);
}
.ifixit-logo-title {
  font-size: 1.6rem;
  font-weight: bold;
  color: #b08968;
  letter-spacing: 2px;
}
.ifixit-nav {
  display: flex;
  gap: 8px;
}
.ifixit-nav .el-button {
  font-size: 1rem;
  color: #5c4033;
  font-weight: 500;
  background: none;
  border-radius: 6px;
  padding: 6px 18px;
  transition: background 0.2s, color 0.2s;
}
.ifixit-nav .el-button:hover {
  background: #e4d4c8;
  color: #b08968;
}
.ifixit-main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 48px 12px 32px 12px;
  background: #f7f5f2;
}
.ifixit-footer {
  background: #fff;
  color: #b08968;
  text-align: center;
  padding: 16px 0 10px 0;
  font-size: 15px;
  letter-spacing: 1px;
  border-top: 1.5px solid #e4d4c8;
  box-shadow: 0 -2px 8px #e4d4c880;
}
@media (max-width: 900px) {
  .ifixit-header { padding: 0 12px; }
  .ifixit-main { padding: 24px 2px 16px 2px; }
}
</style>