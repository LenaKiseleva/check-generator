from django.contrib import admin

from .models import Check, Printer


class PrinterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'api_key', 'check_type', 'point_id', )
    search_fields = ('id', 'name', 'api_key', 'check_type', 'point_id', )
    list_filter = ('id', 'name', 'api_key', 'check_type', 'point_id', )
    empty_value_display = '-не указано-'


admin.site.register(Printer, PrinterAdmin)


class CheckAdmin(admin.ModelAdmin):
    list_display = ('printer_id', 'defined_type',
                    'order', 'status', 'pdf_file')
    list_filter = ('printer_id', 'defined_type', 'status', )
    search_fields = ('printer_id', 'defined_type', 'status', )
    empty_value_display = '-не указано-'


admin.site.register(Check, CheckAdmin)
