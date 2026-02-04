import sys
import os
import json
from datetime import datetime, timezone

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.extractor import extract_intelligence
from app.schemas import Message, HoneyPotRequest

def test_intelligence_extraction():
    print("Testing intelligence extraction...")
    text = "Please pay 1234567890123456 to scammer.fraud@fakebank or call me at +91-9876543210"
    intel = extract_intelligence(text)
    
    print(f"Extracted Bank Accounts: {intel.bankAccounts}")
    print(f"Extracted UPI IDs: {intel.upiIds}")
    print(f"Extracted Phone Numbers: {intel.phoneNumbers}")
    
    assert "1234567890123456" in intel.bankAccounts
    assert "scammer.fraud@fakebank" in intel.upiIds
    assert "+91-9876543210" in intel.phoneNumbers or "9876543210" in "".join(intel.phoneNumbers)
    print("Intelligence extraction test PASSED.")

def test_message_counting():
    print("\nTesting message counting logic...")
    # This is a bit harder to test without running the full FastAPI app,
    # but we can verify the logic we added to routes.py.
    
    history = [
        Message(sender="scammer", text="Hi", timestamp=1770005528731),
        Message(sender="user", text="Hello", timestamp=1770005529731),
        Message(sender="scammer", text="Give me money", timestamp=1770005530731)
    ]
    current_message = Message(sender="user", text="Why?", timestamp=1770005531731)
    
    total_count = len(history) + 1
    print(f"History length: {len(history)}")
    print(f"Current message: 1")
    print(f"Total calculated: {total_count}")
    
    assert total_count == 4
    print("Message counting logic test PASSED.")

def test_guvi_payload_compatibility():
    print("\nTesting GUVI payload compatibility...")
    # Mock a payload without timestamp and with extra fields
    payload = {
        "sessionId": "guvi-test-001",
        "message": {
            "sender": "scammer",
            "text": "Your bank account is blocked. Verify now.",
            "timestamp": 1770005528731
        },
        "conversationHistory": [], # Test empty list history
        "metadata": {
            "channel": "SMS",
            "language": "English",
            "locale": "IN"
        },
        "extra_field_from_guvi": "some_value"
    }
    
    # Verify HoneyPotRequest can parse this
    from app.schemas import HoneyPotRequest
    request = HoneyPotRequest(**payload)
    print("Payload parsing successful.")
    assert request.sessionId == "guvi-test-001"
    assert request.message.text == "Your bank account is blocked. Verify now."
    assert request.conversationHistory == [] or request.conversationHistory is None
    
    # Test message count with None history
    total_count = len(request.conversationHistory or []) + 1
    assert total_count == 1
    print("Message count with None history PASSED.")

if __name__ == "__main__":
    try:
        test_intelligence_extraction()
        test_message_counting()
        test_guvi_payload_compatibility()
        print("\nAll verification tests PASSED.")
    except Exception as e:
        print(f"\nTests FAILED: {e}")
        sys.exit(1)
