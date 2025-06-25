#!/usr/bin/env python3
"""
简化版启动脚本
"""
import uvicorn
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 启动家具维修助手后端服务...")
    print("📍 服务地址: http://localhost:8080")
    print("📝 API文档: http://localhost:8080/docs")
    print("❌ 停止服务: Ctrl+C")
    print("-" * 50)
    
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
