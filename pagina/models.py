from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


# Create your models here.
opciones_carrera=[
    [0,'Matematica'],
    [1, 'Fisica']
]
opciones_sexo=[
    [0,'Masculino'],
    [1, 'Femenino']
]

class perfil(models.Model):
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    carrera=models.IntegerField(choices=opciones_carrera,blank=False,null=True)
    sexo=models.IntegerField(choices=opciones_sexo, blank=False, null=True)
    cui=models.IntegerField(blank=False, null=True)



    def __str__(self):
        return self.user.username+' (perfil)'


class archivo(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    file=models.FileField(blank=False, null=True, validators=[FileExtensionValidator(['p2'])])

    def __str__(self):
        return self.file.name

    def extension(self):
        extension = self.file.name.split('.')[-1]
        return extension.lower()