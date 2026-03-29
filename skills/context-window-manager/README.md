# 🪟 context-window-manager

**Smart context window management with sliding windows and intelligent summarization.**

---

## 🎯 Features

### Sliding Window
- Default: Keep only last 6-8 messages
- Configurable window size
- Dramatically reduces history tokens

### Intelligent Summarization
- Earlier messages replaced with concise summaries
- Extracts key decisions and action items
- Maintains conversation continuity

### Importance Marking
- `/keep` command to mark important messages
- Important messages stay in context
- Auto-detects high-value content

### Manual Controls
- `/window [n]` - Set window size
- `/summary` - Force summary generation
- `/history` - Show full history
- `/clear` - Clear non-important history

---

## 💡 How to Use

### Automatic Mode
- Activates when conversation exceeds 8 rounds
- Applies sliding window automatically
- Generates summaries for older messages

### Manual Commands
- `/keep` - Keep current message in context
- `/window 10` - Set window to 10 messages
- `/compact` - Force context compaction
- `/status` - Show current context status

---

## 📊 Savings

**50-80% savings on conversation context!**

| Conversation Length | Savings |
|-------------------|---------|
| Short (<8 rounds) | 0% (no change) |
| Medium (8-20 rounds) | 50-60% |
| Long (>20 rounds) | 70-80% |

---

## 🔧 Scripts

- `window_manager.py` - Main context window management
- `summary_engine.py` - Intelligent summarization
- `importance_detector.py` - Importance detection and marking

---

## 📚 References

- `window_strategies.md` - Window management strategies
- `importance_rules.md` - Importance detection rules

---

*Part of the Tokens Optimization Skills Collection*
