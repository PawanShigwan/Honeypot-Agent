from datetime import datetime, timezone
from typing import Dict, Any, List
from .schemas import ExtractedIntelligence

class SessionManager:
    def __init__(self):
        # sessionId -> session_data dict
        self.sessions: Dict[str, Any] = {}

    def get_or_create_session(self, session_id: str) -> Dict[str, Any]:
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "created_at": datetime.now(timezone.utc),
                "total_messages": 0,
                "scam_detected": False,
                "intelligence": ExtractedIntelligence(),
                "callback_sent": False,
                "messages": [],
                "agent_notes": ""
            }
        return self.sessions[session_id]

    def update_session(self, session_id: str, data: Dict[str, Any]):
        if session_id in self.sessions:
            self.sessions[session_id].update(data)

    def add_message(self, session_id: str, message: Any):
        if session_id in self.sessions:
            self.sessions[session_id]["messages"].append(message)
            self.sessions[session_id]["total_messages"] += 1

    def update_intelligence(self, session_id: str, new_intel: ExtractedIntelligence):
        if session_id in self.sessions:
            current = self.sessions[session_id]["intelligence"]
            
            # Merge lists and deduplicate
            current.bankAccounts = list(set(current.bankAccounts + new_intel.bankAccounts))
            current.upiIds = list(set(current.upiIds + new_intel.upiIds))
            current.phishingLinks = list(set(current.phishingLinks + new_intel.phishingLinks))
            current.phoneNumbers = list(set(current.phoneNumbers + new_intel.phoneNumbers))
            current.cryptoWallets = list(set(current.cryptoWallets + new_intel.cryptoWallets))
            current.emailAddresses = list(set(current.emailAddresses + new_intel.emailAddresses))
            current.socialMediaHandles = list(set(current.socialMediaHandles + new_intel.socialMediaHandles))
            current.suspiciousKeywords = list(set(current.suspiciousKeywords + new_intel.suspiciousKeywords))

session_store = SessionManager()
