import re
from .schemas import ExtractedIntelligence

# Regex Patterns
UPI_PATTERN = r"\b[\w.-]+@[\w.-]+\b"
BANK_AC_PATTERN = r"\b\d{9,18}\b"
PHONE_PATTERN = r"(?<!\d)(?:\+91[\-\s]?)?[6-9]\d{9}(?!\d)"
URL_PATTERN = r"https?://[^\s]+"
# Simple regex for BTC/ETH style wallets
CRYPTO_PATTERN = r"\b(?:[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[ac-hj-np-z02-9]{11,71}|0x[a-fA-F0-9]{40}|[a-zA-Z0-9]{30,50})\b"
EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
SUSPICIOUS_KEYWORDS_LIST = ["urgent", "verify", "blocked", "pay", "upi", "click", "suspend", "kyc", "lottery"]

def extract_intelligence(text: str) -> ExtractedIntelligence:
    intel = ExtractedIntelligence()
    
    # Extract UPI
    upi_matches = re.findall(UPI_PATTERN, text)
    if upi_matches:
        intel.upiIds = list(set(upi_matches))
        
    # Extract Bank Accounts
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
        
    # Extract Crypto
    crypto_matches = re.findall(CRYPTO_PATTERN, text)
    if crypto_matches:
        intel.cryptoWallets = list(set(crypto_matches))
        
    # Extract Emails
    email_matches = re.findall(EMAIL_PATTERN, text)
    if email_matches:
        intel.emailAddresses = list(set(email_matches))
        
    # Extract Keywords
    text_lower = text.lower()
    found_keywords = [kw for kw in SUSPICIOUS_KEYWORDS_LIST if kw in text_lower]
    if found_keywords:
        intel.suspiciousKeywords = list(set(found_keywords))
        
    return intel
