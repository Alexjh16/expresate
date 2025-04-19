from django import forms
from altcha import verify_solution
from django.contrib.auth.forms import UserCreationForm
from .models import Users, Paises, RolesUser


class registrarUserForm(UserCreationForm):
    pais = forms.ModelChoiceField(
        queryset=Paises.objects.all(),
        required=True,
        label="País"
    )
    rol = forms.ModelChoiceField(
        queryset=RolesUser.objects.all(),
        required=True,
        label="Rol"
    )    
    class Meta(UserCreationForm.Meta):
        model = Users
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'dispositivo', 'pais', 'edad', 'rol')
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name or not first_name.strip():
            raise forms.ValidationError("Por favor ingresa tus nombres.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name or not last_name.strip():
            raise forms.ValidationError("Por favor ingresa tus apellidos.")
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Users.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya está en uso. Por favor elige otro.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está registrado. Por favor usa otro.")
        return email

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad < 7 or edad > 120:
            raise forms.ValidationError("La edad debe estar entre 7 y 120 años.")
        return edad

    def clean_pais(self):
        pais = self.cleaned_data.get('pais')
        if not Paises.objects.filter(id=pais.id).exists():
            raise forms.ValidationError("Por favor selecciona un país válido.")
        return pais

    def clean_rol(self):
        rol = self.cleaned_data.get('rol')
        if not RolesUser.objects.filter(id=rol.id).exists():
            raise forms.ValidationError("Por favor selecciona un rol válido.")
        return rol
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("La contraseña debe contener al menos una letra.")
        return password

    def clean_dispositivo(self):
        dispositivo = self.cleaned_data.get('dispositivo')
        dispositivos_permitidos = ['smartphone', 'tablet', 'laptop', 'desktop']
        if dispositivo not in dispositivos_permitidos:
            raise forms.ValidationError("Por favor selecciona un dispositivo válido.")
        return dispositivo

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data
