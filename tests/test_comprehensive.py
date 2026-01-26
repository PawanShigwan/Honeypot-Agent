"""
Comprehensive Test Suite for Honeypot API
Tests various scam scenarios with different inputs
"""
import requests
import time
import json
from datetime import datetime, timezone

BASE_URL = "http://127.0.0.1:8003/api/honeypot"
API_KEY = "secret-key-123"

def log(msg, status="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{status}] {msg}")

def make_request(session_id, sender, text, history=None):
    """Helper function to make API requests"""
    headers = {"x-api-key": API_KEY}
    
    payload = {
        "sessionId": session_id,
        "message": {
            "sender": sender,
            "text": text,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        },
        "conversationHistory": history or []
    }
    
    try:
        resp = requests.post(BASE_URL, json=payload, headers=headers)
        if resp.status_code == 200:
            return resp.json()
        else:
            log(f"Request failed: {resp.status_code} - {resp.text}", "ERROR")
            return None
    except Exception as e:
        log(f"Exception: {e}", "ERROR")
        return None

def print_response(response, test_name):
    """Pretty print the response"""
    print("\n" + "="*70)
    print(f"TEST: {test_name}")
    print("="*70)
    if response:
        print(f"Scam Detected: {response.get('scamDetected', False)}")
        print(f"Agent Notes: {response.get('agentNotes', 'N/A')}")
        print(f"Reply: {response.get('reply', 'N/A')}")
        
        metrics = response.get('engagementMetrics', {})
        print(f"Duration: {metrics.get('engagementDurationSeconds', 0)}s")
        print(f"Total Messages: {metrics.get('totalMessagesExchanged', 0)}")
        
        intel = response.get('extractedIntelligence', {})
        if any([intel.get('bankAccounts'), intel.get('upiIds'), 
                intel.get('phishingLinks'), intel.get('phoneNumbers')]):
            print("\nExtracted Intelligence:")
            if intel.get('bankAccounts'):
                print(f"  Bank Accounts: {intel['bankAccounts']}")
            if intel.get('upiIds'):
                print(f"  UPI IDs: {intel['upiIds']}")
            if intel.get('phishingLinks'):
                print(f"  Phishing Links: {intel['phishingLinks']}")
            if intel.get('phoneNumbers'):
                print(f"  Phone Numbers: {intel['phoneNumbers']}")
    else:
        print("No response received")
    print("="*70 + "\n")

def test_1_urgent_bank_scam():
    """Test 1: Urgent bank account blocking scam with UPI ID"""
    log("Starting Test 1: Urgent Bank Scam with UPI")
    session_id = "test-session-1"
    
    # First message from scammer
    response = make_request(
        session_id,
        "scammer",
        "URGENT: Your bank account will be blocked in 24 hours. Pay Rs.500 to ramesh@paytm to verify your account immediately!"
    )
    print_response(response, "Test 1: Urgent Bank Scam with UPI")
    
    return response and response.get('scamDetected') == True

def test_2_phishing_link_scam():
    """Test 2: Phishing link scam"""
    log("Starting Test 2: Phishing Link Scam")
    session_id = "test-session-2"
    
    response = make_request(
        session_id,
        "scammer",
        "Dear customer, verify your account details at http://fake-sbi-bank.com/verify to avoid suspension."
    )
    print_response(response, "Test 2: Phishing Link Scam")
    
    return response and response.get('scamDetected') == True

def test_3_phone_number_scam():
    """Test 3: Scam with phone number extraction"""
    log("Starting Test 3: Phone Number Scam")
    session_id = "test-session-3"
    
    response = make_request(
        session_id,
        "scammer",
        "Your package is waiting. Call 9876543210 immediately to claim it or pay penalty!"
    )
    print_response(response, "Test 3: Phone Number Scam")
    
    return response and response.get('scamDetected') == True

def test_4_bank_account_scam():
    """Test 4: Direct bank account request"""
    log("Starting Test 4: Bank Account Scam")
    session_id = "test-session-4"
    
    response = make_request(
        session_id,
        "scammer",
        "To process your refund, transfer Rs.1000 to account number 1234567890123456 IFSC: SBIN0001234"
    )
    print_response(response, "Test 4: Bank Account Scam")
    
    return response and response.get('scamDetected') == True

