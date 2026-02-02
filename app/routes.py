from fastapi import APIRouter, Depends, BackgroundTasks, Request
from .schemas import HoneyPotRequest, HoneyPotResponse, EngagementMetrics
from .auth import verify_api_key
from .session_store import session_store
from .detector import detect_scam_rule_based, detect_suspicious_rule_based
from .extractor import extract_intelligence
from .agent import agent
from .callback import send_guvi_callback
from datetime import datetime, timezone
import sys

router = APIRouter()

@router.post("/honeypot", response_model=HoneyPotResponse)
async def honeypot_endpoint(
    request: HoneyPotRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    session = session_store.get_or_create_session(request.sessionId)
    
    # Update local session state
    session_store.add_message(request.sessionId, request.message)
    
    # 1. FAST DETECTION (Rules)
    is_confirmed_scam = session["scam_detected"]
    is_suspicious = False
    agent_notes = session.get("agent_notes", "")

    # Rule-based check
    is_high_conf_rule = detect_scam_rule_based(request.message.text)
    is_suspicious_rule = detect_suspicious_rule_based(request.message.text)
    
    # Intelligence check
    has_any_intelligence = any([
        session["intelligence"].bankAccounts,
        session["intelligence"].upiIds,
        session["intelligence"].phishingLinks,
        session["intelligence"].phoneNumbers
    ])

    if not is_confirmed_scam:
        if has_any_intelligence:
            is_confirmed_scam = True
            agent_notes = "Confirmed by Intelligence Extraction"
        elif is_high_conf_rule:
            is_confirmed_scam = True
            agent_notes = "Confirmed by High-Confidence Rules"
        elif is_suspicious_rule:
            is_suspicious = True
            agent_notes = "Suspicious behavior detected (Rules)"
        
        # Save state
        if is_confirmed_scam:
            session["scam_detected"] = True
            session["agent_notes"] = agent_notes
    
    # 2. ASYNC HEAVY LIFTING (Background Tasks)
    # We run AI detection and Intelligence extraction in background IF not already confirmed
    # to keep response time < 2s.
    
    def background_processing(sid: str, msg_text: str, sender: str):
        sess = session_store.sessions[sid]
        
        # Extract Intelligence from current message and history (source = scammer)
        full_conversation = request.conversationHistory + [request.message]
        for msg in full_conversation:
            if msg.sender == "scammer":
                intel = extract_intelligence(msg.text)
                session_store.update_intelligence(sid, intel)
            
        # Re-check scam state if not confirmed
        if not sess["scam_detected"]:
            # Check current message for AI detection
            if sender == "scammer":
                is_ai_scam = agent.detect_scam_ai(msg_text)
                if is_ai_scam:
                    sess["scam_detected"] = True
                    sess["agent_notes"] = "Confirmed by Gemini AI"
        
        # Trigger GUVI Callback if criteria met
        has_intel = any([
            sess["intelligence"].bankAccounts,
            sess["intelligence"].upiIds,
            sess["intelligence"].phishingLinks,
            sess["intelligence"].phoneNumbers
        ])
        
        should_send = sess["scam_detected"] and (has_intel or sess["total_messages"] >= 3)
        if should_send and not sess.get("callback_sent", False):
            sess["callback_sent"] = True
            send_guvi_callback(sid, sess)

    background_tasks.add_task(background_processing, request.sessionId, request.message.text, request.message.sender)

    # 3. REPLY GENERATION
    # If it's a scam or suspicious, generate a reply to keep them engaged
    reply_text = None
    if (is_confirmed_scam or is_suspicious or is_suspicious_rule) and request.message.sender == "scammer":
        # Note: generate_reply is relatively fast but could be moved to background if needed.
        # For now, we keep it here to provide a reply in the same response.
        reply_text = agent.generate_reply(request.message.text, request.conversationHistory)

    # Final Agent Notes for Response
    final_agent_notes = session.get("agent_notes", "Analyzing...")
    if is_confirmed_scam:
        notes_parts = [final_agent_notes]
        if session["intelligence"].upiIds:
            notes_parts.append(f"UPI: {', '.join(session['intelligence'].upiIds)}")
        final_agent_notes = " | ".join(notes_parts)

    duration = int((datetime.now(timezone.utc) - session["created_at"]).total_seconds())
    
    return HoneyPotResponse(
        scamDetected=is_confirmed_scam,
        engagementMetrics=EngagementMetrics(
            engagementDurationSeconds=duration,
        totalMessagesExchanged=len(request.conversationHistory) + 1
        ),
        extractedIntelligence=session["intelligence"],
        agentNotes=final_agent_notes,
        reply=reply_text
    )
