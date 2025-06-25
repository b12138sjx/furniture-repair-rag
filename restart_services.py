#!/usr/bin/env python3
"""
重启前后端服务
"""
import subprocess
import sys
import time

def main():
    print("🔄 重启服务...")
    
    # 1. 清理端口
    print("🧹 清理端口...")
    subprocess.run([sys.executable, "kill_ports.py"])
    
    # 2. 清理前端依赖
    print("🧹 清理前端依赖...")
    subprocess.run([
        "rm", "-rf", 
        "frontend/node_modules",
        "frontend/package-lock.json"
    ])
    
    # 3. 重新安装前端依赖
    print("📦 重新安装前端依赖...")
    subprocess.run([
        "npm", "install", "--prefix", "frontend"
    ])
    
    # 4. 启动服务
    print("🚀 启动服务...")
    time.sleep(2)
    subprocess.run([sys.executable, "start_all.py"])

if __name__ == "__main__":
    main()
