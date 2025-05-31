from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'address_line1': forms.TextInput(attrs={'placeholder': '123 Main St'}),
            'city': forms.TextInput(attrs={'placeholder': 'Your city'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'ZIP/Postal Code'}),
        }
