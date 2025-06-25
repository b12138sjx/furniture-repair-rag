# 家具维修 RAG 系统部署说明

## 部署环境要求
### 硬件要求
- 至少 2GB 内存
- 至少 10GB 可用磁盘空间
- 稳定的网络连接

### 软件要求
- 后端
  - Python 3.8 及以上版本
  - 安装所需的 Python 依赖（可通过 `pip install -r requirements.txt` 安装）
- 前端
  - Node.js 16 及以上版本
  - npm 或 yarn 包管理器

## 后端部署步骤
### 1. 克隆项目代码
```bash
git clone <项目仓库地址>
cd furniture-repair-rag
```

### 2. 配置环境变量
复制 `.env.example` 文件并重命名为 `.env`，根据实际情况填写以下环境变量：
```plaintext
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACEHUB_API_TOKEN=your_huggingfacehub_api_token
VECTOR_DB_PATH=./data/processed/vectors
DEFAULT_LLM_MODEL=gpt-3.5-turbo
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 3. 创建虚拟环境并安装依赖
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 4. 启动后端服务
```bash
uvicorn backend.api.server:app --host 0.0.0.0 --port 8000
```

## 前端部署步骤
### 1. 进入前端目录并安装依赖
```bash
cd frontend
npm install
```

### 2. 构建前端项目
```bash
npm run build
```
构建完成后，会在 `frontend/dist` 目录下生成静态文件。

### 3. 部署静态文件
将 `frontend/dist` 目录下的静态文件部署到 Nginx 或 Apache 等 Web 服务器中。以下是一个简单的 Nginx 配置示例：
```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        root /path/to/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 注意事项
- 确保后端服务和前端服务的端口不冲突。
- 在生产环境中，建议使用 HTTPS 协议来保护数据传输安全。
- 定期备份 `data` 目录下的数据，防止数据丢失。