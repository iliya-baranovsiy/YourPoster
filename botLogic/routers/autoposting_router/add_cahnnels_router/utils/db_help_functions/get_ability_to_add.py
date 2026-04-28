from .payment_plans_limits import PaymentLimit


def get_ability_to_add(channels_list: list, payment_plan: str) -> tuple:
    ability_default_count = PaymentLimit[payment_plan].value
    ability_count = ability_default_count - len(channels_list)
    return True if ability_count > 0 else False, payment_plan, ability_count
