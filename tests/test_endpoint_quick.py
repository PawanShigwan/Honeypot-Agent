import requests
import json
import time

url = "http://127.0.0.1:8000/api/honeypot"
headers = {
    "x-api-key": "secret-key-123",
    "Content-Type": "application/json"
}
payload = {
  "sessionId": "session-test-001",
  "message": {
    "sender": "scammer",
    "text": "Urgent: Your bank account is blocked. Click here http://scam-link.com to verify.",
    "timestamp": int(time.time() * 1000)
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}

print(f"Testing URL: {url}")
try:
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
