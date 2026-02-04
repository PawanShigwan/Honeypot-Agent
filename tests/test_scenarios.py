import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/honeypot"
HEADERS = {
    "x-api-key": "secret-key-123",
    "Content-Type": "application/json"
}

scenarios = [
  {
    "name": "Crypto Scam",
    "text": "Invest $1000 in Bitcoin now and get 300% guaranteed returns in 24 hours! Send to wallet: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
    "expect_scam": True
  },
  {
    "name": "Job Scam",
    "text": "Congratulations! You have been selected for the Data Entry role. Salary $5000/month. Please pay $50 registration fee via UPI to hr_verify@upi to proceed.",
    "expect_scam": True
  },
  {
    "name": "Tech Support Scam",
    "text": "Microsoft Security Alert: Your computer is infected. Call 1-800-123-4567 immediately to speak to a technician.",
    "expect_scam": True
  },
  {
    "name": "Legitimate Message (False Positive Check)",
    "text": "Hey, are we still on for lunch tomorrow at 1 PM? Let me know.",
    "expect_scam": False
  }
]

def run_scenario(scenario):
    session_id = f"test-scenario-{int(time.time())}-{scenario['name'].split()[0].lower()}"
    print(f"\n--- Running Scenario: {scenario['name']} ---")
    print(f"Input Text: {scenario['text']}")
    
    payload = {
        "sessionId": session_id,
        "message": {
            "sender": "scammer",
            "text": scenario['text'],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        },
        "conversationHistory": []
    }
    
    try:
        response = requests.post(BASE_URL, headers=HEADERS, json=payload)
        data = response.json()
        
        is_scam = data.get("scamDetected")
        print(f"Scam Detected: {is_scam}")
        
        if is_scam == scenario['expect_scam']:
            print("✅ PASS: Detection matches expectation.")
        else:
            print(f"❌ FAIL: Expected {scenario['expect_scam']} but got {is_scam}")
            
        if is_scam:
            print(f"Agent Reply: {data.get('reply')}")
            intel = data.get('extractedIntelligence', {})
            # Compact print of non-empty intel
            found_intel = {k: v for k, v in intel.items() if v and v != []}
            if found_intel:
                print(f"Extracted Intel: {json.dumps(found_intel)}")
            else:
                print("No specific intel extracted (generic scam).")
        
    except Exception as e:
        print(f"Error running scenario: {e}")

for s in scenarios:
    run_scenario(s)
    time.sleep(1) # Brief pause between tests
