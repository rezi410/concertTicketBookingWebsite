from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Concert, GoldTicket, SliverTicket, BronzeTicket


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = '__all__'
    
class GoldTicketForm(forms.ModelForm):
    class Meta:
        model = GoldTicket
        fields = '__all__'


class SliverTicketForm(forms.ModelForm):
    class Meta:
        model = SliverTicket
        fields = '__all__'

class BronzeTicketForm(forms.ModelForm):
    class Meta:
        model = BronzeTicket
        fields = '__all__'
