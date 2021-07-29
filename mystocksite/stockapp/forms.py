
from django.core.exceptions import ValidationError
from django import forms
from django.forms import ModelForm
from .models import Stock

class StockForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Stock
        fields = ['name','nse_symbol','yahoo_symbol',]


        def clean(self):
            cleaned_data = super().clean()
            name = cleaned_data.get("name")
            nse_symbol = cleaned_data.get("nse_symbol")
            yahoo_symbol = cleaned_data.get("yahoo_symbol")
            if not name:
                raise forms.ValidationError("You must enter name.")
            if not nse_symbol:
                raise forms.ValidationError("You must enter nse_symbol.")
            if not yahoo_symbol:
                raise forms.ValidationError("You must enter yahoo_symbol."   )

class FilterForm(forms.Form):
    FILTER_CHOICE = [
        ('new_intraday_high', 'New Intraday High'),
        ('new_closing_high', 'New Closing High'),
        ('new_intraday_low', 'New Intraday Low'),
        ('new_closing_low', 'New Closing Low'),
    ]

    filter = forms.CharField(label="filter",widget=forms.Select( choices=FILTER_CHOICE))