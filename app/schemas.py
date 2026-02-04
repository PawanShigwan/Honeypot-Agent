from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

class Message(BaseModel):
    sender: str  # Must be "scammer" or "user"
    text: str
    timestamp: int  # Epoch milliseconds

class Metadata(BaseModel):
    channel: str = "SMS"
    language: str = "English"
    locale: str = "IN"

class HoneyPotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message] = []
    metadata: Metadata = Field(default_factory=Metadata)

    class Config:
        extra = "allow"

class EngagementMetrics(BaseModel):
    engagementDurationSeconds: int = 0
    totalMessagesExchanged: int = 0

class ExtractedIntelligence(BaseModel):
    bankAccounts: List[str] = []
    upiIds: List[str] = []
    phishingLinks: List[str] = []
    phoneNumbers: List[str] = []
    cryptoWallets: List[str] = []
    emailAddresses: List[str] = []
    socialMediaHandles: List[str] = []
    sessionId: str = ""
    suspiciousKeywords: List[str] = []

class HoneyPotResponse(BaseModel):
    scamDetected: bool
    engagementMetrics: EngagementMetrics
    extractedIntelligence: ExtractedIntelligence
    agentNotes: str = ""
    reply: Optional[str] = None
