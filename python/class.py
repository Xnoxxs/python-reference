
class PaymentService:

    @classmethod
    def process_payment(cls, amount: int):
        """Public method — can be called from outside"""
        print("Starting payment process...")
        fee = cls._calculate_fee(amount)   # internal use
        total = amount + fee
        print(f"Payment processed: {total}")
        return total

    @classmethod
    def _calculate_fee(cls, amount: int):
        """Internal (private) method — should NOT be used outside"""
        return int(amount * 0.05)

    @staticmethod
    def convert(amount: int):
        """Internal (private) method — should NOT be used outside"""
        return int(amount  / 100)


PaymentService.process_payment(amount=100)

"""
🔑 Rule of thumb (memorize this)
    ✅ Use @classmethod when:
    
    The method needs to call other methods in the same class
    
    The method depends on class-level configuration
    
    You may override the class later (subclassing)
    
    You want polymorphism / extensibility
    
    👉 Service classes, factories, repositories → usually @classmethod

✅ Use @staticmethod when:

    The method is pure logic
    
    It does not depend on class state
    
    It does not call other class methods
    
    It could live outside the class but is grouped there for clarity
    
    👉 Helpers, validators, formatters → usually @staticmethod
"""
