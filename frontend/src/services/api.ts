import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8080/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应接口定义
export interface QAResponse {
  answer: string
  sources?: string[]
  confidence?: number
}

export interface UploadResponse {
  success: boolean
  message: string
  file_id?: string
}

export interface ErrorResponse {
  success: boolean
  error: string
  detail?: string
}

// 问答API
export const askQuestion = async (query: string, contextSize: number = 3): Promise<QAResponse> => {
  try {
    const response = await api.get('/qa', {
      params: {
        query,
        context_size: contextSize
      }
    })
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

export default api
