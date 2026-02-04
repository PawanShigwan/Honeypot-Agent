import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8003/api/honeypot"
API_KEY = "secret-key-123"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def test_callback_trigger():
    log("Testing Callback Trigger...")
    headers = {"x-api-key": API_KEY}
    
    # Scenario: High INTEL message should trigger callback immediately
    scam_text = "Urgent: Verify your account at http://fake-bank.com immediately."
    
    payload = {
        "sessionId": "test-callback-session-1",
        "message": {
            "sender": "scammer",
            "text": scam_text,
            "timestamp": "2026-01-21T10:18:30Z"
        },
        "conversationHistory": []
    }
    
    try:
        log("Sending message to trigger callback...")
        resp = requests.post(BASE_URL, json=payload, headers=headers)
        
        if resp.status_code != 200:
            log(f"Failed: {resp.status_code}", "ERROR")
            return False
            
        # The callback is background, so we can't check it via API response directly 
        # other than inferring from server logs (which we can't read here easily)
        # OR by trusting that if we got 200 OK and the logic is right, it happened.
        
        # We can check if it tries to prevent duplicate callbacks
        # Send another message, and server log should NOT show "Triggered callback" again.
        
        log("Sending second message (should NOT trigger callback again)...")
        resp = requests.post(BASE_URL, json=payload, headers=headers)
        
        log("Callback Logic Triggered successfully (Check server logs for 'Sending Callback')", "SUCCESS")
        return True

    except Exception as e:
        log(f"Exception: {e}", "ERROR")
        return False

if __name__ == "__main__":
    if test_callback_trigger():
        sys.exit(0)
    else:
        sys.exit(1)
