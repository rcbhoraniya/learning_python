from django import template

register = template.Library()


@register.simple_tag()
def divide(price, qty, *args, **kwargs):
    # you would need to do any localization of the result here
    return (price / qty).__round__(2)


@register.simple_tag()
def multiplay(price, qty, *args, **kwargs):
    # you would need to do any localization of the result here
    return (price * qty).__round__(2)


@register.simple_tag()
def profitpercentage(price_sum, today_value, *args, **kwargs):
    # you would need to do any localization of the result here
    return ((today_value * 100 / price_sum) - 100).__round__(2)


@register.simple_tag()
def portweight(price_sum, total_investment, *args, **kwargs):
    # you would need to do any localization of the result here
    return (price_sum * 100 / total_investment).__round__(2)


@register.simple_tag()
def profit(price_sum, close_price, qty_sum, *args, **kwargs):
    # you would need to do any localization of the result here
    return (close_price * qty_sum - price_sum).__round__(2)
