import pygments
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import perfil,archivo
from .forms import ProfileForm,ArchivoForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.lexers import PythonLexer
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponse
import datetime

# Create your views here.
def home(request):
    return render(request, 'pagina/home.html')

def registro(request):
    if request.method == 'POST':
        u_form = UserCreationForm(request.POST)
        p_form = ProfileForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()

            username = u_form.cleaned_data['username']
            sexo = p_form.cleaned_data['sexo']
            carrera = p_form.cleaned_data['carrera']
            user = User.objects.get(username=username)
            cui = p_form.cleaned_data['cui']

            hola = perfil.objects.create(user=user, sexo=sexo, carrera=carrera, cui=cui)
            hola.save()
            messages. success(request, f'Usuario {username} creado exitosamente')
            return redirect('home')
    else:
        u_form = UserCreationForm()
        p_form = ProfileForm()
    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'pagina/registro.html', context)
def profile(request):
    return render (request, 'pagina/profile.html')

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            messages.success(request, 'El archivo se ha cargado exitosamente')
            return redirect('file_repository')
    else:
        form = ArchivoForm()
    return render(request, 'pagina/upload_file.html', {'form': form})

@login_required
def file_repository(request):
    if request.user.is_superuser:
        uploaded_files = archivo.objects.all()
    else:
        uploaded_files = archivo.objects.filter(user=request.user)
    return render(request, 'pagina/file_repository.html', {'uploaded_files': uploaded_files})

def analizador(file_content):
    enteros = r'\b\d+\b'
    reales = r'\b[-+]?\d+\.\d+\b'
    notacioncientifica = r'\b[-+]?\d+(\.\d+)?[eE][+-]?\d+\b'
    complejos = r'\b[-+]?\d+(\.\d+)?[+-]\d+(\.\d+)?[iI]\b'
    fechas = r'\b\d{2}[/|-]\d{2}[/|-]\d{2,4}\b'
    palabrasmate = r'\b(?:Matematico|Matematica|Turing|analisis|Euler|Fermat|Pitagoras|automata|Boole|Cantor|Perelman' \
                   r')\b'
    palabrasfisica = r'\b(?:Experimentacion|Fisico|Fisica|Astronomia|Mecanica|Newton|Einstein|Galileo|Modelo|Tesla' \
                     r'|Dinamica|Particulas)\b'
    file_content = re.sub(fechas, r'<span style="color:orange">\g<0></span>', file_content)
    file_content = re.sub(notacioncientifica, r'<span style="color:purple">\g<0></span>', file_content)
    file_content = re.sub(complejos, r'<span style="color:red">\g<0></span>', file_content)
    file_content = re.sub(reales, r'<span style="color:green">\g<0></span>', file_content)
    file_content = re.sub(enteros, r'<span style="background-color:blue">\g<0></span>', file_content)
    file_content = re.sub(palabrasmate, r'<span style="color:gray">\g<0></span>', file_content)
    file_content = re.sub(palabrasfisica, r'<span style="color:gray">\g<0></span>', file_content)

    return mark_safe(file_content)

@login_required
def edit_file(request, file_id):
    file = archivo.objects.get(pk=file_id)
    if request.method == 'POST':
        file_content = request.POST.get('file_content')
        file_content = analizador(file_content)
        file.file.seek(0)
        file.file.open('w')
        file.file.write(file_content)
        file.file.close()
        file.save()
        return redirect('file_repository')
    else:
        file.file.open('r')
        file_content = file.file.read()
        file.file.close()
        file_content = analizador(file_content)

    return render(request, 'pagina/edit_file.html', {'file':file, 'file_content': file_content})