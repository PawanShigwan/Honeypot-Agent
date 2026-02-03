import requests
import json
import traceback
import sys
from .config import settings

def send_guvi_callback(session_id: str, session_data: dict):
    """
    Sends the gathered intelligence to the GUVI evaluation endpoint.
    This should be called as a background task.
    """
    try:
        intel = session_data.get("intelligence")
        
        intel_dict = {
            "bankAccounts": intel.bankAccounts,
            "upiIds": intel.upiIds,
            "phishingLinks": intel.phishingLinks,
            "phoneNumbers": intel.phoneNumbers,
            "cryptoWallets": getattr(intel, "cryptoWallets", []),
            "suspiciousKeywords": intel.suspiciousKeywords
        }

        payload = {
            "sessionId": session_id,
            "scamDetected": session_data.get("scam_detected", False),
            "totalMessagesExchanged": session_data.get("total_messages", 0),
            "extractedIntelligence": intel_dict,
            "agentNotes": session_data.get("agent_notes", "Engaged with scammer, extracted intelligence.")
        }
        
        print(f"INFO: Sending Callback for {session_id} to {settings.GUVI_CALLBACK_URL}...", file=sys.stderr)
        
        # Send Request
        response = requests.post(
            settings.GUVI_CALLBACK_URL,
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
             print(f"SUCCESS: Callback sent for {session_id}. Resp: {response.text}", file=sys.stderr)
        else:
             print(f"WARNING: Callback failed for {session_id}. Status: {response.status_code} Resp: {response.text}", file=sys.stderr)
             
    except Exception as e:
        print(f"ERROR: Callback exception for {session_id}: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
