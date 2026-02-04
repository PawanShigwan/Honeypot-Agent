"""
Quick validation test to check specific scenarios
"""
import requests
from datetime import datetime, timezone

BASE_URL = "http://127.0.0.1:8000/api/honeypot"
API_KEY = "secret-key-123"

def test_scenario(name, session_id, sender, text):
    """Test a single scenario and print results"""
    headers = {"x-api-key": API_KEY}
    
    payload = {
        "sessionId": session_id,
        "message": {
            "sender": sender,
            "text": text,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        },
        "conversationHistory": []
    }
    
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"{'='*70}")
    print(f"Input: {text}")
    print(f"Sender: {sender}")
    
    try:
        resp = requests.post(BASE_URL, json=payload, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"\n✓ Status: {resp.status_code} OK")
            print(f"Scam Detected: {data.get('scamDetected')}")
            print(f"Agent Notes: {data.get('agentNotes')}")
            print(f"Reply: {data.get('reply')}")
            
            intel = data.get('extractedIntelligence', {})
            if any([intel.get('bankAccounts'), intel.get('upiIds'), 
                    intel.get('phishingLinks'), intel.get('phoneNumbers')]):
                print("\nIntelligence Extracted:")
                for key, value in intel.items():
                    if value:
                        print(f"  {key}: {value}")
            
            metrics = data.get('engagementMetrics', {})
            print(f"\nMetrics:")
            print(f"  Duration: {metrics.get('engagementDurationSeconds')}s")
            print(f"  Messages: {metrics.get('totalMessagesExchanged')}")
            
            return True
        else:
            print(f"\n✗ Failed: {resp.status_code}")
            print(f"Response: {resp.text}")
            return False
            
    except Exception as e:
        print(f"\n✗ Exception: {e}")
        return False

if __name__ == "__main__":
    print("="*70)
    print("QUICK VALIDATION TEST - Different Input Scenarios")
    print("="*70)
    
    # Test 1: UPI scam
    test_scenario(
        "UPI Payment Scam",
        "quick-test-1",
        "scammer",
        "URGENT! Pay Rs.500 to verify@paytm to unlock your account now!"
    )
    
    # Test 2: Phishing link
    test_scenario(
        "Phishing Link",
        "quick-test-2",
        "scammer",
        "Click here to verify: http://fake-bank.com/verify"
    )
    
    # Test 3: Phone number scam
    test_scenario(
        "Phone Number Scam",
        "quick-test-3",
        "scammer",
        "Call 9876543210 immediately to avoid account suspension!"
    )
    
    # Test 4: Bank account
    test_scenario(
        "Bank Account Scam",
        "quick-test-4",
        "scammer",
        "Transfer to account 1234567890123456 IFSC SBIN0001234"
    )
    
    # Test 5: Legitimate message (should NOT be scam)
    test_scenario(
        "Legitimate Message",
        "quick-test-5",
        "user",
        "Hello, I need help with my account balance inquiry."
    )
    
    # Test 6: AI detection - subtle scam
    test_scenario(
        "Subtle Tax Scam (AI Detection)",
        "quick-test-6",
        "scammer",
        "This is the tax department. You have unpaid taxes. Legal action will be taken if you don't pay today."
    )
    
    # Test 7: Prize scam
    test_scenario(
        "Prize Winning Scam",
        "quick-test-7",
        "scammer",
        "Congratulations! You won Rs.1 lakh. Click http://lottery-fake.com to claim."
    )
    
    # Test 8: OTP scam
    test_scenario(
        "OTP Verification Scam",
        "quick-test-8",
        "scammer",
        "Your account is locked. Share the OTP we sent to verify your identity."
    )
    
    print(f"\n{'='*70}")
    print("All tests completed!")
    print(f"{'='*70}\n")
