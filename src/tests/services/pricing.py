class PricingService:
    def __init__(self, rate: float):
        self.rate = rate

    def calculate_cost(self, minutes: float) -> float:
        return self.rate * minutes
