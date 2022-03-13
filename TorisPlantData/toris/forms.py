from .models import PlantProduction, Product, Order, Employee, Plant
from django.forms import ModelForm
from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password',)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ScientificNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.getScientifName()


class PlantProductionForm(forms.ModelForm):
    class Meta:
        model = PlantProduction
        fields = ["date", "product_code", "plant", "shift", "operator_name", "no_of_winderman", "end_reading",
                  "start_reading", "wastage"]

    def __init__(self, *args, **kwargs):
        super(PlantProductionForm, self).__init__(*args, **kwargs)
        self.fields['shift'].empty_label = 'Select'
        self.fields['product_code'] = ScientificNameChoiceField(queryset=Product.objects.all().order_by('product_code'),
                                                                empty_label="Choose a Product Code", )
        self.fields['plant'].empty_label = 'Select'
        self.fields['operator_name'].empty_label = 'Select'
        self.fields['date'].widget = DatePickerInput(format='%d/%m/%Y', attrs={'autofocus': True})


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('is_deleted', 'deleted_at')


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ('is_deleted', 'deleted_at')


class OrderForm(ModelForm):
    class Meta:
        model = Order
        widgets = {'order_date': forms.SelectDateWidget(), }
        exclude = ('is_deleted', 'deleted_at')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['product_code'] = ScientificNameChoiceField(queryset=Product.objects.all(),
                                                                empty_label="Choose a Product Code", )

        self.fields['order_date'].widget = DatePickerInput(format='%d/%m/%Y', attrs={'autofocus': True})
