#!/usr/bin/env python3
"""
Conversation Compression Script
Compresses long chat histories into concise summaries.
"""

import sys
import json
from datetime import datetime

def compress_conversation(messages, max_rounds=8):
    """
    Compress a conversation history into key summaries.
    
    Args:
        messages: List of message objects
        max_rounds: Maximum rounds before suggesting compression
    
    Returns:
        Compressed summary
    """
    if len(messages) <= max_rounds:
        return None, "Conversation is still concise"
    
    # Extract key points
    key_points = []
    decisions = []
    action_items = []
    
    for msg in messages:
        content = msg.get('content', '')
        
        # Look for decisions
        if any(keyword in content.lower() for keyword in ['决定', '决定了', '同意', '好的，', '行，']):
            decisions.append(content)
        
        # Look for action items
        if any(keyword in content.lower() for keyword in ['帮我', '我需要', '要做', 'todo', '任务']):
            action_items.append(content)
        
        # Extract significant content
        if len(content) > 50:
            key_points.append(content[:100] + "..." if len(content) > 100 else content)
    
    # Build summary
    summary = {
        'compressed_at': datetime.now().isoformat(),
        'original_rounds': len(messages),
        'key_decisions': decisions[-5:],  # Last 5 decisions
        'action_items': action_items[-5:],  # Last 5 action items
        'significant_points': key_points[-10:]  # Last 10 key points
    }
    
    return summary, f"Compressed {len(messages)} rounds to key summary"

def format_summary(summary):
    """Format the compressed summary for readability."""
    if not summary:
        return ""
    
    output = []
    output.append("## 📋 Conversation Summary")
    output.append(f"*Compressed from {summary['original_rounds']} rounds*")
    output.append("")
    
    if summary['key_decisions']:
        output.append("### 🎯 Key Decisions:")
        for decision in summary['key_decisions']:
            output.append(f"- {decision}")
        output.append("")
    
    if summary['action_items']:
        output.append("### ✅ Action Items:")
        for item in summary['action_items']:
            output.append(f"- {item}")
        output.append("")
    
    if summary['significant_points']:
        output.append("### 💡 Key Points:")
        for point in summary['significant_points']:
            output.append(f"- {point}")
    
    return "\n".join(output)

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        # Read from file
        import json
        with open(sys.argv[1], 'r') as f:
            messages = json.load(f)
    else:
        # Demo data
        messages = [
            {'content': '我们来创建一个节省tokens的技能'},
            {'content': '好的，我来帮你设计'},
            {'content': '这个技能应该能够压缩对话历史'},
            {'content': '同意，我们需要提取关键点'},
            {'content': '帮我写一个压缩脚本'},
            {'content': '好的，我来创建'},
            {'content': '脚本应该支持自动压缩'},
            {'content': '没问题，我会添加这个功能'},
            {'content': '太好了，这样我们就能节省很多tokens了'},
            {'content': '是的，这会很有帮助'}
        ]
    
    summary, message = compress_conversation(messages)
    if summary:
        print(format_summary(summary))
    else:
        print(message)
