# 🔧 家具维修智能助手

基于大型语言模型(LLM)和检索增强生成(RAG)技术的个人维修知识库助手

## 📖 项目介绍

本项目是一个智能的家具和设备维修问答系统，通过整合丰富的维修知识库，为用户提供准确、详细的维修指导。系统采用RAG架构，结合向量检索和智能问答，能够理解用户的自然语言查询并提供专业的维修建议。

### 🎯 核心功能

- **智能问答**: 支持自然语言查询，提供详细的维修步骤和指导
- **知识库管理**: 支持多种格式文档上传和智能内容解析
- **数据采集**: 支持从维修网站采集最新的维修指南
- **对话历史**: 保存和管理用户的问答历史记录
- **相关推荐**: 基于当前问题推荐相关的维修问题

### 🏗️ 技术架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vue.js 前端   │    │   FastAPI 后端  │    │   知识库存储    │
│                 │    │                 │    │                 │
│ - 问答界面      │◄──►│ - 问答API       │◄──►│ - JSON格式      │
│ - 文件上传      │    │ - 文件处理      │    │ - 结构化内容    │
│ - 历史记录      │    │ - 智能检索      │    │ - 向量索引      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 快速开始

### 环境要求

- Python >= 3.9
- Node.js >= 16.0
- 内存 >= 4GB

### 1. 克隆项目

```bash
git clone https://github.com/your-repo/furniture-repair-rag.git
cd furniture-repair-rag
```

### 2. 后端启动

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
python simple_server.py
```

### 3. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 4. 访问应用

- 前端界面: http://localhost:5173
- 后端API: http://localhost:8080
- API文档: http://localhost:8080/docs

## 💡 使用指南

### 智能问答

1. 在问答页面输入您的维修问题
2. 系统会智能检索相关的维修知识
3. 获得详细的维修步骤、工具列表和注意事项
4. 查看相关问题推荐

### 知识库管理

1. 上传维修文档(支持PDF、MD、TXT格式)
2. 系统自动解析和结构化内容
3. 查看知识库统计信息

### 数据采集

1. 输入维修网站URL
2. 系统自动采集维修指南
3. 智能清洗和入库

## 📊 项目特色

### 🧠 智能内容解析

- **步骤提取**: 自动识别和提取维修步骤
- **工具识别**: 智能识别所需维修工具
- **注意事项**: 提取重要的安全提醒
- **零件信息**: 识别相关的零部件信息

### 🔍 增强检索

- **关键词匹配**: 基于维修关键词的精准匹配
- **语义搜索**: 理解用户查询意图
- **分数排序**: 智能排序最相关的结果
- **上下文感知**: 考虑维修上下文信息

### 📈 用户体验

- **快捷问题**: 提供常见维修问题快速入口
- **相关推荐**: 基于当前问题的智能推荐
- **评分反馈**: 用户可对回答质量进行评分
- **历史记录**: 保存和查看问答历史

## 🛠️ 技术栈

### 后端技术

- **FastAPI**: 高性能的Python Web框架
- **Pydantic**: 数据验证和序列化
- **JSON**: 轻量级知识库存储
- **正则表达式**: 内容解析和提取

### 前端技术

- **Vue.js 3**: 渐进式JavaScript框架
- **Element Plus**: Vue.js组件库
- **TypeScript**: 类型安全的JavaScript
- **Axios**: HTTP客户端库

## 📁 项目结构

```
furniture-repair-rag/
├── backend/                 # 后端代码
│   ├── simple_server.py    # 简化版API服务器
│   ├── our_data/           # 知识库数据
│   │   ├── phone.json      # 手机维修数据
│   │   └── phone urls.txt  # 维修指南链接
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── services/       # API服务
│   │   └── components/     # 通用组件
│   └── package.json        # NPM依赖
└── README.md               # 项目说明
```

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢 iFixit 提供的优质维修指南数据
- 感谢开源社区提供的技术支持
- 感谢所有贡献者的付出

## 📞 联系我们

如有问题或建议，请联系：
- 邮箱: your-email@example.com
- 项目地址: https://github.com/your-repo/furniture-repair-rag

---

让维修变得更简单！🔧✨