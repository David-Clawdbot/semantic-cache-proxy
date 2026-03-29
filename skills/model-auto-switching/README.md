# 🔄 model-auto-switching

**Automatically switch to low-cost models for simple tasks, high-cost for complex ones.**

---

## 🎯 Features

### Intelligent Task Analysis
- Analyzes task complexity automatically
- Classifies tasks as simple, medium, or complex
- Determines appropriate model for each task

### Cost Optimization
- Uses low-cost models for simple tasks
- Switches to high-cost models for complex tasks
- Estimated 30% cost reduction overall

### Model Configuration
- Supports multiple model providers
- Customizable model mapping
- Fallback mechanisms

---

## 💡 How to Use

### Automatic Mode
- Skill analyzes each task automatically
- Selects optimal model without user intervention
- Provides cost savings estimates

### Manual Override
- `/model [model-name]` - Manual model selection
- `/cost-estimate` - Cost prediction for current task

---

## 📊 Savings

**~30% overall cost savings!**

Breakdown by task type:
- Simple tasks: 75% savings (glm-4.6v-FlashX)
- Medium tasks: 50% savings (balanced models)
- Complex tasks: 0% savings (but quality preserved)

---

## 🔧 Scripts

- `model_selector.py` - Main model selection logic
- `task_analyzer.py` - Task complexity analysis
- `cost_calculator.py` - Cost estimation and tracking

---

## 📚 References

- `model_mapping.md` - Model-to-task configuration
- `cost_analysis.md` - Detailed cost analysis

---

*Part of the Tokens Optimization Skills Collection*
