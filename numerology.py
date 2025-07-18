def get_luck_prediction(number):
    digits = [int(d) for d in str(number) if d.isdigit()]
    total = sum(digits)
    while total > 9:
        total = sum(int(d) for d in str(total))
    lucky = total in [1, 3, 5, 6]
    result = "🍀 Lucky" if lucky else "⚠️ Unlucky"
    return f"Numerology Total: {total}\nResult: {result}"