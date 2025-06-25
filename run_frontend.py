#!/usr/bin/env python3
"""
前端服务启动脚本
"""
import os
import sys
import subprocess
import shutil

def check_node_version():
    """检查Node.js版本"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✅ Node.js版本: {version}")
        return True
    except FileNotFoundError:
        print("❌ 未找到Node.js，请先安装Node.js")
        return False

def check_npm():
    """检查npm"""
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✅ npm版本: {version}")
        return True
    except FileNotFoundError:
        print("❌ 未找到npm")
        return False

def install_dependencies():
    """安装前端依赖"""
    print("📦 安装前端依赖...")
    
    # 删除可能存在的node_modules和lock文件
    if os.path.exists("node_modules"):
        shutil.rmtree("node_modules")
    
    for lock_file in ["package-lock.json", "yarn.lock"]:
        if os.path.exists(lock_file):
            os.remove(lock_file)
    
    try:
        subprocess.run(["npm", "install"], check=True)
        print("✅ 前端依赖安装完成")
        return True
    except subprocess.CalledProcessError:
        print("❌ 前端依赖安装失败")
        return False

def start_frontend():
    """启动前端服务"""
    os.chdir("frontend")
    
    print("🚀 启动前端服务...")
    print("📍 前端地址: http://localhost:5173")
    print("❌ 停止服务: Ctrl+C")
    print("=" * 50)
    
    try:
        subprocess.run(["npm", "run", "dev"])
    except KeyboardInterrupt:
        print("\n👋 前端服务已停止")

def main():
    print("🎨 家具维修助手 - 前端启动")
    print("=" * 40)
    
    if not check_node_version():
        return
        
    if not check_npm():
        return
        
    if not install_dependencies():
        return
        
    start_frontend()

if __name__ == "__main__":
    main()
