import google.generativeai as genai
from .config import settings
from .schemas import Message
from typing import List
import sys
import traceback

# Configure Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY, transport='rest')

class GeminiAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def detect_scam_ai(self, message: str) -> bool:
        """
        Uses Gemini to detect if a message is a scam.
        Returns True/False.
        """
        prompt = f"""
        Analyze the following message and determine if it is a SCAM or NOT_SCAM.
        Consider context: unsolicited offers, urgency, requests for bank details/OTP, threats of account blocking.
        
        Message: "{message}"
        
        Response only with "SCAM" or "NOT_SCAM".
        """
        try:
            response = self.model.generate_content(prompt)
            print(f"DEBUG GEMINI SCAM CHECK: {response.text}", file=sys.stderr)
            text = response.text.strip().upper()
            return "SCAM" in text and "NOT_SCAM" not in text
        except Exception as e:
            print(f"AI Detection Failed: {e}", file=sys.stderr)
            return False

    def generate_reply(self, message: str, history: List[Message]) -> str:
        """
        Generates a persona-based reply.
        Persona: Indian user, slightly confused, cooperative, but never reveals they know it's a scam.
        """
        
        # Format history for context
        history_text = ""
        for msg in history:
            role = "Scammer" if msg.sender == "scammer" else "Me"
            history_text += f"{role}: {msg.text}\n"
            
        prompt = f"""
        You are acting as a potential victim in a scambaiting scenario.
        YOUR PERSONA:
        - Name: Rahul
        - Location: Mumbai, India
        - Personality: Worried about bank account, slightly cooperative but asks verifying questions.
        - Tone: Slightly confused, eager to resolve the "issue" but needs reassurance.
        - Goal: Keep the scammer engaged. Ask if the payment/action will resolve the block immediately.
        - CRITICAL: NEVER reveal you know it is a scam. NEVER admit it is a bot.
        
        CONVERSATION HISTORY:
        {history_text}
        
        LATEST MESSAGE FROM SCAMMER:
        "{message}"
        
        Reply to the scammer as Rahul. Keep it short (1-2 sentences). Example: "Okay, if I pay this, will my account open immediately?" or "I am trying, but link is not opening."
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"AI Reply Failed: {e}", file=sys.stderr)
            return "Sorry sir, I am not understanding. Can you explain?"

agent = GeminiAgent()
