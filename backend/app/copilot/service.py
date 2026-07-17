from sqlalchemy.orm import Session
from typing import Optional, List
import requests
import json

from app.core.config import settings
from app.models.chat import Conversation, Message
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse, ConversationSummary
from app.copilot.context import build_erp_context, SYSTEM_PROMPT_BASE


# ── Conversation management ───────────────────────────────────────────────────

def get_conversations(db: Session, user_id: int) -> List[ConversationSummary]:
    convs = db.query(Conversation).filter(
        Conversation.user_id == user_id,
        Conversation.is_active == True,
    ).order_by(Conversation.updated_at.desc()).all()

    result = []
    for c in convs:
        msg_count = db.query(Message).filter(Message.conversation_id == c.id).count()
        result.append(ConversationSummary(
            id=c.id,
            title=c.title,
            module_context=c.module_context,
            created_at=c.created_at,
            message_count=msg_count,
        ))
    return result


def get_conversation(db: Session, conv_id: int, user_id: int) -> Optional[Conversation]:
    return db.query(Conversation).filter(
        Conversation.id == conv_id,
        Conversation.user_id == user_id,
    ).first()


def delete_conversation(db: Session, conv_id: int, user_id: int) -> bool:
    conv = get_conversation(db, conv_id, user_id)
    if not conv:
        return False
    conv.is_active = False
    db.commit()
    return True


# ── Chat ──────────────────────────────────────────────────────────────────────

def chat(db: Session, user: User, request: ChatRequest) -> ChatResponse:
    # Get or create conversation
    if request.conversation_id:
        conv = get_conversation(db, request.conversation_id, user.id)
        if not conv:
            conv = _create_conversation(db, user.id, request.module_context, request.message)
    else:
        conv = _create_conversation(db, user.id, request.module_context, request.message)

    # Save user message
    user_msg = Message(
        conversation_id=conv.id,
        role="user",
        content=request.message,
    )
    db.add(user_msg)
    db.flush()

    # Build history (last 10 messages)
    history = db.query(Message).filter(
        Message.conversation_id == conv.id,
        Message.id != user_msg.id,
    ).order_by(Message.created_at.desc()).limit(9).all()
    history.reverse()

    # Build messages list
    erp_context = build_erp_context(db, request.module_context)
    system_content = SYSTEM_PROMPT_BASE.format(context=erp_context)

    messages = [{"role": "system", "content": system_content}]
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": request.message})

    # Call Ollama or OpenAI
    if settings.USE_OLLAMA:
        reply_content, tokens = _call_ollama(messages)
    else:
        reply_content, tokens = _call_openai(messages)

    # Save assistant reply
    assistant_msg = Message(
        conversation_id=conv.id,
        role="assistant",
        content=reply_content,
        tokens_used=tokens,
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(user_msg)
    db.refresh(assistant_msg)

    # Auto-title conversation on first exchange
    if not conv.title:
        conv.title = request.message[:60] + ("..." if len(request.message) > 60 else "")
        db.commit()

    return ChatResponse(
        conversation_id=conv.id,
        message=user_msg,
        reply=assistant_msg,
    )


def _create_conversation(db: Session, user_id: int,
                         module_context: Optional[str], first_message: str) -> Conversation:
    conv = Conversation(
        user_id=user_id,
        module_context=module_context,
        title=None,
    )
    db.add(conv)
    db.flush()
    return conv


# ── Ollama (local AI — no API key needed) ─────────────────────────────────────

def _call_ollama(messages: list) -> tuple:
    """Call local Ollama server. Falls back gracefully if not running."""
    try:
        url = f"{settings.OLLAMA_BASE_URL}/api/chat"
        payload = {
            "model": settings.OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 1024,
            }
        }
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        content = data.get("message", {}).get("content", "")
        tokens = data.get("eval_count", 0)
        return content, tokens
    except requests.exceptions.ConnectionError:
        return (
            "⚠️ Ollama is not running. Start it with: `ollama serve` in your terminal. "
            "Then make sure the model is pulled: `ollama pull llama3.2`",
            0,
        )
    except Exception as e:
        return f"Error communicating with Ollama: {str(e)}", 0


# ── OpenAI (fallback — requires API key) ─────────────────────────────────────

def _call_openai(messages: list) -> tuple:
    """Call OpenAI. Fallback when USE_OLLAMA=False."""
    if not settings.OPENAI_API_KEY:
        return (
            "⚠️ No AI backend configured. Either start Ollama locally or set OPENAI_API_KEY in .env",
            0,
        )
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        content = response.choices[0].message.content or ""
        tokens = response.usage.total_tokens if response.usage else 0
        return content, tokens
    except Exception as e:
        return f"Error communicating with OpenAI: {str(e)}", 0
