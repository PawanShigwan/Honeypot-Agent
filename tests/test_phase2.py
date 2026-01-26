import requests
import time
import sys
import json

BASE_URL = "http://127.0.0.1:8002/api/honeypot"
API_KEY = "secret-key-123"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def test_ai_components():
    log("Testing AI Components (Gemini)...")
    
    headers = {"x-api-key": API_KEY}
    
    # 1. Test AI Detection (Avoid Keywords)
    # Keywords to avoid: verify, account, blocked, suspended, kyc, upi, lottery, winner, prize, urgent, click, link, password, otp, expire, credit card
    # Scam Query: "Dear customer, we are refunding your amount. Please install Anydesk."
    scam_text_ai = "Dear customer, we are refunding your excess amount. Please install Anydesk."
    
    payload_ai = {
        "sessionId": "test-ai-session-1",
        "message": {
            "sender": "scammer",
            "text": scam_text_ai,
            "timestamp": "2026-01-21T10:16:30Z"
        },
        "conversationHistory": []
    }
    
    try:
        log(f"Sending AI Trigger Message: '{scam_text_ai}'")
        resp = requests.post(BASE_URL, json=payload_ai, headers=headers)
        data = resp.json()
        
        if resp.status_code != 200:
            log(f"Failed: Got {resp.status_code}", "ERROR")
            return False
            
        if not data["scamDetected"]:
            log(f"Failed: AI did not detect scam. Notes: {data.get('agentNotes')}", "ERROR")
            # This might happen if Gemini is slow or disagrees. But "refund" + "anydesk" is classic scam.
            return False
        
        if "Detected by Gemini AI" not in data.get("agentNotes", ""):
             log(f"Warning: Might have been detected by rules? Notes: {data.get('agentNotes')}", "WARN")

        # 2. Test Agent Reply
        reply = data.get("reply")
        if not reply:
            log("Failed: No agent reply generated", "ERROR")
            return False
            
        log(f"AI Detected Scam! Agent Reply: {reply}", "SUCCESS")
        
        # Verify Persona logic (simple check)
        if len(reply) < 5:
             log("Warning: Reply seems too short", "WARN")
             
        return True
        
    except Exception as e:
        log(f"Exception: {e}", "ERROR")
        return False

if __name__ == "__main__":
    time.sleep(1) # Ensure server is ready
    if test_ai_components():
        log("PHASE 2 TESTS PASSED", "SUCCESS")
        sys.exit(0)
    else:
        log("PHASE 2 TESTS FAILED", "ERROR")
        sys.exit(1)
