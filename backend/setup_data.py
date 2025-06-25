"""
数据初始化脚本
"""
import os
import json
import shutil

def setup_data_structure():
    """设置数据目录结构"""
    directories = [
        "data",
        "data/raw", 
        "data/uploads",
        "data/processed"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ 创建目录: {directory}")

def copy_data_files():
    """复制数据文件到正确位置"""
    source_files = [
        ("../our_data/phone.json", "data/raw/phone.json"),
        ("our_data/phone.json", "data/raw/phone.json"),
        ("data/phone.json", "data/raw/phone.json")
    ]
    
    for source, target in source_files:
        if os.path.exists(source):
            shutil.copy2(source, target)
            print(f"✅ 复制文件: {source} -> {target}")
            return True
    
    print("⚠️  未找到源数据文件，创建示例数据...")
    create_sample_data()
    return False

def create_sample_data():
    """创建示例数据"""
    sample_data = [
        {
            "url": "sample://repair-guide-1",
            "title": "手机电池更换指南",
            "content": """手机电池更换指南
            
步骤 1: 关闭手机电源
在开始维修之前，请确保手机完全关机，以避免电击风险。

步骤 2: 准备工具
您需要以下工具：
- 螺丝刀 (screwdriver)
- 撬棒 (spudger) 
- 镊子 (tweezers)
- 吸盘 (suction handle)

步骤 3: 移除后盖
使用吸盘和撬棒小心地移除手机后盖。

步骤 4: 断开电池连接
使用撬棒断开电池连接器。

步骤 5: 更换电池
移除旧电池，安装新电池。

注意：请小心操作，避免损坏其他组件。

警告：操作过程中请勿使用金属工具直接接触电池。
"""
        },
        {
            "url": "sample://repair-guide-2", 
            "title": "屏幕维修指南",
            "content": """屏幕维修指南

步骤 1: 准备工作
确保设备关机，准备必要的维修工具。

步骤 2: 加热屏幕边缘
使用热风枪 (heat gun) 或吹风机 (hair dryer) 加热屏幕边缘。

步骤 3: 移除屏幕
使用撬片 (opening pick) 小心分离屏幕。

所需工具：
- 热风枪
- 撬片
- 螺丝刀
- 镊子

注意事项：
- 小心操作避免二次损伤
- 保持工作区域清洁
"""
        }
    ]
    
    with open("data/raw/phone.json", 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    print("✅ 创建示例数据文件: data/raw/phone.json")

def main():
    print("🔧 设置家具维修助手数据...")
    print("=" * 40)
    
    # 1. 创建目录结构
    setup_data_structure()
    
    # 2. 复制或创建数据文件
    copy_data_files()
    
    print("=" * 40)
    print("✅ 数据初始化完成！")
    print("现在可以启动后端服务了:")
    print("python start_server.py")

if __name__ == "__main__":
    main()
