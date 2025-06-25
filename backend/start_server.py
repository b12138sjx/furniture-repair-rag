#!/usr/bin/env python3
"""
家具维修助手后端启动脚本
"""
import os
import sys

def check_requirements():
    """检查运行环境"""
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_data_files():
    """检查数据文件"""
    data_paths = [
        "data/raw/phone.json",
        "../our_data/phone.json", 
        "our_data/phone.json",
        "data/phone.json"
    ]
    
    for path in data_paths:
        if os.path.exists(path):
            print(f"✅ 找到数据文件: {path}")
            return True
    
    print("⚠️  未找到数据文件，系统将使用默认数据")
    return False

def main():
    print("🚀 启动家具维修助手后端服务...")
    print("=" * 50)
    
    # 检查环境
    if not check_requirements():
        return
    
    # 检查数据
    check_data_files()
    
    # 创建必要目录
    os.makedirs("data/uploads", exist_ok=True)
    os.makedirs("data/raw", exist_ok=True)
    
    print("📍 服务地址: http://localhost:8080")
    print("📝 API文档: http://localhost:8080/docs")
    print("❌ 停止服务: Ctrl+C")
    print("=" * 50)
    
    # 启动服务
    import uvicorn
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
