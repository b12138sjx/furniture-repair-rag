#!/usr/bin/env python3
"""
测试爬虫功能
"""
import os
import sys

def test_crawler():
    print("🕷️ 测试爬虫功能...")
    
    # 切换到后端目录
    os.chdir("backend")
    
    # 导入爬虫服务
    from crawler_service import crawler_service
    
    # 1. 检查爬虫状态
    print("\n📊 检查爬虫状态...")
    status = crawler_service.get_crawler_status()
    print(f"数据文件存在: {status['data_file_exists']}")
    print(f"链接文件存在: {status['urls_file_exists']}")
    print(f"数据条数: {status['data_count']}")
    print(f"链接数量: {status['urls_count']}")
    
    # 2. 如果数据不存在，运行爬虫
    if not status['data_file_exists'] or status['data_count'] == 0:
        print("\n🚀 运行爬虫获取数据...")
        result = crawler_service.run_crawler()
        
        if result['success']:
            print("✅ 爬虫运行成功!")
            print(result['message'])
        else:
            print("❌ 爬虫运行失败:")
            print(result['message'])
            return False
    
    # 3. 加载数据测试
    print("\n📖 测试数据加载...")
    data = crawler_service.load_crawled_data()
    print(f"成功加载 {len(data)} 条数据")
    
    if data:
        print("📋 数据样例:")
        sample = data[0]
        print(f"  标题: {sample.get('title', '')[:50]}...")
        print(f"  URL: {sample.get('url', '')}")
        print(f"  内容长度: {len(sample.get('content', ''))} 字符")
    
    return True

if __name__ == "__main__":
    success = test_crawler()
    if success:
        print("\n🎉 爬虫测试完成！现在可以启动后端服务:")
        print("python simple_server.py")
    else:
        print("\n❌ 爬虫测试失败，请检查网络连接和配置")
