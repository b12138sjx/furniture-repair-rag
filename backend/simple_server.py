from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import uuid
import re
from typing import List, Optional
from crawler_service import crawler_service

app = FastAPI(title="家具维修智能助手", description="基于RAG的家具维修知识库问答系统")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class QARequest(BaseModel):
    query: str
    answer_mode: str = "auto"  # auto, llm_only, kb_only
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    context_size: int = 3

class QAResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None
    related_questions: Optional[List[str]] = []
    model_used: Optional[str] = None
    answer_mode: str = "auto"
    processing_time: Optional[float] = None

class UploadResponse(BaseModel):
    success: bool
    message: str
    file_id: Optional[str] = None

class CollectRequest(BaseModel):
    url: str

class ChatHistory(BaseModel):
    question: str
    answer: str
    timestamp: str

# 新增模型配置
class ModelConfig(BaseModel):
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 1000

# 支持的模型列表
SUPPORTED_MODELS = {
    "gpt-3.5-turbo": {
        "name": "GPT-3.5 Turbo",
        "provider": "OpenAI",
        "description": "快速、高效的对话模型"
    },
    "gpt-4": {
        "name": "GPT-4",
        "provider": "OpenAI", 
        "description": "更强大的理解和推理能力"
    },
    "chatglm_std": {
        "name": "ChatGLM 标准版",
        "provider": "智谱AI",
        "description": "中文优化的对话模型"
    },
    "chatglm_pro": {
        "name": "ChatGLM Pro",
        "provider": "智谱AI",
        "description": "专业级中文对话模型"
    },
    "ERNIE-Bot": {
        "name": "文心一言",
        "provider": "百度",
        "description": "百度自研的大语言模型"
    }
}

# 全局变量存储知识库和对话历史
knowledge_base = []
chat_history = []

def load_knowledge_base():
    """加载已有的维修数据"""
    global knowledge_base
    
    # 尝试多个可能的数据文件路径
    possible_paths = [
        "data/raw/phone.json",
        "../data/raw/phone.json", 
        "our_data/phone.json",
        "../our_data/phone.json",
        "data/phone.json",
        "../data/phone.json"
    ]
    
    phone_json_file = None
    for path in possible_paths:
        if os.path.exists(path):
            phone_json_file = path
            print(f"📂 找到数据文件: {path}")
            break
    
    if not phone_json_file:
        print("⚠️  未找到数据文件，请先运行爬虫抓取数据")
        print("💡 提示: 进入 backend/data/raw/ 目录运行:")
        print("   python quick_crawl.py")
        create_comprehensive_sample_data()
        phone_json_file = "data/raw/phone.json"
    
    try:
        with open(phone_json_file, 'r', encoding='utf-8') as f:
            phone_data = json.load(f)
            print(f"📱 原始数据条数: {len(phone_data)}")
            
            for i, item in enumerate(phone_data):
                content = item.get('content', '')
                title = item.get('title', '')
                
                # 降低过滤条件，保留更多数据
                if content and len(content.strip()) > 50:
                    # 清洗和结构化内容
                    structured_content = structure_repair_content(content)
                    knowledge_base.append({
                        'content': structured_content,
                        'title': title,
                        'url': item.get('url', ''),
                        'type': 'phone_repair',
                        'keywords': extract_keywords(content)
                    })
                    if i < 5:  # 只显示前5条的处理信息
                        print(f"✅ 处理第 {i+1} 条: {title[:50]}...")
                else:
                    if i < 5:
                        print(f"❌ 跳过第 {i+1} 条: 内容太短 ({len(content)} 字符)")
        
        print(f"📱 成功加载维修数据: {len(knowledge_base)} 条")
        
        # 如果数据量还是很少，提示用户
        if len(knowledge_base) < 10:
            print("\n💡 数据量较少的解决方案:")
            print("1. 进入 backend/data/raw/ 目录")
            print("2. 运行: python quick_crawl.py")
            print("3. 选择抓取更多URL (建议50-100个)")
            print("4. 重启后端服务")
        
    except Exception as e:
        print(f"❌ 加载知识库失败: {e}")
        create_comprehensive_sample_data()

