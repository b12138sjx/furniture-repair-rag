<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const dialogVisible = ref(false)
const router = useRouter()
const sidebarCollapsed = ref(false)
</script>

<template>
  <div class="app-container">
    <!-- 左侧边栏 -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <!-- 顶部Logo -->
      <div class="sidebar-header">
        <div class="logo" @click="router.push('/')">
          <img src="/wrench.svg" alt="diy家具维修" class="logo-img" />
          <span v-if="!sidebarCollapsed" class="logo-title">家具维修助手</span>
        </div>
        <el-button 
          @click="sidebarCollapsed = !sidebarCollapsed" 
          class="collapse-btn"
          circle
          size="small"
        >
          <el-icon>
            <Fold v-if="!sidebarCollapsed" />
            <Expand v-else />
          </el-icon>
        </el-button>
      </div>
      
      <!-- 导航菜单 -->
      <nav class="sidebar-nav">
        <div class="nav-section">
          <div v-if="!sidebarCollapsed" class="nav-section-title">主要功能</div>
          <div class="nav-items">
            <router-link 
              to="/" 
              class="nav-item"
              :class="{ active: $route.path === '/' }"
            >
              <el-icon><House /></el-icon>
              <span v-if="!sidebarCollapsed">首页</span>
            </router-link>
            
            <router-link 
              to="/qa" 
              class="nav-item"
              :class="{ active: $route.path === '/qa' }"
            >
              <el-icon><ChatDotRound /></el-icon>
              <span v-if="!sidebarCollapsed">智能问答</span>
            </router-link>
            
            <router-link 
              to="/kb" 
              class="nav-item"
              :class="{ active: $route.path === '/kb' }"
            >
              <el-icon><Document /></el-icon>
              <span v-if="!sidebarCollapsed">知识库</span>
            </router-link>
          </div>
        </div>
        
        <div v-if="!sidebarCollapsed" class="nav-section">
          <div class="nav-section-title">最近对话</div>
          <div class="chat-history">
            <div class="history-item">
              <el-icon><ChatLineRound /></el-icon>
              <span>如何更换iPhone电池？</span>
            </div>
            <div class="history-item">
              <el-icon><ChatLineRound /></el-icon>
              <span>屏幕破裂维修步骤</span>
            </div>
            <div class="history-item">
              <el-icon><ChatLineRound /></el-icon>
              <span>充电口清洁方法</span>
            </div>
          </div>
        </div>
      </nav>
      
      <!-- 底部设置 -->
      <div class="sidebar-footer">
        <div class="footer-item" @click="dialogVisible = true">
          <el-icon><InfoFilled /></el-icon>
          <span v-if="!sidebarCollapsed">关于系统</span>
        </div>
        <div class="footer-item">
          <el-icon><Setting /></el-icon>
          <span v-if="!sidebarCollapsed">设置</span>
        </div>
      </div>
    </aside>

    <!-- 右侧主内容区 -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- 关于对话框 -->
    <el-dialog v-model="dialogVisible" title="关于本系统" width="500px">
      <div class="about-content">
        <p>🔧 <strong>家具维修智能助手</strong></p>
        <p>基于RAG技术的智能维修知识库问答系统</p>
        <ul>
          <li>🤖 智能问答：自然语言理解维修问题</li>
          <li>📚 知识库：丰富的维修指南和技术文档</li>
          <li>🔍 数据采集：自动抓取最新维修信息</li>
          <li>💡 个性化：支持上传自定义维修文档</li>
        </ul>
        <p class="inspiration">灵感来自 iFixit，致力于让维修变得更简单</p>
      </div>
    </el-dialog>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  background: #f8f9fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 左侧边栏 */
.sidebar {
  width: 280px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
  transition: width 0.3s ease;
  position: relative;
}

.sidebar.collapsed {
  width: 64px;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: opacity 0.2s;
  flex: 1;
}

.logo:hover {
  opacity: 0.8;
}

.logo-img {
  width: 32px;
  height: 32px;
  margin-right: 12px;
  filter: drop-shadow(0 2px 4px #b0896833);
}

.logo-title {
  font-size: 18px;
  font-weight: 600;
  color: #8b7355;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.collapse-btn {
  background: transparent;
  border: 1px solid #e5e7eb;
  color: #6b7280;
  transition: all 0.2s;
}

.collapse-btn:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.sidebar-nav {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 32px;
}

.nav-section-title {
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  margin: 0 20px 12px 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.nav-items {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 0 12px;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-radius: 8px;
  color: #4b5563;
  text-decoration: none;
  transition: all 0.2s;
  font-size: 14px;
  font-weight: 500;
  gap: 12px;
  position: relative;
}

.nav-item:hover {
  background: #f3f4f6;
  color: #8b7355;
}

.nav-item.active {
  background: linear-gradient(135deg, #8b7355, #a0845c);
  color: white;
}

.nav-item .el-icon {
  font-size: 18px;
  min-width: 18px;
}

.chat-history {
  padding: 0 12px;
  max-height: 300px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  margin-bottom: 4px;
  background: #f9fafb;
  border-radius: 6px;
  font-size: 13px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.history-item:hover {
  background: #f3f4f6;
  color: #374151;
}

.history-item span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-footer {
  padding: 20px 12px;
  border-top: 1px solid #f3f4f6;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.footer-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 6px;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.footer-item:hover {
  background: #f3f4f6;
  color: #374151;
}

.footer-item .el-icon {
  font-size: 16px;
  min-width: 16px;
}

/* 右侧主内容 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f8f9fa;
  overflow: hidden;
}

/* 关于对话框样式 */
.about-content {
  line-height: 1.6;
}

.about-content p {
  margin: 0 0 16px 0;
}

.about-content ul {
  margin: 16px 0;
  padding-left: 20px;
}

.about-content li {
  margin-bottom: 8px;
}

.inspiration {
  font-size: 14px;
  color: #6b7280;
  font-style: italic;
  text-align: center;
  margin-top: 20px !important;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    width: 64px;
  }
  
  .sidebar.collapsed {
    width: 48px;
  }
  
  .sidebar-header {
    padding: 16px 12px;
  }
  
  .logo-title {
    display: none;
  }
  
  .nav-section-title {
    display: none;
  }
  
  .chat-history {
    display: none;
  }
}

@media (max-width: 640px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 1000;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .sidebar.collapsed {
    transform: translateX(0);
    width: 64px;
  }
  
  .main-content {
    margin-left: 0;
  }
}
</style>