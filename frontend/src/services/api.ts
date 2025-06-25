import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8080/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求接口定义
export interface QARequest {
  query: string
  answer_mode: 'auto' | 'llm_only' | 'kb_only'
  model: string
  temperature: number
  context_size: number
}

// 响应接口定义
export interface QAResponse {
  answer: string
  sources?: string[]
  confidence?: number
  related_questions?: string[]
  model_used?: string
  answer_mode: string
  processing_time?: number
}

export interface ModelInfo {
  id: string
  name: string
  provider: string
  description: string
  available: boolean
}

export interface ModelsResponse {
  models: ModelInfo[]
  default: string
}

// 获取可用模型列表
export const getAvailableModels = async (): Promise<ModelsResponse> => {
  try {
    const response = await api.get('/models')
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || '获取模型列表失败')
  }
}

// 问答API - 支持模型选择
export const askQuestion = async (
  query: string, 
  contextSize: number = 3,
  model: string = 'gpt-3.5-turbo',
  temperature: number = 0.7
): Promise<QAResponse> => {
  try {
    const response = await api.get('/qa', {
      params: {
        query,
        context_size: contextSize,
        model,
        temperature
      }
    })
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || '请求失败')
  }
}

// 增强版问答API
export const askQuestionV2 = async (request: QARequest): Promise<QAResponse> => {
  try {
    const response = await api.post('/qa', request)
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || '请求失败')
  }
}

// 文件上传API
export const uploadFile = async (file: File): Promise<UploadResponse> => {
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || '上传失败')
  }
}

// 爬虫状态API
export const getCrawlerStatus = async (): Promise<any> => {
  try {
    const response = await api.get('/crawler/status')
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || '获取状态失败')
  }
}

// 数据采集API (修复)
export const collectData = async (url: string): Promise<any> => {
  try {
    const response = await api.post('/crawl', {
      url
    })
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || '采集失败')
  }
}

// 备用采集API
export const collectDataAlt = async (url: string): Promise<any> => {
  try {
    const response = await api.post('/collect', {
      url
    })
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || '采集失败')
  }
}

// 知识库统计API
export const getKnowledgeStats = async (): Promise<any> => {
  try {
    const response = await api.get('/knowledge/stats')
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || '获取统计失败')
  }
}

// 最近活动API
export const getRecentActivity = async (limit: number = 10): Promise<any> => {
  try {
    const response = await api.get('/knowledge/recent', {
      params: { limit }
    })
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || '获取活动记录失败')
  }
}

// 增强的数据采集API
export const collectDataEnhanced = async (url: string): Promise<any> => {
  try {
    const response = await api.post('/crawl', { url })
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || '采集失败')
  }
}

export default api
