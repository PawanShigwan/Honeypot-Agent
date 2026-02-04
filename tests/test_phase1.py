import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8002/api/honeypot"
API_KEY = "secret-key-123"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def test_auth():
    log("Testing Auth...")
    # No Key
    resp = requests.post(BASE_URL, json={})
    if resp.status_code != 401:
        log(f"Failed: Expected 401 for missing key, got {resp.status_code}", "ERROR")
        return False
    
    # Wrong Key
    resp = requests.post(BASE_URL, json={}, headers={"x-api-key": "wrong"})
    if resp.status_code != 401:
        log(f"Failed: Expected 401 for wrong key, got {resp.status_code}", "ERROR")
        return False
        
    log("Auth Test Passed", "SUCCESS")
    return True

def test_flow():
    log("Testing Basic Flow & Scam Detection...")
    
    headers = {"x-api-key": API_KEY}
    
    # Non-Scam Message
    payload_clean = {
        "sessionId": "test-session-1",
        "message": {
            "sender": "user",
            "text": "Hello, how are you?",
            "timestamp": "2026-01-21T10:15:30Z"
        },
        "conversationHistory": []
    }
    
    try:
        resp = requests.post(BASE_URL, json=payload_clean, headers=headers)
        data = resp.json()
        
        if resp.status_code != 200:
            log(f"Failed: Clean Request got {resp.status_code} {resp.text}", "ERROR")
            return False
            
        if data["scamDetected"] is True:
            log(f"Failed: False positive on 'Hello, how are you?'", "ERROR")
            return False
            
        log("Clean Message Test Passed", "SUCCESS")
        
        # Scam Message
        payload_scam = {
            "sessionId": "test-session-1",
            "message": {
                "sender": "scammer",
                "text": "Your account is blocked. Verify immediately.",
                "timestamp": "2026-01-21T10:16:30Z"
            },
            "conversationHistory": [payload_clean["message"]]
        }
        
        resp = requests.post(BASE_URL, json=payload_scam, headers=headers)
        data = resp.json()
        
        if not data["scamDetected"]:
            log("Failed: Did not detect scam message", "ERROR")
            return False
            
        if data["engagementMetrics"]["totalMessagesExchanged"] != 2:
            log(f"Failed: Incorrect message count. Expected 2, got {data['engagementMetrics']['totalMessagesExchanged']}", "ERROR")
            return False

        log("Scam Message Test Passed", "SUCCESS")
        return True
        
    except Exception as e:
        log(f"Exception during test: {e}", "ERROR")
        return False

if __name__ == "__main__":
    # Wait for server to start
    log("Waiting for server...")
    time.sleep(3)
    
    if test_auth() and test_flow():
        log("ALL PHASE 1 TESTS PASSED", "SUCCESS")
        sys.exit(0)
    else:
        log("TESTS FAILED", "ERROR")
        sys.exit(1)
