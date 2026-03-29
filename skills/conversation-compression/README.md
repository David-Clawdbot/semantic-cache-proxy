# 📝 conversation-compression

**Compress long chat history into key summaries using /compact command.**

---

## 🎯 Features

### Automatic Compression
- Activates when conversation exceeds 8 rounds
- Triggers on keywords: "save tokens", "shorten conversation"
- Provides `/compact` command for manual compression

### Smart Summarization
- Extracts key points and decisions
- Preserves important context
- Removes redundant chit-chat

### Compression Formats
- Bullet-point summaries
- Key decision logs
- Action item tracking

---

## 💡 How to Use

### Automatic Mode
- Skill activates automatically when conversation exceeds 8 rounds
- Provides compression suggestion

### Manual Mode
- `/compact` - Compress current conversation
- `/compact [n]` - Compress last n messages

---

## 📊 Savings

**70-90% savings on conversation history tokens!**

Especially effective for:
- Long conversations with lots of back-and-forth
- Chats with repetitive confirmations
- Extended problem-solving sessions

---

## 🔧 Scripts

- `compress_conversation.py` - Main compression engine
- `summary_templates.py` - Summary format templates

---

## 📚 References

- `compression_strategies.md` - Detailed compression strategies

---

*Part of the Tokens Optimization Skills Collection*
