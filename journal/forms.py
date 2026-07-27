from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Trade

# Tailwind classes for inputs (matches .floating-field in base.html)
FIELD_CLS = 'floating-field'
SELECT_CLS = 'floating-field'


class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['symbol', 'side', 'entry_price', 'exit_price', 'quantity', 'date', 'notes']
        widgets = {
            'symbol': forms.TextInput(attrs={
                'class': FIELD_CLS,
                'placeholder': ' ',
            }),
            'side': forms.Select(attrs={'class': SELECT_CLS}),
            'entry_price': forms.NumberInput(attrs={
                'class': FIELD_CLS,
                'placeholder': ' ',
                'step': '0.0001'
            }),
            'exit_price': forms.NumberInput(attrs={
                'class': FIELD_CLS,
                'placeholder': ' ',
                'step': '0.0001'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': FIELD_CLS,
                'placeholder': ' ',
                'step': '0.0001'
            }),
            'date': forms.DateInput(attrs={
                'class': FIELD_CLS,
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': FIELD_CLS,
                'rows': 3,
                'placeholder': ' ',
            }),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': FIELD_CLS, 'placeholder': ' '})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': FIELD_CLS,
            'placeholder': ' '
        })
        self.fields['password1'].widget.attrs.update({
            'class': FIELD_CLS + ' pl-12',
            'placeholder': ' '
        })
        self.fields['password2'].widget.attrs.update({
            'class': FIELD_CLS + ' pl-12',
            'placeholder': ' '
        })


class TradeFilterForm(forms.Form):
    symbol = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'floating-field',
            'placeholder': ' ',
        })
    )
    side = forms.ChoiceField(
        required=False,
        choices=[('', 'همه'), ('buy', 'خرید'), ('sell', 'فروش')],
        widget=forms.Select(attrs={'class': 'floating-field'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'floating-field',
            'type': 'date'
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'floating-field',
            'type': 'date'
        })
    )
