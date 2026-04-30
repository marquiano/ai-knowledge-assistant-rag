def estimate_openai_cost(prompt: str, answer: str) -> float:
    """
    Rough estimation for demo purposes.
    Uses a simple approximation: 1 token ≈ 4 characters.
    Adjust pricing according to the model used.
    """
    input_tokens = len(prompt) / 4
    output_tokens = len(answer) / 4

    # Approximate GPT-4o-mini prices; update if needed.
    input_cost_per_1m = 0.15
    output_cost_per_1m = 0.60

    cost = (input_tokens / 1_000_000 * input_cost_per_1m) + (
        output_tokens / 1_000_000 * output_cost_per_1m
    )

    return round(cost, 6)
