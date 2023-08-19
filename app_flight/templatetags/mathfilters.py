from django import template

register = template.Library()


@register.filter
def mult(value, arg):
    "Multiplies the arg and the value"
    return int(value) * int(arg)


@register.filter
def sub(value, arg):
    "Subtracts the arg from the value"
    return round(float(value) - float(arg), 2)


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


@register.simple_tag(takes_context=True)
def ticket_total_amount(context, ticket):
    request = context["request"]
    traveler_adult = int(request.GET.get("traveler_adult", 1))
    traveler_child = int(request.GET.get("traveler_child", 0))
    traveler_infant = int(request.GET.get("traveler_infant", 0))
    total_adult_amount = ticket.get_ticket_price_method(
        passenger_type="adult", traveler=traveler_adult
    )
    total_child_amount = ticket.get_ticket_price_method(
        passenger_type="child", traveler=traveler_child
    )
    total_infant_amount = ticket.get_ticket_price_method(
        passenger_type="infant", traveler=traveler_infant
    )
    total_amount = total_adult_amount + total_child_amount + total_infant_amount
    discount_amount = round(ticket.get_ticket_discount_price(total_amount), 2)
    return [total_amount, round(total_amount - discount_amount, 2),]
