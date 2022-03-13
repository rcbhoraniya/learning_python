from django.forms import ModelForm
from .models import Customer
from .models import Product
from .models import UserProfile
from .models import InventoryLog
from .models import BookLog
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class CustomerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer_name'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['customer_address'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['customer_phone'].widget.attrs.update(
            {'class': 'form-control', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Numbers only',
             'required': 'true'})
        self.fields['customer_gst'].widget.attrs.update({'class': 'form-control', 'maxlength': '15',
                                                         'pattern': '[A-Z0-9]{15}', 'title': 'GSTIN Format Required',
                                                         'required': 'true'})

    class Meta:
        model = Customer
        fields = ['customer_name', 'customer_address', 'customer_phone', 'customer_gst']


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['product_hsn'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['product_unit'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['product_gst_percentage'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['product_rate_with_gst'].widget.attrs.update({'class': 'form-control', 'required': 'true'})

    class Meta:
        model = Product
        fields = ['product_name', 'product_hsn', 'product_unit', 'product_gst_percentage', 'product_rate_with_gst']


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['business_title'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['business_address'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['business_email'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['business_phone'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['business_gst'].widget.attrs.update({'class': 'form-control', 'required': 'true'})

    class Meta:
        model = UserProfile
        fields = ['business_title', 'business_address', 'business_email', 'business_phone', 'business_gst']


class InventoryLogForm(ModelForm):
    class Meta:
        model = InventoryLog
        fields = ['date', 'change', 'change_type', 'description']


class BookLogForm(ModelForm):
    class Meta:
        model = BookLog
        fields = ['date', 'change', 'change_type', 'description']
