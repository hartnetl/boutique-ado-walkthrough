# post here means after 
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem

@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    Handles signals from the post save event
    Here: sender=orderlineitem, instance of the model that sent it, a boolean
    by django saying if this is a new instance or one being updated and any 
    keyword arguements
    Our code inside the method is really simple.
    We just have to access instance.order - which refers to the order this 
    specific line item is related to - and call the update_total method on it.
    To execute this function anytime the post_save signal is sent use the 
    receiver decorator, telling it we're receiving post saved signals from the
    OrderLineItem model.
    """
    instance.order.update_total()

@receiver(post_delete, sender=OrderLineItem)
def update_on_save(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    Same same as above, but different
    * Note: There's an error here that will be addressed later *
    """
    instance.order.update_total()