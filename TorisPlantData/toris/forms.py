from .models import PlantProduction, Product, Order, Operator
from django.forms import ModelForm
from bootstrap_datepicker_plus import DatePickerInput
from django import forms


class PlantProductionForm(forms.ModelForm):
    class Meta:
        model = PlantProduction
        fields = ["date", "product_code", "plant", "shift", "operator_name", "no_of_winderman", "end_reading",
                  "start_reading", "wastage"]
        # widgets = {'date': forms.SelectDateWidget(attrs={'class': 'datepicker'})  }

    def __init__(self, *args, **kwargs):
        super(PlantProductionForm, self).__init__(*args, **kwargs)
        self.fields['shift'].empty_label = 'Select'
        self.fields['product_code'].empty_label = 'Select'
        self.fields['plant'].empty_label = 'Select'
        self.fields['operator_name'].empty_label = 'Select'
        self.fields['date'].widget = DatePickerInput(format='%d/%m/%Y')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {'order_date': forms.SelectDateWidget(), }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['product_code'].empty_label = 'Select'
        self.fields['order_date'].widget = DatePickerInput(format='%d/%m/%Y')
