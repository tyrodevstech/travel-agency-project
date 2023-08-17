from django import template

register = template.Library()

@register.filter
def mult(value, arg):
    "Multiplies the arg and the value"
    return int(value) * int(arg)

@register.filter
def sub(value, arg):
    "Subtracts the arg from the value"
    return round(float(value) - float(arg),2)

@register.filter
def div(value, arg):
    "Divides the value by the arg"
    return int(value) / int(arg)


@register.filter
def get_pay_price(subtotal, discount_price):
    return float(subtotal) - float(discount_price)


@register.filter
def get_tour_discount_price(subtotal, discount_price):
    return float(subtotal) - float(discount_price)

@register.filter(takes_context=True)
def get_ticket_total_amount(context, ticket):
    print(context)
    return ticket