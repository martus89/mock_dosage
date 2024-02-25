from django.contrib import admin
from .models import Storage, ApprovedDrug, Product


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('rack', 'box', 'extra_info')
    search_fields = ['rack', 'box']
    list_filter = ['rack']


@admin.register(ApprovedDrug)
class ApprovedDrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'components', 'form', 'created_at', 'usage_time', 'usage_time_unit',
                    'is_approved')
    search_fields = ['name', 'form', 'created_at']
    list_filter = ['form', 'is_approved', 'usage_time_unit']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('approved_drug', 'serial_number', 'storage', 'quantity', 'quantity_unit', 'created_by',
                    'best_before_date', 'is_opened', 'ready_to_use')
    search_fields = ['approved_drug', 'serial_number', 'storage', 'created_by', 'is_opened']
    list_filter = ['is_opened', 'created_by']

    def ready_to_use(self, obj):
        return obj.ready_to_use()
