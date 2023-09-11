from django import forms
from .models import Callback


class CallbackForm(forms.ModelForm):
    class Meta:
        model = Callback
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mail_text', 'placeholder': 'Имя'}),
            'email': forms.EmailInput(attrs={'class': 'mail_text', 'placeholder': 'Почта'}),
            'phone': forms.TextInput(attrs={'class': 'mail_text', 'placeholder': 'Номер телефона'}),
            'message': forms.Textarea(attrs={'class': 'massage-bt', 'placeholder': 'Текст обращения', 'rows': '5'})
        }