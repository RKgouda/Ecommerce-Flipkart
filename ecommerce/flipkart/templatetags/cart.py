from django import template

register = template.Library()

@register.filter(name="isexistsincart")
def isexistsincart(product,cart):
    keys = cart.keys()
    for key in keys:
        if int(key) == product.id:
            return True
    return False

@register.filter(name="cart_quantity")
def cart_quantity(product,cart):
    keys = cart.keys()
    for key in keys:
        if int(key) == product.id:
            return cart.get(key)
    return False

@register.filter(name="total_price")
def total_price(product,cart):
   return product.product_price * cart_quantity(product,cart)

@register.filter(name="payable_amount")
def payable_amount(product,cart):
    s = 0
    for i in product:
        s = s + total_price(i,cart)
    return s

@register.filter(name="order_total_price")
def order_total_price(price,quantity):
   return price * quantity
