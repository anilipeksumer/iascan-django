from django.contrib import admin
from .models import PortScanner
# Register your models here.
@admin.register(PortScanner) #decorator : bunu admin panelini özelleştirip, search ar vs eklemek için yaptık.
class PortScannerAdmin(admin.ModelAdmin):
    list_display = ["domainName", "ipField","scan_date"]
    list_display_links = ["domainName", "ipField"] #link ekleme (içeriğe giden.)
    search_fields = ["ipField", "domainName"] #search bar ekle.
    list_filter = ["scan_date","domainName"]
    class Meta: #decorator ve classı birbirine bağladığımız nokta.
        model = PortScanner
