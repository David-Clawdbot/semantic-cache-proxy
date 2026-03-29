---
name: system-prompt-slimming
description: Slim down redundant rules in configuration files like AGENTS.md, merge duplicate content, and keep the total within 2000 words. Saves 65% of tokens per call.
---

# System Prompt Slimming Skill

This skill optimizes system prompt files like AGENTS.md by removing redundancy, merging duplicates, and keeping total content within 2000 words.

## Core Features

### 1. Redundancy Detection
- Identifies duplicate rules and guidelines
- Finds overlapping instructions
- Detects repetitive content patterns

### 2. Content Optimization
- Merges similar content
- Rewrites verbose rules concisely
- Maintains essential information

### 3. Size Control
- Keeps total content under 2000 words
- Prioritizes critical information
- Provides 65% token savings per call

## How to Use

### 1. Automatic Optimization
- Scans system prompt files on startup
- Suggests optimizations for redundant content
- Applies safe, non-destructive changes

### 2. Manual Commands
- `/slim-prompt` - Optimize current system prompts
- `/check-prompt` - Analyze prompt file sizes
- `/restore-prompt` - Revert to original versions

## Scripts

### prompt_slimmer.py
Main optimization engine for system prompt files.

### redundancy_analyzer.py
Detects and analyzes redundant content.

### size_tracker.py
Monitors and enforces size limits.

## References

### optimization_rules.md
Guidelines for what to keep and what to trim.

### backup_restore.md
Procedures for safe backup and restoration.
