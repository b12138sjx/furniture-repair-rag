<template>
  <div class="home-container">
    <!-- 主要欢迎区域 -->
    <div class="hero-section">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <!-- 主标题区域 -->
        <div class="hero-header">
          <div class="hero-logo">
            <img src="/wrench.svg" alt="diy家具维修" class="logo-icon" />
          </div>
          <h1 class="hero-title">diy家具维修助手</h1>
          <p class="hero-subtitle">专业、开放、简洁的家具维修知识与工具，助你轻松DIY修复家居</p>
        </div>
        
        <!-- 快速操作卡片 -->
        <div class="action-cards">
          <div class="primary-card" @click="$router.push('/qa')">
            <div class="card-icon">
              <el-icon><ChatDotRound /></el-icon>
            </div>
            <div class="card-content">
              <h3>开始智能问答</h3>
              <p>向AI助手询问任何维修问题，获得专业解答</p>
            </div>
            <div class="card-arrow">
              <el-icon><ArrowRight /></el-icon>
            </div>
          </div>
          
          <div class="secondary-cards">
            <div class="mini-card" @click="$router.push('/kb')">
              <div class="mini-icon kb-icon">
                <el-icon><Document /></el-icon>
              </div>
              <div class="mini-content">
                <h4>知识库管理</h4>
                <span>上传和管理维修文档</span>
              </div>
            </div>
            
            <div class="mini-card" @click="showExamples = !showExamples">
              <div class="mini-icon question-icon">
                <el-icon><QuestionFilled /></el-icon>
              </div>
              <div class="mini-content">
                <h4>常见问题</h4>
                <span>查看维修问题示例</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 示例问题区域 -->
    <transition name="slide-down">
      <div v-if="showExamples" class="examples-section">
        <div class="examples-content">
          <h3>💡 试试这些热门问题</h3>
          <div class="example-grid">
            <div 
              v-for="question in exampleQuestions" 
              :key="question"
              class="example-item"
              @click="askQuestion(question)"
            >
              <el-icon><ChatLineRound /></el-icon>
              <span>{{ question }}</span>
            </div>
          </div>
        </div>
      </div>
    </transition>
    
    <!-- 特性展示 -->
    <div class="features-section">
      <div class="features-content">
        <h2 class="section-title">为什么选择我们？</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>AI智能问答</h3>
            <p>支持多种大模型，理解自然语言，提供专业维修建议</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3>丰富知识库</h3>
            <p>涵盖各类设备的维修指南，持续更新最新技术文档</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3>智能检索</h3>
            <p>基于向量搜索技术，快速定位相关维修信息</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3>快速响应</h3>
            <p>秒级响应速度，24/7在线服务，随时解答维修疑问</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 统计数据 -->
    <div class="stats-section">
      <div class="stats-content">
        <div class="stat-item">
          <div class="stat-number">1000+</div>
          <div class="stat-label">维修指南</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">50+</div>
          <div class="stat-label">设备类型</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">24/7</div>
          <div class="stat-label">在线服务</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">99%</div>
          <div class="stat-label">问题解决率</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const showExamples = ref(false)

const exampleQuestions = ref([
  '如何更换iPhone电池？',
  '笔记本屏幕闪烁怎么办？',
  '手机充电慢的原因？',
  '电脑风扇噪音大如何处理？',
  '显示器花屏如何修复？',
  '键盘按键失灵怎么办？'
])

function askQuestion(question: string) {
  router.push({
    path: '/qa',
    query: { q: question }
  })
}
</script>

<style scoped>
.home-container {
  width: 100%;
  min-height: 100vh;
  background: #f7f5f2;
}

/* 主要欢迎区域 */
.hero-section {
  padding: 120px 40px 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  position: relative;
  background-image: url('@/assets/home.jpg'); /* 修改为相对路径 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(0, 0, 0, 0.65) 0%,
    rgba(139, 115, 85, 0.75) 30%,
    rgba(160, 132, 92, 0.65) 70%,
    rgba(0, 0, 0, 0.55) 100%
  );
  backdrop-filter: blur(1px);
}

.hero-content {
  max-width: 1200px;
  width: 100%;
  text-align: center;
  position: relative;
  z-index: 2;
}

.hero-header {
  margin-bottom: 60px;
  /* background: rgba(0, 0, 0, 0.3); */
  /* padding: 40px; */
  border-radius: 20px;
  /* backdrop-filter: blur(10px); */
  /* border: 1px solid rgba(255, 255, 255, 0.1); */
}

.hero-logo {
  margin-bottom: 32px;
}

.logo-icon {
  width: 96px;
  height: 96px;
  filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.5)) brightness(1.3);
}

.hero-title {
  font-size: 64px;
  font-weight: 700;
  color: white;
  margin: 0 0 20px 0;
  letter-spacing: 1px;
  line-height: 1.2;
  /* text-shadow: 
    0 2px 4px rgba(0, 0, 0, 0.8),
    0 1px 0px rgba(255, 255, 255, 0.1); */
  background: linear-gradient(135deg, #ffffff, #f0f0f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 24px;
  color: white;
  margin: 0;
  line-height: 1.6;
  opacity: 0.9;
  max-width: 800px;
  margin: 0 auto;
}

/* 操作卡片 */
.action-cards {
  display: flex;
  flex-direction: column;
  gap: 32px;
  align-items: center;
}

.primary-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(15px);
  padding: 48px;
  border-radius: 24px;
  box-shadow: 
    0 12px 48px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 32px;
  max-width: 700px;
  width: 100%;
}

