from django.contrib import admin
from .models import *

admin.site.register(Stock)
admin.site.register(Product)
# admin.site.register(State)
# admin.site.register(District)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(PurchaseInvoice)
admin.site.register(PurchaseInvoiceItem)
admin.site.register(UserProfile)