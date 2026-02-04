import re

HIGH_CONFIDENCE_SCAM_KEYWORDS = [
    r"verify.*immediately",
    r"account.*blocked",
    r"suspended",
    r"kyc",
    r"upi.*id",
    r"pay.*upi",
    r"lottery",
    r"winner",
    r"prize",
    r"urgent",
    r"click.*link",
    r"password",
    r"otp",
    r"expire",
    r"credit.*card",
    r"transfer.*to",
    r"account.*number",
    r"phishing",
    r"suspicious.*activity",
    r"tax.*department",
    r"unpaid.*taxes",
    r"legal.*action",
    r"package.*waiting",
    r"claim.*prize",
    r"claim.*it",
    r"pay.*penalty",
    r"refund.*process"
]

SUSPICIOUS_BEHAVIOR_KEYWORDS = [
    r"account.*flagged",
    r"unusual.*activity",
    r"verification.*required",
    r"urgent.*message",
    r"official.*notice",
    r"security.*alert",
    r"action.*needed",
    r"customer.*care",
    r"calling.*from.*the"
]

def detect_scam_rule_based(text: str) -> bool:
    """Detects high-confidence scams based on rules."""
    text_lower = text.lower()
    for pattern in HIGH_CONFIDENCE_SCAM_KEYWORDS:
        if re.search(pattern, text_lower):
            return True
    return False

def detect_suspicious_rule_based(text: str) -> bool:
    """Detects suspicious behavior that might be a scam but isn't confirmed yet."""
    text_lower = text.lower()
    for pattern in SUSPICIOUS_BEHAVIOR_KEYWORDS:
        if re.search(pattern, text_lower):
            return True
    return False