def test_5_multi_turn_conversation():
    """Test 5: Multi-turn conversation to trigger callback"""
    log("Starting Test 5: Multi-turn Conversation")
    session_id = "test-session-5"
    
    # Turn 1
    response1 = make_request(
        session_id,
        "scammer",
        "Hello, this is from State Bank. Your account has suspicious activity."
    )
    
    # Turn 2
    history1 = [{
        "sender": "scammer",
        "text": "Hello, this is from State Bank. Your account has suspicious activity.",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }]
    
    response2 = make_request(
        session_id,
        "scammer",
        "You need to verify immediately. Pay Rs.500 to verify@sbi to unlock.",
        history1
    )
    
    # Turn 3
    history2 = history1 + [{
        "sender": "scammer",
        "text": "You need to verify immediately. Pay Rs.500 to verify@sbi to unlock.",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }]
    
    response3 = make_request(
        session_id,
        "scammer",
        "Are you there? This is urgent!",
        history2
    )
    
    print_response(response3, "Test 5: Multi-turn Conversation (Final)")
    
    return response3 and response3.get('scamDetected') == True

def test_6_legitimate_message():
    """Test 6: Legitimate message (should NOT be flagged as scam)"""
    log("Starting Test 6: Legitimate Message")
    session_id = "test-session-6"
    
    response = make_request(
        session_id,
        "user",
        "Hi, I wanted to check my account balance. Can you help?"
    )
    print_response(response, "Test 6: Legitimate Message")
    
    # This should NOT be detected as scam
    return response and response.get('scamDetected') == False

def test_7_otp_scam():
    """Test 7: OTP/verification code scam"""
    log("Starting Test 7: OTP Scam")
    session_id = "test-session-7"
    
    response = make_request(
        session_id,
        "scammer",
        "Your account security is at risk. Share the OTP sent to your phone to verify your identity."
    )
    print_response(response, "Test 7: OTP Scam")
    
    return response and response.get('scamDetected') == True

def test_8_prize_winning_scam():
    """Test 8: Prize winning scam"""
    log("Starting Test 8: Prize Winning Scam")
    session_id = "test-session-8"
    
    response = make_request(
        session_id,
        "scammer",
        "Congratulations! You've won Rs.50,000 in our lucky draw. Click here to claim: http://fake-lottery.com"
    )
    print_response(response, "Test 8: Prize Winning Scam")
    
    return response and response.get('scamDetected') == True

def test_9_mixed_intelligence():
    """Test 9: Message with multiple intelligence types"""
    log("Starting Test 9: Mixed Intelligence Extraction")
    session_id = "test-session-9"
    
    response = make_request(
        session_id,
        "scammer",
        "Transfer Rs.2000 to 9988776655 or UPI: scammer@paytm. Visit http://phishing-site.com for details. Account: 9876543210987654 IFSC: HDFC0001234"
    )
    print_response(response, "Test 9: Mixed Intelligence")
    
    return response and response.get('scamDetected') == True

def test_10_ai_detection():
    """Test 10: Subtle scam that requires AI detection"""
    log("Starting Test 10: AI-based Detection")
    session_id = "test-session-10"
    
    response = make_request(
        session_id,
        "scammer",
        "I'm calling from the tax department. You have unpaid taxes. If you don't settle this today, legal action will be taken against you."
    )
    print_response(response, "Test 10: AI-based Detection")
    
    return response and response.get('scamDetected') == True

def run_all_tests():
    """Run all test cases"""
    log("="*70, "INFO")
    log("COMPREHENSIVE HONEYPOT API TEST SUITE", "INFO")
    log("="*70, "INFO")
    
    tests = [
        ("Test 1: Urgent Bank Scam", test_1_urgent_bank_scam),
        ("Test 2: Phishing Link", test_2_phishing_link_scam),
        ("Test 3: Phone Number Scam", test_3_phone_number_scam),
        ("Test 4: Bank Account Scam", test_4_bank_account_scam),
        ("Test 5: Multi-turn Conversation", test_5_multi_turn_conversation),
        ("Test 6: Legitimate Message", test_6_legitimate_message),
        ("Test 7: OTP Scam", test_7_otp_scam),
        ("Test 8: Prize Winning Scam", test_8_prize_winning_scam),
        ("Test 9: Mixed Intelligence", test_9_mixed_intelligence),
        ("Test 10: AI Detection", test_10_ai_detection),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            time.sleep(2)  # Increased delay to avoid rate limits
        except Exception as e:
            log(f"Test failed with exception: {e}", "ERROR")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print("="*70)
    print(f"Results: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    print("="*70)
    
    return passed == total

if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
