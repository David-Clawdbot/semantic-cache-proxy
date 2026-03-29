#!/usr/bin/env python3
"""
Model Auto-Switching Script
Automatically selects optimal models based on task complexity.
"""

import sys
import json
from enum import Enum
from typing import Dict, List, Tuple

class TaskComplexity(Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"

class ModelSelector:
    def __init__(self):
        # Model configuration - can be customized
        self.model_mapping = {
            TaskComplexity.SIMPLE: {
                "model": "glm-4.6v-FlashX",
                "cost_multiplier": 0.5,
                "description": "Fast, cost-effective model for simple tasks"
            },
            TaskComplexity.MEDIUM: {
                "model": "glm-4.6v",
                "cost_multiplier": 1.0,
                "description": "Balanced model for medium complexity"
            },
            TaskComplexity.COMPLEX: {
                "model": "gpt-4.5v",
                "cost_multiplier": 2.0,
                "description": "High-performance model for complex tasks"
            }
        }
        
        # Simple task indicators
        self.simple_indicators = [
            "hello", "hi", "你好", "谢谢", "thanks",
            "what time", "几点", "天气", "weather",
            "简单", "simple", "quick", "快速",
            "yes", "no", "是", "不是",
            "确认", "confirm", "check", "检查"
        ]
        
        # Complex task indicators
        self.complex_indicators = [
            "写代码", "write code", "program", "编程",
            "设计", "design", "architecture", "架构",
            "分析", "analyze", "research", "研究",
            "复杂", "complex", "difficult", "困难",
            "优化", "optimize", "refactor", "重构",
            "创建", "create", "build", "构建"
        ]
    
    def analyze_task_complexity(self, user_input: str) -> TaskComplexity:
        """
        Analyze the complexity of a user's task.
        
        Args:
            user_input: The user's input text
            
        Returns:
            TaskComplexity enum value
        """
        input_lower = user_input.lower()
        
        # Check for complex indicators first
        for indicator in self.complex_indicators:
            if indicator in input_lower:
                return TaskComplexity.COMPLEX
        
        # Check for simple indicators
        for indicator in self.simple_indicators:
            if indicator in input_lower:
                return TaskComplexity.SIMPLE
        
        # Check input length
        if len(user_input) < 50:
            return TaskComplexity.SIMPLE
        elif len(user_input) < 200:
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.COMPLEX
    
    def select_model(self, user_input: str) -> Tuple[str, Dict]:
        """
        Select the optimal model for a given task.
        
        Args:
            user_input: The user's input text
            
        Returns:
            Tuple of (model_name, model_info)
        """
        complexity = self.analyze_task_complexity(user_input)
        model_info = self.model_mapping[complexity]
        
        return model_info["model"], {
            "complexity": complexity.value,
            **model_info
        }
    
    def calculate_savings(self, complexity: TaskComplexity) -> Dict:
        """
        Calculate potential cost savings.
        
        Args:
            complexity: The task complexity
            
        Returns:
            Savings information
        """
        # Assume using complex model by default
        default_cost = self.model_mapping[TaskComplexity.COMPLEX]["cost_multiplier"]
        actual_cost = self.model_mapping[complexity]["cost_multiplier"]
        
        savings_percent = ((default_cost - actual_cost) / default_cost) * 100
        
        return {
            "default_cost_multiplier": default_cost,
            "actual_cost_multiplier": actual_cost,
            "savings_percent": round(savings_percent, 1),
            "estimated_monthly_savings": f"~{savings_percent:.0f}%" if savings_percent > 0 else "None"
        }

def main():
    selector = ModelSelector()
    
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        # Demo with different inputs
        test_inputs = [
            "你好",
            "帮我写一个Python脚本",
            "简单的问题",
            "设计一个复杂的系统架构"
        ]
        
        print("=== Model Auto-Switching Demo ===\n")
        
        for input_text in test_inputs:
            model, info = selector.select_model(input_text)
            savings = selector.calculate_savings(TaskComplexity(info["complexity"]))
            
            print(f"Input: {input_text}")
            print(f"Selected Model: {model}")
            print(f"Complexity: {info['complexity']}")
            print(f"Cost Savings: {savings['savings_percent']}%")
            print("-" * 50)
        
        return
    
    # Single input mode
    model, info = selector.select_model(user_input)
    savings = selector.calculate_savings(TaskComplexity(info["complexity"]))
    
    print(f"Selected Model: {model}")
    print(f"Task Complexity: {info['complexity']}")
    print(f"Description: {info['description']}")
    print(f"Estimated Savings: {savings['savings_percent']}%")

if __name__ == "__main__":
    main()
