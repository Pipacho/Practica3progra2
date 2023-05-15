from django import forms
from .models import perfil,archivo
class ProfileForm(forms.ModelForm):
    class Meta:
        model = perfil
        fields = ['cui', 'carrera', 'sexo']

class ArchivoForm(forms.ModelForm):
    class Meta:
        model = archivo
        fields = ['user','file']
        widgets = {'file': forms.FileInput(attrs={'accept':'.p2'})}

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        extension = uploaded_file.name.split('.')[-1]
        if extension.lower() != 'p2':
            raise forms.ValidationError('El archivo debe tener la extensión .p2')
        return uploaded_file