import requests
import time
import sys
import json

BASE_URL = "http://127.0.0.1:8002/api/honeypot"
API_KEY = "secret-key-123"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def test_intelligence_extraction():
    log("Testing Intelligence Extraction...")
    headers = {"x-api-key": API_KEY}
    
    # Scenario: Scammer sends multiple pieces of intel
    scam_text = "Pay 5000 to upi: scammer@okicici or bank account 9876543210. Visit http://phishing.com/login"
    
    payload = {
        "sessionId": "test-intel-session-1",
        "message": {
            "sender": "scammer",
            "text": scam_text,
            "timestamp": "2026-01-21T10:18:30Z"
        },
        "conversationHistory": []
    }
    
    try:
        resp = requests.post(BASE_URL, json=payload, headers=headers)
        data = resp.json()
        
        if resp.status_code != 200:
            log(f"Failed: {resp.status_code}", "ERROR")
            return False
            
        intel = data["extractedIntelligence"]
        
        # Verify UPI
        if "scammer@okicici" not in intel["upiIds"]:
            log(f"Failed to extract UPI. Got: {intel['upiIds']}", "ERROR")
            return False
            
        # Verify Bank
        if "9876543210" not in intel["bankAccounts"]:
            log(f"Failed to extract Bank. Got: {intel['bankAccounts']}", "ERROR")
            return False
            
        # Verify URL
        found_url = False
        for link in intel["phishingLinks"]:
            if "phishing.com" in link:
                found_url = True
                break
        if not found_url:
             log(f"Failed to extract URL. Got: {intel['phishingLinks']}", "ERROR")
             return False

        log("Intelligence Extraction Passed", "SUCCESS")
        return True
        
    except Exception as e:
        log(f"Exception: {e}", "ERROR")
        return False

if __name__ == "__main__":
    if test_intelligence_extraction():
        sys.exit(0)
    else:
        sys.exit(1)