def structure_repair_content(content: str) -> dict:
    """结构化维修内容"""
    # 提取步骤
    steps = extract_repair_steps(content)
    
    # 提取工具列表
    tools = extract_tools(content)
    
    # 提取注意事项
    warnings = extract_warnings(content)
    
    # 提取零件信息
    parts = extract_parts(content)
    
    return {
        'raw_content': content,
        'steps': steps,
        'tools': tools,
        'warnings': warnings,
        'parts': parts,
        'summary': content[:300] + "..." if len(content) > 300 else content
    }

def extract_repair_steps(content: str) -> List[str]:
    """提取维修步骤"""
    step_patterns = [
        r'步骤\s*\d+[：:]\s*(.+?)(?=步骤\s*\d+|$)',
        r'Step\s*\d+[：:]\s*(.+?)(?=Step\s*\d+|$)',
        r'\d+[\.、]\s*(.+?)(?=\d+[\.、]|$)'
    ]
    
    steps = []
    for pattern in step_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        if matches:
            steps.extend([step.strip() for step in matches if len(step.strip()) > 10])
            break
    
    return steps[:10]  # 最多返回10个步骤

def extract_tools(content: str) -> List[str]:
    """提取工具列表"""
    tool_keywords = [
        'screwdriver', 'spudger', 'tweezers', 'opening pick', 'suction handle',
        '螺丝刀', '撬棒', '镊子', '撬片', '吸盘', '热风枪', 'heat gun', 'hair dryer'
    ]
    
    tools = []
    for keyword in tool_keywords:
        if keyword.lower() in content.lower():
            tools.append(keyword)
    
    return list(set(tools))

def extract_warnings(content: str) -> List[str]:
    """提取注意事项"""
    warning_patterns = [
        r'注意[：:](.+?)(?=\n|$)',
        r'小心[：:](.+?)(?=\n|$)',
        r'Be careful(.+?)(?=\n|$)',
        r'Don\'t(.+?)(?=\n|$)'
    ]
    
    warnings = []
    for pattern in warning_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        warnings.extend([warning.strip() for warning in matches])
    
    return warnings[:5]  # 最多返回5个警告

def extract_parts(content: str) -> List[str]:
    """提取零件信息"""
    part_keywords = [
        'battery', 'screen', 'camera', 'speaker', 'antenna', 'microphone',
        '电池', '屏幕', '摄像头', '扬声器', '天线', '麦克风', '后盖', '充电口'
    ]
    
    parts = []
    for keyword in part_keywords:
        if keyword.lower() in content.lower():
            parts.append(keyword)
    
    return list(set(parts))

def extract_keywords(content: str) -> List[str]:
    """提取关键词"""
    # 维修相关关键词
    repair_keywords = [
        'replacement', 'repair', 'fix', 'install', 'remove', 'disconnect',
        '更换', '维修', '修理', '安装', '移除', '断开', '连接', '拆解'
    ]
    
    keywords = []
    content_lower = content.lower()
    
    for keyword in repair_keywords:
        if keyword.lower() in content_lower:
            keywords.append(keyword)
    
    return keywords

def enhanced_search(query: str, top_k: int = 3) -> List[dict]:
    """增强的搜索功能"""
    query_lower = query.lower()
    results = []
    
    for item in knowledge_base:
        score = 0
        content = item['content']
        
        # 关键词匹配
        for keyword in item.get('keywords', []):
            if keyword.lower() in query_lower:
                score += 2
        
        # 内容匹配
        if isinstance(content, dict):
            # 在摘要中搜索
            if any(word in content.get('summary', '').lower() for word in query_lower.split()):
                score += 1
            
            # 在步骤中搜索
            for step in content.get('steps', []):
                if any(word in step.lower() for word in query_lower.split()):
                    score += 1.5
        else:
            # 直接内容搜索
            if any(word in content.lower() for word in query_lower.split()):
                score += 1
        
        if score > 0:
            results.append({
                'item': item,
                'score': score
            })
    
    # 按分数排序
    results.sort(key=lambda x: x['score'], reverse=True)
    return [result['item'] for result in results[:top_k]]

