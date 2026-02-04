import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/honeypot"
HEADERS = {
    "x-api-key": "secret-key-123",
    "Content-Type": "application/json"
}
SESSION_ID = f"eval-flow-{int(time.time())}"

def print_step(step, msg):
    print(f"\n{'='*50}\nSTEP {step}: {msg}\n{'='*50}")

def send_message(text, sender="scammer", history=[]):
    payload = {
        "sessionId": SESSION_ID,
        "message": {
            "sender": sender,
            "text": text,
            "timestamp": int(time.time() * 1000)
        },
        "conversationHistory": history,
        "metadata": {
            "channel": "WhatsApp",
            "language": "English",
            "locale": "IN"
        }
    }
    
    try:
        response = requests.post(BASE_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

# DATA
history = []

# STEP 1: Platform sends a suspected scam message
print_step(1, "Platform sends a suspected scam message")
scam_msg = "Urgent attention required! Your account has been compromised. Click http://suspicious-link.net to verify immediately or call +1-555-0199."
print(f"Sending message: '{scam_msg}'")

resp1 = send_message(scam_msg, history=history)

if not resp1:
    exit(1)

# STEP 2: System analyzes and detects scam
print_step(2, "System Analysis & Detection")
print(f"Scam Detected: {resp1.get('scamDetected')}")
if resp1.get('scamDetected'):
    print("SUCCESS: Scam was detected correctly.")
else:
    print("FAILURE: Scam was NOT detected.")

# STEP 3: Agent Activation
print_step(3, "Agent Activation")
agent_reply = resp1.get('reply')
print(f"Agent Reply: {agent_reply}")
if agent_reply:
    print("SUCCESS: AI Agent was activated and replied.")
    # Update history for next turn
    history.append({"sender": "scammer", "text": scam_msg, "timestamp": int(time.time() * 1000) - 5000})
    history.append({"sender": "user", "text": agent_reply, "timestamp": int(time.time() * 1000) - 2000})
else:
    print("FAILURE: No reply from agent.")

# STEP 4: Intelligence Extraction
print_step(4, "Intelligence Extraction (Initial)")
intel = resp1.get('extractedIntelligence', {})
print("Extracted Intelligence:", json.dumps(intel, indent=2))
if intel.get('phishingLinks') or intel.get('phoneNumbers'):
    print("SUCCESS: Intelligence extracted from first message.")
else:
    print("WARNING: No intelligence extracted yet.")

# STEP 5: Conversation Continuation (Agent continues) & More Intelligence
print_step(5, "Conversation Continuation")
followup_msg = "Please send $500 to my crypto wallet 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa to unlock it."
print(f"Sending follow-up: '{followup_msg}'")

resp2 = send_message(followup_msg, history=history)

if not resp2:
    exit(1)

print(f"Agent Reply 2: {resp2.get('reply')}")
intel_2 = resp2.get('extractedIntelligence', {})
print("Updated Intelligence:", json.dumps(intel_2, indent=2))

if "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" in str(intel_2.get('cryptoWallets', [])) or "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" in str(intel_2):
    print("SUCCESS: New intelligence (Crypto Wallet) extracted.")

# STEP 6: Performance Evaluation
print_step(6, "Performance Evaluation (Metrics)")
metrics = resp2.get('engagementMetrics', {})
print("Metrics:", json.dumps(metrics, indent=2))
if metrics.get('totalMessagesExchanged') >= 3:
     print("SUCCESS: Message count reflects history.")
else:
     print("WARNING: Message count mismatch.")

print("\nEvaluation Flow Test Complete.")
