from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm  as BaseAuthenticationForm
from django.contrib.auth import authenticate

from django import forms
from .models import Custom_User

class Custom_User_Creation_Form(UserCreationForm):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control mb-4 w-75 border border-black border-2','name':"password1",'id':"password1"})
        self.fields['password2'].widget.attrs.update({'class': 'form-control mb-4 w-75 border border-black border-2','name':"password2",'id':"password2"})
        self.fields['nit'].widget.attrs.update({'class': 'form-control mb-4 w-75 border border-black border-2','name':"nit",'id':"nit"})
        self.fields['email'].widget.attrs.update({'class': 'form-control mb-4 w-75 border border-black border-2','name':"email",'id':"email"})
        self.fields['name'].widget.attrs.update({'class': 'form-control mb-4 w-75 border border-black border-2','name':"name",'id':"name"})
        
    class Meta:
        model = Custom_User
        fields = ('nit', 'name', 'email','password1','password2')

    from django import forms
from django.contrib.auth.forms import AuthenticationForm

class Custom_Login_Form(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control mb-4 w-75 border border-black border-2',
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-4 w-75 border border-black border-2',
        }),
    )


