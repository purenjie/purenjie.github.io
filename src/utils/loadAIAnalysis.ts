/**
 * Load AI analysis data for a blog post from cache
 * 
 * This utility reads the AI-generated analysis data for a given blog post
 * by looking up the cache file mapping in manifest.json
 */

import fs from 'node:fs'
import path from 'node:path'

export interface AIAnalysisData {
  id: string
  title: string
  date?: string
  tags: string[]
  slug?: string
  path: string
  md5: string
  metrics: {
    sentenceAvgLen: number
    sentenceLenBuckets: Record<string, number>
    readability: Record<string, number | string>
  }
  analysis?: string
  style: {
    tone: Record<string, number>
    rhythm?: string
    tropes: string[]
  }
  content: {
    keywords: string[]
    concepts: string[]
  }
  sentiment: {
    label?: string
    score?: number
  }
  stance: Record<string, string | null>
  structure: {
    pattern?: string
    opening?: string
    closing?: string
  }
  depth?: string
  diagnostics: {
    llm_raw?: string
    warnings: string[]
  }
}

interface Manifest {
  latest: Record<string, string>
  history: Array<{ path: string; md5: string }>
}

const PROJECT_ROOT = path.join(process.cwd())
const CACHE_DIR = path.join(PROJECT_ROOT, 'scripts', 'ai_analysis', 'cache')
const MANIFEST_PATH = path.join(PROJECT_ROOT, 'scripts', 'ai_analysis', 'manifest.json')

/**
 * Load AI analysis data for a blog post
 * @param postId - The post ID (e.g., "2025-02-23-也许你该买份保险" or "2025-10-31-AI驱动的博客分析系统/index")
 * @returns AI analysis data or null if not found
 */
export function loadAIAnalysis(postId: string): AIAnalysisData | null {
  try {
    // Check if manifest exists
    if (!fs.existsSync(MANIFEST_PATH)) {
      console.warn('[loadAIAnalysis] Manifest file not found:', MANIFEST_PATH)
      return null
    }

    // Read manifest
    const manifestContent = fs.readFileSync(MANIFEST_PATH, 'utf-8')
    const manifest: Manifest = JSON.parse(manifestContent)

    // Find cache file for this post
    // The manifest keys are full paths, so we need to find the matching entry
    const matchingKey = Object.keys(manifest.latest).find(key => {
      // Extract the post identifier from the full path
      // e.g., "/Users/.../blog/src/content/blog/2025-02-23-也许你该买份保险.md"
      // Should match postId "2025-02-23-也许你该买份保险"
      const pathParts = key.split('/')
      const fileName = pathParts[pathParts.length - 1]
      
      // Handle both .md files and index.md in folders
      if (fileName === 'index.md') {
        const folderName = pathParts[pathParts.length - 2]
        return postId.includes(folderName) || folderName === postId.replace('/index', '')
      } else {
        const fileNameWithoutExt = fileName.replace('.md', '')
        return postId.includes(fileNameWithoutExt) || fileNameWithoutExt === postId
      }
    })

    if (!matchingKey) {
      console.warn('[loadAIAnalysis] No cache entry found for post:', postId)
      return null
    }

    const cacheFileName = manifest.latest[matchingKey]
    const cacheFilePath = path.join(CACHE_DIR, cacheFileName)

    // Check if cache file exists
    if (!fs.existsSync(cacheFilePath)) {
      console.warn('[loadAIAnalysis] Cache file not found:', cacheFilePath)
      return null
    }

    // Read and parse cache file
    const cacheContent = fs.readFileSync(cacheFilePath, 'utf-8')
    const analysisData: AIAnalysisData = JSON.parse(cacheContent)

    return analysisData
  } catch (error) {
    console.error('[loadAIAnalysis] Error loading analysis data:', error)
    return null
  }
}

