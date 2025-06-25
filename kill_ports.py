#!/usr/bin/env python3
"""
清理占用端口的进程
"""
import subprocess
import sys

def kill_port_process(port):
    """杀死占用指定端口的进程"""
    try:
        # 查找占用端口的进程
        result = subprocess.run([
            "lsof", "-ti", f":{port}"
        ], capture_output=True, text=True)
        
        pids = result.stdout.strip().split('\n')
        
        for pid in pids:
            if pid:
                subprocess.run(["kill", "-9", pid])
                print(f"✅ 已杀死端口 {port} 的进程 PID: {pid}")
                
    except Exception as e:
        print(f"清理端口 {port} 时出错: {e}")

def main():
    print("🧹 清理端口占用...")
    
    # 清理常用端口
    ports = [8080, 5173, 3000]
    
    for port in ports:
        kill_port_process(port)
    
    print("✅ 端口清理完成")

if __name__ == "__main__":
    main()
