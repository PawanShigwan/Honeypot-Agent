import re
from .schemas import ExtractedIntelligence

# Regex Patterns
UPI_PATTERN = r"\b[\w.-]+@[\w.-]+\b"
BANK_AC_PATTERN = r"\b\d{12,18}\b"
PHONE_PATTERN = r"(?<!\d)(?:\+91[\-\s]?)?[6-9]\d{9}(?!\d)"
URL_PATTERN = r"https?://[^\s]+"
SUSPICIOUS_KEYWORDS_LIST = ["urgent", "verify", "blocked", "pay", "upi", "click", "suspend", "kyc", "lottery"]

def extract_intelligence(text: str) -> ExtractedIntelligence:
    intel = ExtractedIntelligence()
    
    # Extract UPI
    upi_matches = re.findall(UPI_PATTERN, text)
    if upi_matches:
        intel.upiIds = list(set(upi_matches))
        
    # Extract Bank Accounts (Generic 9-18 digit numbers)
    bank_matches = re.findall(BANK_AC_PATTERN, text)
    if bank_matches:
        intel.bankAccounts = list(set(bank_matches))

    # Extract Phone
    phone_matches = re.findall(PHONE_PATTERN, text)
    if phone_matches:
        intel.phoneNumbers = list(set(phone_matches))
        
    # Extract URLs
    url_matches = re.findall(URL_PATTERN, text)
    if url_matches:
        intel.phishingLinks = list(set(url_matches))
        
    # Extract Keywords
    text_lower = text.lower()
    found_keywords = [kw for kw in SUSPICIOUS_KEYWORDS_LIST if kw in text_lower]
    if found_keywords:
        intel.suspiciousKeywords = list(set(found_keywords))
        
    return intel
