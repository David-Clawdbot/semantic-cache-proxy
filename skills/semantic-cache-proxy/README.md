# 🧠 semantic-cache-proxy

**Semantic caching for repeated queries - similar questions return cached results.**

---

## 🎯 Features

### Semantic Similarity Matching
- Uses Sentence-BERT for vector embeddings
- ≥0.85 similarity threshold for cache hits
- Understands semantic meaning, not just exact matches

### Redis Storage
- Fast in-memory caching
- 24-hour automatic expiration
- Manual cache clearing available

### Manual Toggle
- Enable/disable caching on demand
- Cache status monitoring
- Hit/miss statistics

---

## 💡 How to Use

### Automatic Activation
- Automatically caches responses
- Checks for similar queries before sending to model
- Returns cached results for high-similarity matches

### Manual Controls
- View cache statistics
- Clear specific cache entries
- Enable/disable caching temporarily

---

## 📊 Savings

**Up to 80% savings on repeated or similar queries!**

Perfect for:
- FAQ-style conversations
- Common setup questions
- Documentation lookups
- Repeated troubleshooting

---

## 🔧 Configuration

```json
{
  "similarity_threshold": 0.85,
  "cache_ttl_hours": 24,
  "redis_url": "redis://localhost:6379"
}
```

---

## 📚 Dependencies

- sentence-transformers (for embeddings)
- redis (for caching)
- scikit-learn (for similarity calculation)

---

*Part of the Tokens Optimization Skills Collection*
