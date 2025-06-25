#!/usr/bin/env python3
"""
后端服务启动脚本
"""
import os
import sys
import subprocess

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python版本过低，需要3.9+")
        return False
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """安装依赖"""
    print("📦 检查并安装依赖...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0", 
            "python-multipart==0.0.6",
            "pydantic==2.5.0"
        ], check=True)
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError:
        print("❌ 依赖安装失败")
        return False

def start_backend():
    """启动后端服务"""
    os.chdir("backend")
    
    print("🚀 启动后端服务...")
    print("📍 服务地址: http://localhost:8080")
    print("📝 API文档: http://localhost:8080/docs")
    print("❌ 停止服务: Ctrl+C")
    print("=" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "simple_server:app",
            "--host", "0.0.0.0",
            "--port", "8080", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 后端服务已停止")

def main():
    print("🔧 家具维修助手 - 后端启动")
    print("=" * 40)
    
    if not check_python_version():
        return
        
    if not install_dependencies():
        return
        
    start_backend()

if __name__ == "__main__":
    main()
