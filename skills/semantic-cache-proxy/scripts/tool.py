#!/usr/bin/env python3
"""
语义缓存省Token技能工具脚本
用于实现与OpenClaw系统交互的功能
"""

import sys
import json
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import main

def run():
    """
    主函数
    """
    if len(sys.argv) > 1:
        # 获取输入参数
        args = sys.argv[1:]
        
        if args[0] == "clear":
            # 清除缓存
            main.clear_cache()
            print(json.dumps({"success": True, "message": "Cache cleared"}))
        
        elif args[0] == "toggle":
            # 切换缓存开关
            if len(args) > 1:
                enabled = args[1].lower() == "true"
            else:
                current = main.is_cache_enabled()
                enabled = not current
            
            main.set_cache_enabled(enabled)
            print(json.dumps({"success": True, "cache_enabled": enabled}))
        
        elif args[0] == "status":
            # 获取状态
            enabled = main.is_cache_enabled()
            count = len(list(main.r.keys("query:*")))
            print(json.dumps({"success": True, "cache_enabled": enabled, "cache_count": count}))
        
        elif args[0] == "process":
            # 处理查询
            if len(args) > 1:
                query = " ".join(args[1:])
                result = main.main(query)
                print(json.dumps({"success": True, "result": result}))
            else:
                print(json.dumps({"success": False, "error": "No query provided"}))
        
        elif args[0] == "store":
            # 存储查询结果
            if len(args) > 2:
                query = args[1]
                response = " ".join(args[2:])
                main.cache_query_response(query, response)
                print(json.dumps({"success": True}))
            else:
                print(json.dumps({"success": False, "error": "Invalid parameters"}))
        
        else:
            print(json.dumps({"success": False, "error": "Invalid command"}))
    
    else:
        print(json.dumps({"success": False, "error": "No command provided"}))

if __name__ == "__main__":
    run()
