<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const dialogVisible = ref(false)
const router = useRouter()
</script>

<template>
  <div class="bt-wood-root">
    <aside class="bt-wood-sider">
      <div class="bt-wood-logo">
        <span>RAG</span>
      </div>
      <el-menu
        :default-active="router.currentRoute.value.path"
        class="bt-wood-menu"
        @select="key => router.push(key)"
        background-color="#e4d4c8"
        text-color="#5c4033"
        active-text-color="#b08968"
        router
      >
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/kb">知识库</el-menu-item>
        <el-menu-item index="/qa">问答</el-menu-item>
        <el-menu-item index="/collect">数据采集</el-menu-item>
      </el-menu>
      <div class="bt-wood-sider-footer">
        <el-button type="text" @click="dialogVisible = true">关于</el-button>
      </div>
    </aside>
    <div class="bt-wood-main">
      <header class="bt-wood-header">
        <span class="bt-wood-title">家具维修 RAG 系统</span>
        <span class="bt-wood-header-actions"></span>
      </header>
      <main class="bt-wood-content">
        <router-view />
      </main>
      <footer class="bt-wood-footer">
        <span>© 2024 家具维修 RAG 系统</span>
      </footer>
    </div>
    <el-dialog v-model="dialogVisible" title="关于本系统" width="400px">
      <span>
        本系统基于原木风格设计，致力于为用户提供温馨、专业的家具维修知识问答体验。
      </span>
    </el-dialog>
  </div>
</template>

<style scoped>
.bt-wood-root {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5e9da 0%, #e4d4c8 100%);
  font-family: 'Avenir', 'Helvetica Neue', Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  color: #5c4033;
}
.bt-wood-sider {
  width: 72px;
  background: #e4d4c8;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 2px 0 8px #c8ad7f22;
  padding-top: 18px;
  z-index: 2;
}
.bt-wood-logo {
  font-size: 22px;
  font-weight: bold;
  color: #b08968;
  margin-bottom: 32px;
  letter-spacing: 2px;
  width: 100%;
  text-align: center;
}
.bt-wood-menu {
  border: none;
  width: 100%;
  flex: 1;
  background: transparent;
}
.bt-wood-menu .el-menu-item {
  justify-content: center;
  font-size: 15px;
  border-radius: 8px;
  margin: 6px 0;
  transition: background 0.2s;
}
.bt-wood-menu .el-menu-item.is-active {
  background: #b08968 !important;
  color: #fff !important;
}
.bt-wood-sider-footer {
  margin: 24px 0 12px 0;
  width: 100%;
  text-align: center;
}
.bt-wood-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: #f5e9da;
}
.bt-wood-header {
  height: 56px;
  background: #fff;
  color: #5c4033;
  display: flex;
  align-items: center;
  padding: 0 32px;
  border-bottom: 1px solid #e4d4c8;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: 1px;
  box-shadow: 0 2px 8px #e4d4c880;
  z-index: 1;
}
.bt-wood-title {
  flex: 1;
}
.bt-wood-content {
  flex: 1;
  padding: 40px 0 0 0;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 400px;
}
.bt-wood-footer {
  background: #f5e9da;
  color: #b08968;
  text-align: center;
  padding: 12px 0 8px 0;
  font-size: 14px;
  letter-spacing: 1px;
  border-top: 1px solid #e4d4c8;
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