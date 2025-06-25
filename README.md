# 家具维修 RAG 系统

本项目是一个基于家具维修领域的检索增强生成（RAG）系统，结合网页数据爬取、文档处理、向量存储、大模型调用和前端交互等功能，为用户提供家具维修相关问题的智能回答。

## 项目结构
```plaintext
furniture-repair-rag/
├── backend/                          # 后端代码
├── frontend/                         # 前端代码
├── data/                             # 数据存储
├── docs/                             # 文档
├── models/                           # 模型文件
├── scripts/                          # 脚本
├── .env                               # 环境变量文件
├── .gitignore                         # Git忽略文件
├── requirements.txt                   # Python依赖
├── package.json                       # 前端依赖
└── README.md                          # 项目说明
```

## 技术栈
### 后端
- Python + FastAPI：作为 API 服务
- LangChain：处理 RAG 逻辑
- ChromaDB：作为向量数据库
- Hugging Face 模型：进行向量化

### 前端
- Vue 3 + Vite：构建用户界面
- Element Plus 或自定义 UI 组件
- Axios：进行 API 请求
- Pinia：管理应用状态

## 安装与运行
### 后端
1. 安装依赖：`pip install -r requirements.txt`
2. 配置环境变量：在 `.env` 文件中填写 API 密钥等信息
3. 运行服务：`uvicorn backend.api.server:app --reload`

### 前端
1. 安装依赖：`npm install`
2. 运行开发服务器：`npm run dev`

## 文档
- `docs/architecture.md`：架构设计
- `docs/development.md`：开发指南
- `docs/deployment.md`：部署说明
- `docs/usage.md`：使用手册