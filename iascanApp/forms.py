from dataclasses import field, fields
from pyexpat import model
from django import forms
from .models import PortScanner,DirBuster
class ScannerForm(forms.ModelForm):
    class Meta: #Django Formları oluşturmak için default verilen class adı.
        model = PortScanner
        fields = ["domainName", "startPort","endPort","velocityField"]
        
class DirForm(forms.ModelForm):
    class Meta:
        model = DirBuster
        fields = ["domainName", "sslField"]
   
    