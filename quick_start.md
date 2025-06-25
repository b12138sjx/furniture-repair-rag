# 🚀 快速启动指南

## 方式一：分别启动（推荐）

### 1. 启动后端
```bash
python run_backend.py
```
等待看到 "Application startup complete" 消息

### 2. 启动前端（新终端）
```bash
python run_frontend.py  
```

## 方式二：一键启动
```bash
python start_all.py
```

## 方式三：手动启动

### 后端
```bash
cd backend
pip install fastapi uvicorn python-multipart pydantic
python simple_server.py
```

### 前端
```bash
cd frontend  
npm install
npm run dev
```

## 验证启动

1. 后端API: http://localhost:8080
2. 前端界面: http://localhost:5173
3. API文档: http://localhost:8080/docs

## 常见问题

### 端口冲突
- 后端默认8080端口
- 前端默认5173端口
- 如冲突请修改端口号

### 依赖问题
```bash
# Python依赖
pip install -r backend/requirements.txt

# Node.js依赖  
cd frontend && npm install
```

### 数据文件
系统会自动创建示例数据，也可手动放置到 `backend/data/raw/` 目录
