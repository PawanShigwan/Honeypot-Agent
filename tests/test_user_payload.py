import sys
import os
import json
from pydantic import ValidationError

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.schemas import HoneyPotRequest

def test_user_suggested_payload():
    print("Testing user-suggested payload compatibility...")
    payload = {
      "sessionId": "wertyu-dfghj-ertyui",
      "message": {
        "sender": "scammer",
        "text": "Your bank account is blocked. Verify now.",
        "timestamp": 1770005528731
      },
      "conversationHistory": [],
      "metadata": {
        "channel": "SMS",
        "language": "English",
        "locale": "IN"
      }
    }
    
    try:
        request = HoneyPotRequest(**payload)
        print("Payload parsing successful.")
        assert request.sessionId == "wertyu-dfghj-ertyui"
        assert request.message.timestamp == 1770005528731
        assert request.metadata.channel == "SMS"
        print("User-suggested payload test PASSED.")
    except Exception as e:
        print(f"Payload parsing FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_user_suggested_payload()