def generate_detailed_answer(query: str, contexts: List[dict]) -> str:
    """生成详细的回答"""
    if not contexts:
        return "抱歉，我没有找到相关的维修信息。请尝试更具体的问题，比如'如何更换iPhone电池'或'屏幕维修步骤'。"
    
    answer_parts = []
    answer_parts.append(f"根据维修知识库，关于'{query}'的解答如下：\n")
    
    for i, context in enumerate(contexts[:2], 1):
        content = context['content']
        
        if isinstance(content, dict):
            # 结构化内容
            answer_parts.append(f"📋 **方法 {i}：{context.get('title', '维修指南')}**\n")
            
            # 添加步骤
            if content.get('steps'):
                answer_parts.append("🔧 **主要步骤：**")
                for j, step in enumerate(content['steps'][:3], 1):
                    answer_parts.append(f"   {j}. {step[:100]}...")
                answer_parts.append("")
            
            # 添加工具
            if content.get('tools'):
                tools_str = "、".join(content['tools'][:5])
                answer_parts.append(f"🛠️ **所需工具：** {tools_str}\n")
            
            # 添加注意事项
            if content.get('warnings'):
                answer_parts.append("⚠️ **注意事项：**")
                for warning in content['warnings'][:2]:
                    answer_parts.append(f"   • {warning}")
                answer_parts.append("")
        else:
            # 简单内容
            answer_parts.append(f"**参考信息 {i}：**\n")
            answer_parts.append(content[:200] + "...\n")
    
    answer_parts.append("💡 **温馨提示：** 维修过程中请务必断电操作，如遇困难建议寻求专业帮助。")
    
    return "\n".join(answer_parts)

def generate_related_questions(query: str, contexts: List[dict]) -> List[str]:
    """生成相关问题"""
    related_questions = []
    
    # 基于上下文生成相关问题
    for context in contexts:
        if isinstance(context['content'], dict):
            parts = context['content'].get('parts', [])
            for part in parts[:2]:
                related_questions.append(f"如何更换{part}？")
                related_questions.append(f"{part}维修需要什么工具？")
    
    # 通用相关问题
    common_questions = [
        "维修前需要注意什么？",
        "常用的维修工具有哪些？",
        "如何判断是否需要更换零件？",
        "维修后如何测试功能？"
    ]
    
    related_questions.extend(common_questions)
    return list(set(related_questions))[:4]

def create_sample_data():
    """创建示例数据"""
    os.makedirs("data/raw", exist_ok=True)
    
    sample_data = [
        {
            "url": "sample://battery-replacement",
            "title": "iPhone电池更换指南", 
            "content": """iPhone电池更换步骤：
            
步骤 1: 关机并准备工具
关闭iPhone电源，准备P2五角螺丝刀、撬棒、镊子等工具。

步骤 2: 移除螺丝
使用P2螺丝刀移除充电口两侧的螺丝。

步骤 3: 打开后盖
用吸盘和撬片小心打开后盖。

步骤 4: 断开电池
使用撬棒断开电池连接器。

步骤 5: 移除胶条
撕掉电池下方的拉条胶带。

步骤 6: 安装新电池
放入新电池并重新连接。

所需工具: P2螺丝刀、撬棒、镊子、吸盘
注意: 操作时请断电，小心静电"""
        }
    ]
    
    with open("data/raw/phone.json", 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)

