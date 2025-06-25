# 家具维修 RAG 系统开发指南

## 环境准备
### 后端环境
1. 安装 Python 3.8 及以上版本。
2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
```
3. 安装依赖：
```bash
pip install -r requirements.txt
```

### 前端环境
1. 安装 Node.js 和 npm。
2. 安装项目依赖：
```bash
cd frontend
npm install
```

## 代码结构说明
### 后端
- `backend/data_crawler`：数据爬取模块，包含爬虫脚本和工具函数。
- `backend/data_processor`：数据处理模块，负责文档加载、分块和向量化。
- `backend/models`：模型调用模块，封装大模型接口和 RAG 核心链。
- `backend/api`：API 接口模块，提供与前端交互的接口。
- `backend/config`：配置文件模块，存放系统配置和 API 密钥。

### 前端
- `frontend/src`：源代码目录，包含组件、视图、API 请求和状态管理。
- `frontend/public`：公共资源目录，存放 HTML 文件和图标。
- `frontend/package.json`：前端依赖配置文件。
- `frontend/vite.config.js`：Vite 配置文件。

## 开发流程
### 数据爬取模块开发
1. 在 `backend/data_crawler/furniture_crawler.py` 中添加新的爬取规则。
2. 编写工具函数，优化 HTML 解析和文本清洗逻辑，可在 `backend/data_crawler/utils.py` 中实现。

### 数据处理模块开发
1. 扩展 `backend/data_processor/document_processor.py` 支持更多文档格式。
2. 调整文本分块参数，优化向量化效果，可在 `backend/data_processor/vector_builder.py` 中修改。

### RAG 核心引擎开发
1. 在 `backend/models/llm_interface.py` 中添加新的大模型支持。
2. 优化 `backend/models/rag_chain.py` 中的 Prompt 模板，提高回答质量。

### 前端开发
1. 在 `frontend/src/components` 中添加新的组件。
2. 在 `frontend/src/views` 中创建新的页面。
3. 更新 `frontend/src/api` 中的 API 请求逻辑。

## 调试与测试
### 后端调试
启动 FastAPI 服务：
```bash
uvicorn backend.api.server:app --reload
```
使用 Postman 或 curl 测试 API 接口。

### 前端调试
启动 Vite 开发服务器：
```bash
cd frontend
npm run dev
```
在浏览器中访问 `http://localhost:3000` 进行调试。