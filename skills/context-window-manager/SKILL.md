---
name: context-window-manager
description: Smart context window management that saves 50-80% of history tokens using sliding windows, intelligent summarization, and importance marking. Activates automatically for long conversations.
---

# Context Window Manager Skill

This skill manages conversation context windows to dramatically reduce token usage while preserving important information.

## Core Features

### 1. Sliding Window
- Default: Keep only last 6-8 messages
- Configurable window size
- Dramatically reduces history tokens

### 2. Intelligent Summarization
- Earlier messages replaced with concise summaries
- Extracts key decisions and action items
- Maintains conversation continuity

### 3. Importance Marking
- `/keep` command to mark important messages
- Important messages stay in context
- Auto-detects high-value content

### 4. Manual Controls
- `/window [n]` - Set window size
- `/summary` - Force summary generation
- `/history` - Show full history
- `/clear` - Clear non-important history

## How to Use

### Automatic Mode
- Activates when conversation exceeds 8 rounds
- Applies sliding window automatically
- Generates summaries for older messages

### Manual Commands
- `/keep` - Keep current message in context
- `/window 10` - Set window to 10 messages
- `/compact` - Force context compaction
- `/status` - Show current context status

## Token Savings
- **Short conversations (<8 rounds)**: 0% (no change)
- **Medium conversations (8-20 rounds)**: 50-60% savings
- **Long conversations (>20 rounds)**: 70-80% savings

## Scripts

### window_manager.py
Main context window management logic.

### summary_engine.py
Intelligent conversation summarization.

### importance_detector.py
Detects and marks important messages.

## References

### window_strategies.md
Different window management strategies and tradeoffs.

### importance_rules.md
Rules for auto-detecting important messages.
