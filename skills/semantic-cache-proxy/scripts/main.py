#!/usr/bin/env python3
"""
语义缓存省Token技能主脚本
使用轻量级的gensim模型替代sentence-transformers，避免安装大型PyTorch依赖包
"""

import redis
import numpy as np
import gensim
import gensim.downloader as api
import json
from datetime import datetime, timedelta
import hashlib
import jieba

# 配置
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
EXPIRE_TIME = 24 * 60 * 60  # 24小时
THRESHOLD = 0.85  # 语义相似度阈值

# 初始化
try:
    # 尝试加载轻量级的语义模型
    model = api.load("glove-twitter-25")
except:
    model = None

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def text_to_vector(text):
    """
    将文本转换为语义向量
    """
    try:
        # 使用jieba对中文进行分词
        tokens = list(jieba.cut(text))
        vectors = [model[token] for token in tokens if token in model]
        
        if vectors:
            return np.mean(vectors, axis=0).tolist()
        else:
            return None
    except:
        return None

def calculate_similarity(vec1, vec2):
    """
    计算两个向量的余弦相似度
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)

def find_similar_queries(text_vector, threshold=THRESHOLD):
    """
    在Redis中查找与给定向量相似度≥阈值的查询
    """
    similar_queries = []
    
    # 获取所有存储的查询向量
    for key in r.keys("query:*"):
        query_text = key.decode().split(":")[1]
        stored_vector = json.loads(r.get(f"vector:{query_text}"))
        similarity = calculate_similarity(text_vector, stored_vector)
        
        if similarity >= threshold:
            response = r.get(f"response:{query_text}")
            if response:
                response = response.decode()
            
            similar_queries.append({
                "query": query_text,
                "similarity": similarity,
                "response": response
            })
    
    # 按相似度排序
    similar_queries.sort(key=lambda x: x["similarity"], reverse=True)
    
    return similar_queries

def cache_query_response(query, response):
    """
    缓存查询和响应
    """
    vector = text_to_vector(query)
    
    if vector:
        # 存储查询文本、向量和响应
        r.set(f"query:{query}", query)
        r.set(f"vector:{query}", json.dumps(vector))
        r.set(f"response:{query}", response)
        
        # 设置过期时间
        r.expire(f"query:{query}", EXPIRE_TIME)
        r.expire(f"vector:{query}", EXPIRE_TIME)
        r.expire(f"response:{query}", EXPIRE_TIME)

def is_cache_enabled():
    """
    检查缓存是否启用
    """
    enabled = r.get("cache_enabled")
    return enabled is None or enabled.decode() == "true"

def set_cache_enabled(enabled):
    """
    启用或禁用缓存
    """
    r.set("cache_enabled", "true" if enabled else "false")

def clear_cache():
    """
    清除所有缓存
    """
    for key in r.keys("query:*"):
        r.delete(key)
    for key in r.keys("vector:*"):
        r.delete(key)
    for key in r.keys("response:*"):
        r.delete(key)
    print("Cache cleared")

def main(text):
    """
    主函数：处理查询
    """
    if not is_cache_enabled() or not model:
        return None
    
    text_vector = text_to_vector(text)
    
    if text_vector:
        similar_queries = find_similar_queries(text_vector)
        
        if similar_queries:
            return similar_queries[0]["response"]
    
    return None

if __name__ == "__main__":
    # 测试
    query1 = "北京天气怎么样"
    response1 = "北京今天天气晴朗，最高气温25℃，最低气温15℃"
    cache_query_response(query1, response1)
    
    query2 = "北京的天气如何"
    result = main(query2)
    
    print(f"Query: {query2}")
    print(f"Result: {result}")