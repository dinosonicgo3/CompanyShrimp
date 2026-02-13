import logging

class PricingCalculator:
    def __init__(self, config=None):
        self.config = config or {"markup_ratio": 1.3, "add_fee": 10}
        self.logger = logging.getLogger("shrimp.pricing")

    def calculate(self, original_price):
        try:
            markup_ratio = self.config.get("markup_ratio", 1.3)
            add_fee = self.config.get("add_fee", 10)
            
            final_price = int(original_price * markup_ratio + add_fee)
            self.logger.info(f"計算定價: 原價 {original_price} -> 售價 {final_price}")
            return final_price
        except Exception as e:
            self.logger.error(f"計算定價失敗: {str(e)}")
            return original_price
