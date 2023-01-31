from django import forms
from django.db.models import Max
from django.forms import formset_factory, BaseFormSet

from .models import *


class InventoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):  # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'form-control', 'type': 'text'})
        self.fields['current_stock'].widget.attrs.update({'class': 'form-control', 'type': 'text', 'min': '0'})
        self.fields['alert_level'].widget.attrs.update({'class': 'form-control', 'type': 'text', 'min': '0'})

    class Meta:
        model = Inventory
        fields = ['product', 'current_stock', 'alert_level']


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):  # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'type': 'text'})
        self.fields['hsn'].widget.attrs.update({'class': 'form-control', 'type': 'text'})
        self.fields['unit'].widget.attrs.update({'class': 'form-control', 'type': 'text'})
        self.fields['rate_without_gst'].widget.attrs.update({'class': 'form-control', 'type': 'text'})
        self.fields['profit_margin_percentage'].widget.attrs.update({'class': 'form-control', 'type': 'text'})
        self.fields['gst_percentage'].widget.attrs.update({'class': 'form-control', 'type': 'text'})

    class Meta:
        model = Product
        fields = ['name', 'hsn', 'unit', 'rate_without_gst', 'profit_margin_percentage', 'gst_percentage']


