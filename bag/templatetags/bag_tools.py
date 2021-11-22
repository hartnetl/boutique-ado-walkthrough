from django import template


register = template.Library()

''' Calculate the subtotal for products '''
# This wrapper registers the function in a template filter 
# Look at django documentation (creating custom template tags and filters) for a full explanation
@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity
