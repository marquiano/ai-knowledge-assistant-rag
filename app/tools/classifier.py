def classify_intent(text: str) -> dict:
    text = text.lower()

    if any(word in text for word in ["urgent", "now", "immediately"]):
        priority = "high"
    else:
        priority = "normal"

    if any(word in text for word in ["create", "send", "execute"]):
        intent = "action"
    else:
        intent = "information"

    return {
        "intent": intent,
        "priority": priority
    }