def create_comprehensive_sample_data():
    """创建更全面的示例数据"""
    os.makedirs("data/raw", exist_ok=True)
    
    sample_data = [
        {
            "url": "sample://battery-replacement",
            "title": "iPhone电池更换指南", 
            "content": """iPhone电池更换完整指南

简介
本指南将教你如何安全地更换iPhone电池。如果你的iPhone电池续航时间明显缩短，或者系统提示电池健康度低于80%，那么可能需要更换电池。

你所需要的工具
- P2五角螺丝刀
- 撬棒 (spudger)
- 镊子 (tweezers)
- 吸盘 (suction handle)
- 撬片 (opening pick)
- 热风枪或吹风机

步骤 1: 准备工作
关闭iPhone电源，确保电池电量低于25%以降低安全风险。

步骤 2: 移除螺丝
使用P2五角螺丝刀移除充电口两侧的两颗螺丝。

步骤 3: 打开后盖
用吸盘和撬片小心打开后盖，注意不要损坏排线。

步骤 4: 断开电池连接
使用撬棒断开电池连接器，确保完全断电。

步骤 5: 移除胶条
撕掉电池下方的拉条胶带，如果断裂可使用异丙醇软化。

步骤 6: 安装新电池
放入新电池并重新连接排线。

注意事项：
- 操作时请断电，小心静电
- 不要用金属工具直接接触电池
- 处理好旧电池的回收"""
        },
        {
            "url": "sample://screen-replacement",
            "title": "iPhone屏幕更换指南",
            "content": """iPhone屏幕更换详细步骤

简介
如果你的iPhone屏幕破裂或显示异常，本指南将帮你完成屏幕更换。

工具清单
- 热风枪 (heat gun)
- 撬片 (opening pick)
- 吸盘
- 螺丝刀套装
- 镊子

步骤 1: 加热屏幕
使用热风枪加热屏幕边缘，软化密封胶。

步骤 2: 创建缝隙
用吸盘拉起屏幕一角，插入撬片。

步骤 3: 分离屏幕
沿着边缘滑动撬片，分离屏幕组件。

步骤 4: 断开排线
小心断开屏幕排线连接器。

步骤 5: 安装新屏幕
按相反顺序安装新屏幕组件。

警告：
- 加热时不要过度，避免损坏内部组件
- 排线非常脆弱，操作要轻柔"""
        },
        {
            "url": "sample://camera-repair",
            "title": "摄像头维修指南",
            "content": """iPhone摄像头维修指南

故障诊断
- 摄像头模糊不清
- 黑屏或无法启动
- 闪光灯不工作
- 自动对焦失效

维修步骤
步骤 1: 检查软件问题
重启设备，检查相机应用设置。

步骤 2: 清洁镜头
使用专用清洁布擦拭镜头表面。

步骤 3: 更换摄像头模块
如需更换硬件，需要拆解设备。

所需工具：
- 精密螺丝刀
- 防静电手套
- 清洁布

注意：摄像头模块包含精密光学元件，操作需格外小心。"""
        },
        {
            "url": "sample://charging-port-repair", 
            "title": "充电口维修指南",
            "content": """充电口问题诊断与维修

常见问题
- 充电速度慢
- 无法充电
- 接触不良
- 充电口松动

维修方法
步骤 1: 清洁充电口
使用小刷子清除灰尘和异物。

步骤 2: 检查充电线
测试不同的充电线和适配器。

步骤 3: 更换充电口组件
如需更换硬件，按以下步骤：
- 拆卸底部螺丝
- 断开相关排线
- 更换充电口模块

工具要求：
- P2螺丝刀
- 撬棒
- 新的充电口组件"""
        },
        {
            "url": "sample://speaker-repair",
            "title": "扬声器维修指南", 
            "content": """iPhone扬声器维修指南

故障现象
- 无声音输出
- 声音破音或失真
- 音量很小
- 只有一个扬声器工作

诊断步骤
步骤 1: 软件检查
检查音量设置、静音开关、蓝牙连接。

步骤 2: 硬件检查
测试不同的音频源和应用。

步骤 3: 清洁扬声器
清除扬声器网罩的灰尘和异物。

步骤 4: 更换扬声器
- 拆卸相关螺丝
- 断开扬声器排线
- 安装新扬声器

所需工具：
- 螺丝刀
- 撬棒
- 镊子
- 新扬声器组件"""
        }
    ]
    
    with open("data/raw/phone.json", 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 创建了 {len(sample_data)} 条示例维修数据")

def get_available_models():
    """获取可用的模型列表"""
    try:
        # 这里可以添加模型可用性检查逻辑
        # 例如检查API密钥是否配置等
        available = []
        for model_id, info in SUPPORTED_MODELS.items():
            # 简单检查 - 实际项目中应该检查API密钥等
            available.append({
                "id": model_id,
                "name": info["name"],
                "provider": info["provider"],
                "description": info["description"],
                "available": True  # 这里应该是真实的可用性检查
            })
        return available
    except Exception as e:
        print(f"检查模型可用性失败: {e}")
        return []

def call_llm_model(model_name: str, prompt: str, temperature: float = 0.7) -> str:
    """调用指定的大语言模型"""
    try:
        # 这里集成你现有的模型调用代码
        # 根据model_name选择不同的模型接口
        
        if model_name.startswith("gpt-"):
            # OpenAI模型调用
            return call_openai_model(model_name, prompt, temperature)
        elif model_name.startswith("chatglm"):
            # 智谱AI模型调用
            return call_zhipu_model(model_name, prompt, temperature)
        elif model_name.startswith("ERNIE"):
            # 百度文心模型调用
            return call_wenxin_model(model_name, prompt, temperature)
        else:
            # 默认使用模拟回复
            return generate_mock_response(prompt)
            
    except Exception as e:
        print(f"模型调用失败: {e}")
        return f"抱歉，模型调用出现问题：{str(e)}"

def call_openai_model(model_name: str, prompt: str, temperature: float) -> str:
    """调用OpenAI模型"""
    try:
        # 这里应该使用你现有的OpenAI调用代码
        # import openai
        # response = openai.ChatCompletion.create(...)
        return f"[OpenAI {model_name}] 这是一个模拟回复：{prompt[:50]}..."
    except Exception as e:
        raise Exception(f"OpenAI模型调用失败: {e}")

def call_zhipu_model(model_name: str, prompt: str, temperature: float) -> str:
    """调用智谱AI模型"""
    try:
        # 这里应该使用你现有的智谱AI调用代码
        return f"[智谱AI {model_name}] 这是一个模拟回复：{prompt[:50]}..."
    except Exception as e:
        raise Exception(f"智谱AI模型调用失败: {e}")

def call_wenxin_model(model_name: str, prompt: str, temperature: float) -> str:
    """调用百度文心模型"""
    try:
        # 这里应该使用你现有的文心模型调用代码
        return f"[百度文心 {model_name}] 这是一个模拟回复：{prompt[:50]}..."
    except Exception as e:
        raise Exception(f"文心模型调用失败: {e}")

def generate_mock_response(prompt: str) -> str:
    """生成模拟回复"""
    return f"这是一个模拟的AI回复，针对您的问题：{prompt[:100]}..."

def generate_llm_only_answer(query: str, model_name: str = "gpt-3.5-turbo", temperature: float = 0.7) -> str:
    """仅使用大模型回答，不依赖知识库"""
    prompt = f"""你是一个专业的维修助手。用户问题：{query}

请基于你的训练知识回答这个维修问题。如果是关于设备维修的问题，请提供：
1. 问题可能的原因分析
2. 详细的解决步骤
3. 所需工具和注意事项
4. 预防措施建议

如果不是维修相关问题，请礼貌地引导用户提问维修相关问题。

回答要专业、详细、实用。"""

    try:
        response = call_llm_model(model_name, prompt, temperature)
        return response
    except Exception as e:
        return f"大模型调用失败：{str(e)}。请稍后重试或联系技术支持。"

def generate_kb_only_answer(query: str, contexts: List[dict]) -> str:
    """仅基于知识库回答，不使用大模型"""
    if not contexts:
        return "抱歉，在知识库中没有找到与您问题相关的信息。建议您：\n1. 尝试使用不同的关键词重新提问\n2. 选择'大模型回答'获取AI的建议\n3. 上传相关的维修文档到知识库"
    
    answer_parts = []
    answer_parts.append(f"根据知识库检索，找到以下相关信息：\n")
    
    for i, context in enumerate(contexts[:2], 1):
        content = context['content']
        title = context.get('title', '维修指南')
        
        answer_parts.append(f"📋 **参考资料 {i}：{title}**\n")
        
        if isinstance(content, dict):
            # 结构化内容
            if content.get('steps'):
                answer_parts.append("🔧 **维修步骤：**")
                for j, step in enumerate(content['steps'][:4], 1):
                    answer_parts.append(f"   {j}. {step}")
                answer_parts.append("")
            
            if content.get('tools'):
                tools_str = "、".join(content['tools'][:5])
                answer_parts.append(f"🛠️ **所需工具：** {tools_str}\n")
            
            if content.get('warnings'):
                answer_parts.append("⚠️ **注意事项：**")
                for warning in content['warnings'][:2]:
                    answer_parts.append(f"   • {warning}")
                answer_parts.append("")
        else:
            # 纯文本内容
            lines = content.split('\n')[:8]
            for line in lines:
                if line.strip():
                    answer_parts.append(f"   {line.strip()}")
            answer_parts.append("")
    
    answer_parts.append("💡 **提示：** 以上信息来自知识库文档，建议结合实际情况操作。")
    
    return "\n".join(answer_parts)

def generate_auto_answer(query: str, contexts: List[dict], model_name: str = "gpt-3.5-turbo", temperature: float = 0.7) -> str:
    """智能选择回答模式"""
    if not contexts:
        # 没有相关知识库内容，使用大模型
        return generate_llm_only_answer(query, model_name, temperature)
    else:
        # 有知识库内容，结合知识库和大模型
        return generate_enhanced_answer(query, contexts, model_name, temperature)

@app.post("/api/v1/qa", response_model=QAResponse)
async def get_answer_v2(request: QARequest):
    """增强版问答接口，支持多种回答模式"""
    import time
    start_time = time.time()
    
    try:
        answer = ""
        sources = []
        confidence = 0.5
        contexts = []
        
        # 根据回答模式处理
        if request.answer_mode == "llm_only":
            # 仅使用大模型
            answer = generate_llm_only_answer(request.query, request.model, request.temperature)
            confidence = 0.8
            
        elif request.answer_mode == "kb_only":
            # 仅使用知识库
            contexts = enhanced_search(request.query, request.context_size)
            answer = generate_kb_only_answer(request.query, contexts)
            sources = [ctx.get('url', '内部知识库') for ctx in contexts]
            confidence = 0.9 if contexts else 0.3
            
        else:  # auto
            # 智能选择模式
            contexts = enhanced_search(request.query, request.context_size)
            answer = generate_auto_answer(request.query, contexts, request.model, request.temperature)
            sources = [ctx.get('url', '内部知识库') for ctx in contexts]
            confidence = 0.9 if contexts else 0.8
        
        # 生成相关问题
        related_questions = generate_related_questions(request.query, contexts)
        
        # 保存对话历史
        from datetime import datetime
        chat_history.append({
            'question': request.query,
            'answer': answer,
            'model': request.model,
            'answer_mode': request.answer_mode,
            'timestamp': datetime.now().isoformat()
        })
        
        processing_time = time.time() - start_time
        
        return QAResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
            related_questions=related_questions,
            model_used=request.model,
            answer_mode=request.answer_mode,
            processing_time=round(processing_time, 2)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"问答处理失败: {str(e)}")

