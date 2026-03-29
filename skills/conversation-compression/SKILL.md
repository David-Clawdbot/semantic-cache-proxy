---
name: conversation-compression
description: Compress long chat history into key summaries using /compact command. Activate when对话超过8轮 or user mentions "save tokens" or "shorten conversation".
---

# Conversation Compression Skill

This skill compresses long chat histories into concise key summaries to save tokens.

## Core Features

### 1. Automatic Compression
- Activates when conversation exceeds 8 rounds
- Triggers on keywords: "save tokens", "shorten conversation"
- Provides `/compact` command for manual compression

### 2. Smart Summarization
- Extracts key points and decisions
- Preserves important context
- Removes redundant chit-chat

### 3. Compression Formats
- Bullet-point summaries
- Key decision logs
- Action item tracking

## How to Use

### 1. Automatic Mode
- Skill activates automatically when conversation exceeds 8 rounds
- Provides compression suggestion

### 2. Manual Mode
- Use `/compact` command to compress current conversation
- Use `/compact [n]` to compress last n messages

## Scripts

### compress_conversation.py
Main compression script that analyzes and summarizes conversations.

### summary_templates.py
Templates for different compression formats.

## References

### compression_strategies.md
Detailed strategies for effective conversation compression.
