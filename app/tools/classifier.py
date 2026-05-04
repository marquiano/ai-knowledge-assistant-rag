def classify_intent(text: str) -> dict:
    normalized_text = text.lower()

    high_priority_words = [
        "urgent", "urgente", "immediately", "imediatamente",
        "critical", "crítico", "down", "fora do ar",
        "error", "erro", "failure", "falha"
    ]

    action_words = [
        "create", "crie", "send", "envie", "execute",
        "run", "rode", "notify", "notifique",
        "open", "abra", "call", "chame"
    ]

    priority = "high" if any(word in normalized_text for word in high_priority_words) else "normal"
    intent = "action" if any(word in normalized_text for word in action_words) else "information"

    return {
        "intent": intent,
        "priority": priority
    }