.primary-card:hover {
  transform: translateY(-8px);
  box-shadow: 
    0 24px 64px rgba(0, 0, 0, 0.35),
    0 0 0 1px rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.98);
}

.card-icon {
  width: 72px;
  height: 72px;
  background-image: url('@/assets/btn1.png'); /* 修改为相对路径 */
  background-size: cover; /* 添加背景尺寸 */
  background-position: center; /* 添加背景位置 */
  background-repeat: no-repeat; /* 防止重复 */
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 32px;
  box-shadow: 0 8px 24px rgba(139, 115, 85, 0.3);
}

.card-content {
  flex: 1;
  text-align: left;
}

.card-content h3 {
  margin: 0 0 12px 0;
  color: #4b3a2f;
  font-size: 24px;
  font-weight: 600;
}

.card-content p {
  margin: 0;
  color: #7c5b3a;
  font-size: 16px;
  line-height: 1.5;
}

.card-arrow {
  color: #b08968;
  font-size: 32px;
  opacity: 0.6;
  transition: all 0.3s ease;
}

.primary-card:hover .card-arrow {
  opacity: 1;
  transform: translateX(8px);
}

.secondary-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  width: 100%;
  max-width: 700px;
}

.mini-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(15px);
  padding: 32px;
  border-radius: 20px;
  box-shadow: 
    0 8px 24px rgba(0, 0, 0, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 16px;
}

.mini-card:hover {
  transform: translateY(-4px);
  box-shadow: 
    0 16px 32px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.95);
}

.mini-icon {
  width: 48px;
  height: 48px;
  background: rgba(176, 137, 104, 0.1);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #b08968;
  font-size: 20px;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.mini-icon.kb-icon {
  background-image: url('@/assets/btn2.png');
}

.mini-icon.question-icon {
  background-image: url('@/assets/btn3.png');
}

.mini-content {
  flex: 1;
  text-align: left;
}

.mini-content h4 {
  margin: 0 0 6px 0;
  color: #4b3a2f;
  font-size: 16px;
  font-weight: 600;
}

.mini-content span {
  color: #7c5b3a;
  font-size: 14px;
}

/* 示例问题区域 */
.examples-section {
  background: white;
  border-top: 1px solid #e4d4c8;
  border-bottom: 1px solid #e4d4c8;
  padding: 60px 40px;
}

.examples-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.examples-content h3 {
  color: #8b7355;
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 32px 0;
}

.example-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 16px;
}

.example-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 24px;
  background: #faf8f4;
  border: 1px solid #f0e6d6;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #5c4033;
  font-size: 16px;
  font-weight: 500;
}

.example-item:hover {
  background: #f5e9da;
  border-color: #e4d4c8;
  transform: translateY(-2px);
}

/* 特性展示 */
.features-section {
  padding: 120px 40px;
  background: white;
}

.features-content {
  max-width: 1400px;
  margin: 0 auto;
  text-align: center;
}

.section-title {
  font-size: 42px;
  font-weight: 700;
  color: #8b7355;
  margin: 0 0 60px 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
}

.feature-card {
  background: #faf8f4;
  padding: 48px 32px;
  border-radius: 24px;
  border: 1px solid #f0e6d6;
  transition: all 0.3s ease;
  text-align: center;
}

.feature-card:hover {
  background: white;
  box-shadow: 0 16px 48px rgba(139, 115, 85, 0.15);
  transform: translateY(-8px);
  border-color: #e4d4c8;
}

.feature-icon {
  font-size: 64px;
  margin-bottom: 24px;
  display: block;
}

.feature-card h3 {
  font-size: 22px;
  font-weight: 600;
  color: #4b3a2f;
  margin: 0 0 16px 0;
}

.feature-card p {
  color: #7c5b3a;
  line-height: 1.6;
  margin: 0;
  font-size: 16px;
}

/* 统计数据 */
.stats-section {
  padding: 80px 40px;
  background: #f5e9da;
  border-top: 1px solid #e4d4c8;
}

.stats-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
}

.stat-item {
  text-align: center;
  padding: 40px 32px;
  background: white;
  border-radius: 20px;
  border: 1px solid #f0e6d6;
  box-shadow: 0 8px 24px rgba(139, 115, 85, 0.1);
}

.stat-number {
  font-size: 48px;
  font-weight: 700;
  color: #b08968;
  margin-bottom: 12px;
  display: block;
}

.stat-label {
  font-size: 16px;
  color: #7c5b3a;
  font-weight: 500;
}

/* 动画效果 */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.4s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .hero-section {
    padding: 100px 30px 60px;
  }
  
  .hero-header {
    padding: 32px;
  }
  
  .features-section {
    padding: 100px 30px;
  }
  
  .stats-section {
    padding: 60px 30px;
  }
  
  .examples-section {
    padding: 50px 30px;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 42px;
  }
  
  .hero-subtitle {
    font-size: 18px;
  }
  
  .hero-header {
    padding: 24px;
    margin-bottom: 40px;
  }
  
  .secondary-cards {
    grid-template-columns: 1fr;
  }
  
  .primary-card {
    padding: 32px 24px;
    flex-direction: column;
    text-align: center;
  }
  
  .card-content {
    text-align: center;
  }
  
  .section-title {
    font-size: 32px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }
  
  .stats-content {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
  
  .example-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 60px 16px 40px;
  }
  
  .hero-title {
    font-size: 36px;
  }
  
  .hero-subtitle {
    font-size: 16px;
  }
  
  .hero-header {
    padding: 20px;
  }
}
</style>
