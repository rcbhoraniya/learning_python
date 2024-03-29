from django.core.exceptions import ValidationError
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ('username', 'password',)


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'required': True})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class StockForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['m_cap'].widget.attrs.update({'class': 'form-control'})
        self.fields['sector'].widget.attrs.update({'class': 'form-control'})
        self.fields['nse_symbol'].widget.attrs.update({'class': 'form-control'})
        self.fields['moneycontrol_symbol'].widget.attrs.update({'class': 'form-control'})
        self.fields['yahoo_symbol'].widget.attrs.update({'class': 'form-control'})
        self.fields['scrip_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_portfolio_stock'].widget.attrs.update({'class': "form-check"})

    class Meta:
        model = StockMap
        exclude = ['is_deleted', 'deleted_at']


class SectorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SectorForm, self).__init__(*args, **kwargs)
        self.fields['sector'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Sector
        fields = ['sector']


class StockDataForm(ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%d-%m-%Y %H:%M:%S'),
        input_formats=('%d-%m-%Y %H:%M:%S',)
    )

    def __init__(self, *args, **kwargs):
        super(StockDataForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['company'].widget.attrs.update({'class': 'form-control'})
        self.fields['side'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['trade_num'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = StockData
        exclude = ['is_deleted', 'deleted_at']


class HistoricalDataForm(ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
        input_formats=('%d/%m/%Y %H:%M:%S',)
    )

    def __init__(self, *args, **kwargs):
        super(HistoricalDataForm, self).__init__(*args, **kwargs)
        self.fields['company'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['open'].widget.attrs.update({'class': 'form-control'})
        self.fields['high'].widget.attrs.update({'class': 'form-control'})
        self.fields['low'].widget.attrs.update({'class': 'form-control'})
        self.fields['close'].widget.attrs.update({'class': 'form-control'})
        self.fields['adj_close'].widget.attrs.update({'class': 'form-control'})
        self.fields['volume'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = HistoricalData
        fields = ['company', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']

class StockFilterForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=StockMap.objects.all().filter(is_portfolio_stock=True), to_field_name="id")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-select'})
        # self.fields['name'].queryset = StockMap.objects.all()


    class Meta:
        model = StockMap
        fields = ['id', 'name']


class FilterForm(forms.Form):
    FILTER_CHOICE = [
        ('new_intraday_high', 'New Intraday High'),
        ('new_closing_high', 'New Closing High'),
        ('new_intraday_low', 'New Intraday Low'),
        ('new_closing_low', 'New Closing Low'),
    ]

    filter = forms.CharField(label="filter", widget=forms.Select(choices=FILTER_CHOICE))
