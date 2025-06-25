#!/usr/bin/env python3
"""
启动前后端服务的主脚本
"""
import os
import sys
import subprocess
import threading
import time
import signal

def kill_existing_processes():
    """杀死占用端口的进程"""
    try:
        # 杀死占用8080端口的进程
        subprocess.run(["pkill", "-f", "uvicorn.*8080"], capture_output=True)
        subprocess.run(["pkill", "-f", "simple_server"], capture_output=True)
        time.sleep(1)
        print("✅ 清理已存在的后端进程")
    except:
        pass

def start_backend():
    """在子线程中启动后端"""
    print("🔧 启动后端服务...")
    os.chdir("backend")
    
    # 创建必要目录
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/uploads", exist_ok=True)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "simple_server:app",
            "--host", "0.0.0.0", 
            "--port", "8080",
            "--reload"
        ])
    except Exception as e:
        print(f"❌ 后端启动失败: {e}")

def start_frontend():
    """在主线程中启动前端"""
    print("🎨 启动前端服务...")
    time.sleep(3)  # 等待后端启动
    
    os.chdir("../frontend")
    
    try:
        subprocess.run(["npm", "run", "dev"])
    except Exception as e:
        print(f"❌ 前端启动失败: {e}")

def main():
    print("🚀 家具维修助手 - 全栈启动")
    print("=" * 50)
    
    # 清理已存在的进程
    kill_existing_processes()
    
    print("📍 后端API: http://localhost:8080")
    print("📍 前端界面: http://localhost:5173") 
    print("📝 API文档: http://localhost:8080/docs")
    print("❌ 停止服务: Ctrl+C")
    print("=" * 50)
    
    # 启动后端（在后台线程）
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # 启动前端（在主线程）
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n👋 服务已停止")

if __name__ == "__main__":
    main()
