import uuid
# uuid needed to generate order number

from django.db import models
from django.db.models import Sum
from django.conf import settings

from products.models import Product

# model for each model 
class Order(models.Model):
    # order no. is auto generated and unique 
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    # text field that will contain the original shopping bag that created it
    original_bag = models.TextField(null=False, blank=False, default='')
    # character field that will contain the stripe payment intent id
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    # prepending the method name with an underscore means it will only be used inside this class 
    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        This generated a string of 32 numbers
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs using aggregate function.
        """
        # This works is by using the sum function across all the line-item 
        # total fields for all line items on this order. The default behaviour
        # is to add a new field to the query set called line-item total sum.
        # Which we can then get and set the order total to that.
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        # Now we can calculate delivery costs
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        # Now calculate grand total
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    # override default save method 
    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            # If the current order doesn't have an order number, one is assigned
            self.order_number = self._generate_order_number()
        # then execute original save method
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

# A line item is basically an individual shopping bag item 
class OrderLineItem(models.Model):
    # For each item in an order, this info is created and added to the order. Then the delivery cost, order total and grand totals are updated
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True) # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
