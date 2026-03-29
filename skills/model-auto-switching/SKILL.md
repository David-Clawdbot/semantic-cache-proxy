---
name: model-auto-switching
description: Automatically switch to low-cost models for simple tasks and high-cost models for complex tasks. Reduces token costs by approximately 30%.
---

# Model Auto-Switching Skill

This skill automatically switches between different models based on task complexity to optimize token costs.

## Core Features

### 1. Intelligent Task Analysis
- Analyzes task complexity automatically
- Classifies tasks as simple, medium, or complex
- Determines appropriate model for each task

### 2. Cost Optimization
- Uses low-cost models for simple tasks
- Switches to high-cost models for complex tasks
- Estimated 30% cost reduction

### 3. Model Configuration
- Supports multiple model providers
- Customizable model mapping
- Fallback mechanisms

## How to Use

### 1. Automatic Mode
- Skill analyzes each task automatically
- Selects optimal model without user intervention
- Provides cost savings estimates

### 2. Manual Override
- Users can specify preferred model
- `/model [model-name]` command for manual selection
- `/cost-estimate` for cost predictions

## Scripts

### model_selector.py
Main model selection and switching logic.

### task_analyzer.py
Task complexity analysis engine.

### cost_calculator.py
Cost estimation and savings tracking.

## References

### model_mapping.md
Configuration for model-to-task mapping.

### cost_analysis.md
Detailed cost analysis and optimization strategies.