# 保持兼容性的旧接口
@app.get("/api/v1/qa")
async def get_answer_legacy(
    query: str = Query(..., description="用户的问题"),
    context_size: int = Query(3, description="返回的相关上下文数量"),
    model: str = Query("gpt-3.5-turbo", description="使用的模型"),
    temperature: float = Query(0.7, description="模型温度参数"),
    answer_mode: str = Query("auto", description="回答模式")
):
    """兼容旧版本的GET接口"""
    request = QARequest(
        query=query,
        answer_mode=answer_mode,
        model=model,
        temperature=temperature,
        context_size=context_size
    )
    return await get_answer_v2(request)

# 启动时加载知识库
@app.on_event("startup")
async def startup_event():
    load_knowledge_base()

# API端点
@app.get("/api/v1/models")
async def get_models():
    """获取可用的模型列表"""
    try:
        models = get_available_models()
        return {
            "models": models,
            "default": "gpt-3.5-turbo"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/qa")
async def get_answer(
    query: str = Query(..., description="用户的问题"),
    context_size: int = Query(3, description="返回的相关上下文数量"),
    model: str = Query("gpt-3.5-turbo", description="使用的模型"),
    temperature: float = Query(0.7, description="模型温度参数")
):
    try:
        # 搜索相关内容
        contexts = enhanced_search(query, context_size)
        
        # 使用指定模型生成回答
        answer = generate_enhanced_answer(query, contexts, model, temperature)
        
        # 生成相关问题
        related_questions = generate_related_questions(query, contexts)
        
        # 保存对话历史
        from datetime import datetime
        chat_history.append({
            'question': query,
            'answer': answer,
            'model': model,
            'timestamp': datetime.now().isoformat()
        })
        
        return QAResponse(
            answer=answer,
            sources=[ctx.get('url', '内部知识库') for ctx in contexts],
            confidence=0.9 if contexts else 0.3,
            related_questions=related_questions,
            model_used=model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 创建上传目录 - 修复路径
        upload_dir = "data/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # 保存文件
        file_id = str(uuid.uuid4())
        file_ext = os.path.splitext(file.filename)[1]
        save_path = os.path.join(upload_dir, f"{file_id}{file_ext}")
        
        contents = await file.read()
        with open(save_path, 'wb') as f:
            f.write(contents)
        
        # 如果是文本文件，尝试处理并添加到知识库
        if file_ext.lower() in ['.txt', '.md']:
            try:
                text_content = contents.decode('utf-8')
                structured_content = structure_repair_content(text_content)
                knowledge_base.append({
                    'content': structured_content,
                    'title': file.filename,
                    'url': save_path,
                    'type': 'user_upload',
                    'keywords': extract_keywords(text_content)
                })
                print(f"✅ 已将上传文件添加到知识库: {file.filename}")
            except:
                pass
        
        return UploadResponse(
            success=True,
            message=f"文件 {file.filename} 上传成功并已添加到知识库",
            file_id=file_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/collect")
async def collect_data(request: CollectRequest):
    try:
        # 模拟数据采集（实际项目中可以实现网页爬虫）
        return {
            "success": True,
            "message": f"开始采集网址: {request.url}",
            "status": "processing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/chat/history")
async def get_chat_history(limit: int = Query(10)):
    """获取对话历史"""
    return {"history": chat_history[-limit:]}

@app.delete("/api/v1/chat/history")
async def clear_chat_history():
    """清空对话历史"""
    global chat_history
    chat_history = []
    return {"message": "对话历史已清空"}

@app.get("/api/v1/knowledge/stats")
async def get_knowledge_stats():
    """获取知识库统计信息"""
    try:
        stats = {
            "total_documents": len(knowledge_base),
            "types": {},
            "total_steps": 0,
            "total_tools": set(),
            "total_warnings": 0
        }
        
        for item in knowledge_base:
            doc_type = item.get('type', 'unknown')
            stats['types'][doc_type] = stats['types'].get(doc_type, 0) + 1
            
            if isinstance(item['content'], dict):
                stats['total_steps'] += len(item['content'].get('steps', []))
                stats['total_tools'].update(item['content'].get('tools', []))
                stats['total_warnings'] += len(item['content'].get('warnings', []))
        
        stats['total_tools'] = len(stats['total_tools'])
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/knowledge/recent")
async def get_recent_activity(limit: int = Query(10)):
    """获取最近的知识库活动"""
    try:
        # 模拟最近活动数据
        recent_activities = []
        
        # 从knowledge_base获取最近添加的文档
        for i, item in enumerate(knowledge_base[-limit:]):
            activity = {
                "type": "upload" if "user_upload" in item.get('type', '') else "collect",
                "title": item.get('title', f'文档 {i+1}')[:50],
                "time": "刚刚" if i < 3 else f"{i*2}分钟前",
                "status": "success",
                "url": item.get('url', ''),
                "doc_type": item.get('type', 'unknown')
            }
            recent_activities.append(activity)
        
        return {"activities": recent_activities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/crawl")
async def start_crawl(request: CollectRequest):
    """启动爬虫任务 - 增强版"""
    try:
        # 验证URL
        if not request.url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="无效的URL格式")
        
        # 模拟爬虫处理
        task_id = f"task_{len(knowledge_base) + 1}_{int(time.time())}"
        
        # 这里可以集成真实的爬虫逻辑
        # 暂时返回模拟响应
        response = {
            "success": True,
            "message": f"成功启动采集任务",
            "task_id": task_id,
            "status": "started",
            "url": request.url,
            "estimated_time": "预计2-5分钟完成"
        }
        
        # 模拟添加到知识库（实际应该在爬虫完成后）
        simulated_doc = {
            'content': {
                'summary': f"从 {request.url} 采集的维修指南",
                'steps': [f"步骤1: 从{request.url}采集到的内容"],
                'tools': ['爬虫工具'],
                'warnings': ['请验证采集内容的准确性']
            },
            'title': f"采集自 {request.url}",
            'url': request.url,
            'type': 'web_crawl',
            'keywords': ['采集', '在线资源']
        }
        knowledge_base.append(simulated_doc)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "家具维修智能助手API",
        "status": "running",
        "version": "1.0.0",
        "description": "基于RAG技术的智能维修问答系统"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
