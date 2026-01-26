# Agentic Honeypot API

This is a production-ready Honeypot API designed for the GUVI hackathon. It uses FastAPI for high performance and Gemini AI for intelligent scam detection and interaction.

## 🚀 Features
- **Fast Responses**: Optimized with background tasks to ensure <2s response time.
- **AI-Powered**: Uses Gemini to detect scams and generate natural persona-based replies.
- **Rule-Based Hybrid**: Immediate detection for known scam patterns.
- **Intelligence Extraction**: Automatically extracts UPI IDs, bank accounts, and phishing links.
- **GUVI Automated Callback**: Sends results to the GUVI evaluation platform automatically.

## 🛠️ Setup & Deployment

### 1. Local Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example`.
4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### 2. Deploy to Render
1. Push your code to a GitHub repository.
2. Go to [Render](https://render.com) and create a **New Web Service**.
3. Connect your repository.
4. Render will automatically detect the `render.yaml` or you can manually set:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set Environment Variables in the Render dashboard:
   - `HONEYPOT_API_KEY`: Your secret key for `x-api-key` header.
   - `GEMINI_API_KEY`: Your Google Gemini API key.
   - `GUVI_CALLBACK_URL`: Target URL for automated results.

## 🧪 API Documentation

### POST `/api/honeypot`
**Headers:**
- `x-api-key`: your-secret-key

**Request Body:**
```json
{
  "sessionId": "unique-session-id",
  "message": {
    "sender": "scammer",
    "text": "Hello, your account is blocked. Please verify at https://bit.ly/fake-link",
    "timestamp": "2024-03-20T10:00:00Z"
  },
  "conversationHistory": []
}
```

**Response:**
```json
{
  "scamDetected": true,
  "engagementMetrics": {
    "engagementDurationSeconds": 0,
    "totalMessagesExchanged": 1
  },
  "extractedIntelligence": {
    "bankAccounts": [],
    "upiIds": [],
    "phishingLinks": ["https://bit.ly/fake-link"],
    "phoneNumbers": [],
    "suspiciousKeywords": ["blocked", "verify"]
  },
  "agentNotes": "Confirmed by High-Confidence Rules | Links: 1 found",
  "reply": "Wait, why is my account blocked? I need it for my bills!"
}
```
