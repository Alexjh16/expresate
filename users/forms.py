from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users, Paises, RolesUser

class RegistroUserForm(UserCreationForm):
    pais = forms.ModelChoiceField(
        queryset=Paises.objects.all(),
        required=True,
        label="Pais"
    )
    rol = forms.ModelChoiceField(
        queryset=RolesUser.objects.all(),
        required=True,
        label="Rol"
    )

    class Meta(UserCreationForm.Meta):
        model = Users
        field = ('first_name', 'last_name', 'username', 'email', 'password', 'dispositivo', 'pais', 'edad', 'rol')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update