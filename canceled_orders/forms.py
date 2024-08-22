from django import forms
from .models import CanceledOrder

class CanceledOrderForm(forms.ModelForm):
    class Meta:
        model = CanceledOrder
        fields = ['order_number', 'order_name', 'store_name', 'phone_number', 'comment', 'status']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 1}),
        }