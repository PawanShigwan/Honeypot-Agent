"""
Real-world scenario test - Simulates a complete scam conversation
"""
import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://127.0.0.1:8000/api/honeypot"
API_KEY = "secret-key-123"

def send_message(session_id, sender, text, history):
    """Send a message and return the response"""
    headers = {"x-api-key": API_KEY}
    
    payload = {
        "sessionId": session_id,
        "message": {
            "sender": sender,
            "text": text,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        },
        "conversationHistory": history
    }
    
    try:
        resp = requests.post(BASE_URL, json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"Error: {resp.status_code}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def print_conversation_turn(turn_num, sender, message, response):
    """Print a conversation turn nicely formatted"""
    print(f"\n{'='*70}")
    print(f"TURN {turn_num}")
    print(f"{'='*70}")
    print(f"[{sender.upper()}]: {message}")
    
    if response:
        print(f"\n[SYSTEM ANALYSIS]")
        print(f"  Scam Detected: {response.get('scamDetected')}")
        print(f"  Agent Notes: {response.get('agentNotes', 'N/A')}")
        
        intel = response.get('extractedIntelligence', {})
        has_intel = any([intel.get('bankAccounts'), intel.get('upiIds'), 
                        intel.get('phishingLinks'), intel.get('phoneNumbers')])
        
        if has_intel:
            print(f"\n[INTELLIGENCE EXTRACTED]")
            if intel.get('upiIds'):
                print(f"  🎯 UPI IDs: {', '.join(intel['upiIds'])}")
            if intel.get('phoneNumbers'):
                print(f"  📱 Phone Numbers: {', '.join(intel['phoneNumbers'])}")
            if intel.get('bankAccounts'):
                print(f"  🏦 Bank Accounts: {', '.join(intel['bankAccounts'])}")
            if intel.get('phishingLinks'):
                print(f"  🔗 Phishing Links: {', '.join(intel['phishingLinks'])}")
        
        if response.get('reply'):
            print(f"\n[HONEYPOT REPLY]")
            print(f"  {response['reply']}")
        
        metrics = response.get('engagementMetrics', {})
        print(f"\n[METRICS]")
        print(f"  Duration: {metrics.get('engagementDurationSeconds')}s")
        print(f"  Total Messages: {metrics.get('totalMessagesExchanged')}")

def run_realistic_scam_scenario():
    """Simulate a realistic bank scam conversation"""
    print("="*70)
    print("REALISTIC SCAM SCENARIO: Bank Account Verification Scam")
    print("="*70)
    print("\nThis simulates a common Indian scam where fraudsters pretend to be")
    print("from a bank and try to extract payment via UPI.\n")
    
    session_id = "realistic-scam-2026-01-26"
    history = []
    
    # Turn 1: Initial contact
    scammer_msg_1 = "Hello sir, this is Rajesh from State Bank of India customer care. Your account has been temporarily blocked due to suspicious activity."
    response_1 = send_message(session_id, "scammer", scammer_msg_1, history)
    print_conversation_turn(1, "scammer", scammer_msg_1, response_1)
    
    if response_1 and response_1.get('reply'):
        history.append({
            "sender": "scammer",
            "text": scammer_msg_1,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        })
        history.append({
            "sender": "victim",
            "text": response_1['reply'],
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        })
    
    time.sleep(2)
    
    # Turn 2: Creating urgency
    scammer_msg_2 = "Sir, you need to verify your account immediately or it will be permanently blocked within 24 hours. This is very urgent matter."
    response_2 = send_message(session_id, "scammer", scammer_msg_2, history)
    print_conversation_turn(2, "scammer", scammer_msg_2, response_2)
    
    if response_2 and response_2.get('reply'):
        history.append({
            "sender": "scammer",
            "text": scammer_msg_2,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        })
        history.append({
            "sender": "victim",
            "text": response_2['reply'],
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        })
    
    time.sleep(2)
    
    # Turn 3: The actual scam - requesting payment
    scammer_msg_3 = "To verify and unblock your account, you need to pay verification fee of Rs.500. Please send to our official UPI ID: sbiverify@paytm immediately."
    response_3 = send_message(session_id, "scammer", scammer_msg_3, history)
    print_conversation_turn(3, "scammer", scammer_msg_3, response_3)
    
    if response_3 and response_3.get('reply'):
        history.append({
            "sender": "scammer",
            "text": scammer_msg_3,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        })
        history.append({
            "sender": "victim",
            "text": response_3['reply'],
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        })
    
    time.sleep(2)
    
    # Turn 4: Providing fake link
    scammer_msg_4 = "Also visit our verification portal at http://sbi-verify-account.com to complete the process. Hurry sir!"
    response_4 = send_message(session_id, "scammer", scammer_msg_4, history)
    print_conversation_turn(4, "scammer", scammer_msg_4, response_4)
    
    # Final summary
    print(f"\n{'='*70}")
    print("SCENARIO COMPLETE - SUMMARY")
    print(f"{'='*70}")
    
    if response_4:
        print(f"\n✅ Scam Successfully Detected: {response_4.get('scamDetected')}")
        print(f"📊 Total Conversation Turns: 4")
        print(f"⏱️  Total Duration: {response_4.get('engagementMetrics', {}).get('engagementDurationSeconds')}s")
        
        intel = response_4.get('extractedIntelligence', {})
        print(f"\n🎯 Intelligence Gathered:")
        print(f"   - UPI IDs: {len(intel.get('upiIds', []))} found")
        print(f"   - Phishing Links: {len(intel.get('phishingLinks', []))} found")
        print(f"   - Phone Numbers: {len(intel.get('phoneNumbers', []))} found")
        print(f"   - Bank Accounts: {len(intel.get('bankAccounts', []))} found")
        
        print(f"\n💡 Honeypot Performance:")
        print(f"   - Successfully engaged scammer for {response_4.get('engagementMetrics', {}).get('totalMessagesExchanged')} messages")
        print(f"   - AI-generated replies kept conversation realistic")
        print(f"   - Callback likely triggered (check server logs)")
    
    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    run_realistic_scam_scenario()
