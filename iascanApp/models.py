from email.policy import default
from tabnanny import verbose
from django.db import models
from django import forms
# Create your models here.

class PortScanner(models.Model):
    domainName = models.CharField(max_length = 256, verbose_name = "Domain Address (ex: google.com)")
    startPort = models.CharField(max_length = 5, verbose_name="Start Port (0-65565)")
    endPort = models.CharField(max_length = 5, verbose_name="End Port")
    
    velocityChoices =(
        ("T1", "T1"),
        ("T2", "T2"),
        ("T3", "T3"),
        ("T4", "T4"),
        ("T5", "T5"),
        
    )
    # velocityField = forms.ChoiceField(choices = velocityChoices)
    velocityField = models.CharField(max_length=2,
                                       choices = velocityChoices,
                                       default = "T5",
                                       verbose_name="Port Scan Time (T5 Fastest, T1 Slowest)")
    ipField = models.GenericIPAddressField(verbose_name = "IP Address", default = "8.8.8.8")
    scan_date = models.DateTimeField(auto_now_add = True, verbose_name = "Scan Date")
    ports = models.TextField()
    banners = models.TextField()
    

    
class DirBuster(models.Model):
    domainName = models.CharField(max_length = 256, verbose_name = "Domain Address (ex: google.com)")
    sslChoice =(
    ("SSL Disabled", "SSL Disabled"),
    ("SSL Enabled", "SSL Enabled"))
    sslField = models.CharField(max_length=14,
                                       choices = sslChoice,
                                       default = "SSL Enabled",
                                       verbose_name="SSL Certificate")
    

        
    def __str__(self):
        return "IP:" + self.ipField  + " (" + self.domainName + ")"
    
    