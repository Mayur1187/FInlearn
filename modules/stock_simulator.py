import random
from datetime import datetime

class StockMarket:

    def get_live_candle(self):
        base = random.randint(100, 150)

        o = base
        c = base + random.randint(-10, 10)
        h = max(o, c) + random.randint(0, 10)
        l = min(o, c) - random.randint(0, 10)

        return {
            "x": datetime.now().isoformat(),
            "o": o,
            "h": h,
            "l": l,
            "c": c
        }
    
def get_live_candle(self):
    import random
    base = random.randint(100, 120)

    return [
        {"x": "2024-01-01", "o": base, "h": base+10, "l": base-5, "c": base+5},
        {"x": "2024-01-02", "o": base+5, "h": base+15, "l": base, "c": base+10},
        {"x": "2024-01-03", "o": base+10, "h": base+20, "l": base+5, "c": base+15}
    ]