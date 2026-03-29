#!/usr/bin/env python3
"""
Context Window Manager
Manages conversation context to save tokens.
"""

import json
from datetime import datetime
from typing import List, Dict, Tuple

class WindowManager:
    def __init__(self, window_size: int = 8, summary_threshold: int = 12):
        self.window_size = window_size
        self.summary_threshold = summary_threshold
        self.important_messages = set()
        self.summaries = {}
        self.history = []
    
    def add_message(self, message: Dict, is_important: bool = False) -> None:
        """
        Add a message to history.
        
        Args:
            message: Message dict with 'content', 'role', 'timestamp'
            is_important: Whether to mark as important
        """
        message_id = len(self.history)
        message['id'] = message_id
        message['timestamp'] = message.get('timestamp', datetime.now().isoformat())
        
        self.history.append(message)
        
        if is_important:
            self.mark_important(message_id)
    
    def mark_important(self, message_id: int) -> None:
        """Mark a message as important (kept in context)."""
        if 0 <= message_id < len(self.history):
            self.important_messages.add(message_id)
    
    def generate_summary(self, start_id: int, end_id: int) -> str:
        """Generate a summary for a range of messages."""
        messages = self.history[start_id:end_id+1]
        
        key_points = []
        decisions = []
        action_items = []
        
        for msg in messages:
            content = msg.get('content', '').lower()
            
            # Look for decisions
            if any(kw in content for kw in ['决定', '决定了', '同意', '好的，', '行，', '决定', 'decided', 'agreed']):
                decisions.append(msg.get('content', '')[:100])
            
            # Look for action items
            if any(kw in content for kw in ['帮我', '我需要', '要做', 'todo', '任务', 'need to', 'should']):
                action_items.append(msg.get('content', '')[:100])
            
            # Extract significant content
            if len(msg.get('content', '')) > 50:
                snippet = msg.get('content', '')[:80]
                if snippet not in key_points:
                    key_points.append(snippet)
        
        # Build summary
        summary_parts = []
        summary_parts.append(f"## Summary of messages {start_id}-{end_id}")
        
        if decisions:
            summary_parts.append("### Key Decisions:")
            for d in decisions[-3:]:  # Last 3 decisions
                summary_parts.append(f"- {d}")
        
        if action_items:
            summary_parts.append("### Action Items:")
            for a in action_items[-3:]:  # Last 3 action items
                summary_parts.append(f"- {a}")
        
        if key_points:
            summary_parts.append("### Key Points:")
            for k in key_points[-5:]:  # Last 5 key points
                summary_parts.append(f"- {k}...")
        
        summary = "\n".join(summary_parts)
        
        # Cache the summary
        cache_key = f"{start_id}_{end_id}"
        self.summaries[cache_key] = summary
        
        return summary
    
    def get_context(self) -> Tuple[List[Dict], str]:
        """
        Get optimized context for current conversation.
        
        Returns:
            Tuple of (active_messages, summary_text)
        """
        if len(self.history) <= self.window_size:
            # No need for window management yet
            return self.history, ""
        
        # Determine which messages to keep
        # Always keep important messages
        important_in_window = []
        for msg_id in self.important_messages:
            if msg_id >= len(self.history) - self.summary_threshold:
                important_in_window.append(msg_id)
        
        # Calculate split point
        split_point = max(0, len(self.history) - self.window_size)
        
        # Generate summary for older messages if needed
        summary_text = ""
        if len(self.history) > self.summary_threshold:
            summary_end = split_point - 1
            if summary_end > 0:
                cache_key = f"0_{summary_end}"
                if cache_key in self.summaries:
                    summary_text = self.summaries[cache_key]
                else:
                    summary_text = self.generate_summary(0, summary_end)
        
        # Collect active messages
        active_messages = []
        
        # Add summary as a system message if we have one
        if summary_text:
            active_messages.append({
                'id': -1,
                'role': 'system',
                'content': summary_text,
                'timestamp': datetime.now().isoformat()
            })
        
        # Add important messages that are outside the window
        for msg_id in sorted(important_in_window):
            if msg_id < split_point:
                active_messages.append(self.history[msg_id])
        
        # Add the main window of recent messages
        for i in range(split_point, len(self.history)):
            active_messages.append(self.history[i])
        
        return active_messages, summary_text
    
    def get_stats(self) -> Dict:
        """Get statistics about current context."""
        active, summary = self.get_context()
        
        original_tokens = sum(len(msg.get('content', '')) / 2.7 for msg in self.history)
        active_tokens = sum(len(msg.get('content', '')) / 2.7 for msg in active)
        
        savings = ((original_tokens - active_tokens) / original_tokens * 100) if original_tokens > 0 else 0
        
        return {
            'total_messages': len(self.history),
            'active_messages': len(active),
            'important_messages': len(self.important_messages),
            'has_summary': bool(summary),
            'original_tokens_est': int(original_tokens),
            'active_tokens_est': int(active_tokens),
            'savings_percent': round(savings, 1)
        }

def main():
    # Demo
    print("=== Context Window Manager Demo ===")
    print()
    
    wm = WindowManager(window_size=6, summary_threshold=10)
    
    # Add some demo messages
    demo_messages = [
        "你好，我想学习Python",
        "好的！Python是个很好的起点",
        "你能推荐一些资源吗？",
        "当然！Codecademy和Python官方文档都不错",
        "好的，谢谢！那如何安装呢？",
        "去python.org下载，记得勾选Add to PATH",
        "好的，我是Windows用户",
        "没问题，Windows安装很简单",
        "安装时要注意什么？",
        "记得勾选'Add Python to PATH'，这很重要",
        "好的，我记住了！",
        "安装完告诉我，我们写第一个程序",
        "好的，我现在就去安装！",
        "一会儿见！祝安装顺利！"
    ]
    
    for i, msg in enumerate(demo_messages):
        role = 'user' if i % 2 == 0 else 'assistant'
        wm.add_message({'content': msg, 'role': role})
    
    # Mark some as important
    wm.mark_important(3)  # Resource recommendation
    wm.mark_important(5)  # Installation instructions
    
    # Get and display context
    print(f"Total messages: {len(demo_messages)}")
    print()
    
    active, summary = wm.get_context()
    
    if summary:
        print("=== Summary of Early Messages ===")
        print(summary)
        print()
    
    print("=== Active Context Window ===")
    for msg in active:
        if msg.get('id') == -1:
            continue  # Skip summary message in this view
        print(f"[{msg.get('id')}] {msg.get('role')}: {msg.get('content', '')[:50]}...")
    
    print()
    stats = wm.get_stats()
    print("=== Statistics ===")
    print(f"Total messages: {stats['total_messages']}")
    print(f"Active messages: {stats['active_messages']}")
    print(f"Important messages: {stats['important_messages']}")
    print(f"Original tokens (est): {stats['original_tokens_est']}")
    print(f"Active tokens (est): {stats['active_tokens_est']}")
    print(f"Savings: {stats['savings_percent']}%")
    
    if stats['savings_percent'] >= 50:
        print("\n🎯 Excellent! 50%+ token savings achieved!")

if __name__ == "__main__":
    main()
