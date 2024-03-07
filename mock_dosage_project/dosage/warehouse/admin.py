import csv
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponse
from .models import Storage, ApprovedDrug, Product, User


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export to CSV file"


@admin.action(description='List as staff',)
def make_staff(modeladmin, request, queryset):
    queryset.update(is_staff=True)


@admin.action(description='Remove from staff',)
def unmake_staff(modeladmin, request, queryset):
    queryset.update(is_staff=False)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ['email', 'name', 'surname', 'is_staff', 'is_active', 'permissions_granted']
    list_filter = ['is_staff', 'is_active']
    ordering = ['surname', 'name']
    actions = [make_staff, unmake_staff]
    LIST_PER_PAGE = 50

    fieldsets = (
        (None, {'fields': ('email', 'name', 'surname', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}),
    )
    search_fields = ('email', 'surname', 'name')

    @staticmethod
    def permissions_granted(obj):
        return ", ".join([group.name for group in obj.groups.all()])


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('rack', 'box', 'extra_info', 'created_at', 'created_by', 'updated_at')
    search_fields = ['rack', 'box']
    list_filter = ['rack']
    LIST_PER_PAGE = 50
    actions = [ExportCsvMixin.export_as_csv]

    fieldsets = (
        (None, {
            'fields': ('rack', 'box'),
        }),
        ('Basic Information', {
            'fields': ('extra_info', 'created_by'),
        }),
    )


@admin.action(description='Change to approved',)
def make_approved(modeladmin, request, queryset):
    queryset.update(is_approved=True)


@admin.action(description='Change to unapproved',)
def make_unapproved(modeladmin, request, queryset):
    queryset.update(is_approved=False)


@admin.register(ApprovedDrug)
class ApprovedDrugAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'components', 'form', 'created_at', 'created_by', 'updated_at', 'usage_time',
                    'usage_time_unit', 'is_approved', 'extra_info')
    search_fields = ['name', 'form', 'created_at']
    list_filter = ['form', 'is_approved', 'usage_time_unit']
    actions = [make_approved, make_unapproved, ExportCsvMixin.export_as_csv]
    LIST_PER_PAGE = 50

    fieldsets = (
        (None, {
            'fields': ('name', 'components', 'main_component_dosage', 'form', 'usage_time', 'usage_time_unit',
                       'label', 'is_approved'),
        }),
        ('Basic Information', {
            'fields': ('extra_info', 'created_by'),
        }),
    )


@admin.action(description='List as opened',)
def make_opened(modeladmin, request, queryset):
    queryset.update(is_opened=True)


@admin.action(description='List as unopened',)
def make_unopened(modeladmin, request, queryset):
    queryset.update(is_opened=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('approved_drug', 'serial_number', 'storage', 'quantity', 'quantity_unit',
                    'best_before_date', 'is_opened', 'ready_to_use', 'created_at', 'created_by', 'updated_at')
    search_fields = ['approved_drug', 'serial_number', 'storage', 'created_by', 'is_opened']
    list_filter = ['is_opened', 'created_by']
    actions = [make_opened, make_unopened, ExportCsvMixin.export_as_csv]
    LIST_PER_PAGE = 50

    fieldsets = (
        (None, {
            'fields': ('approved_drug', 'serial_number', 'quantity', 'quantity_unit', 'storage', 'best_before_date',
                       'is_opened', 'opened_date'),
        }),
        ('Basic Information', {
            'fields': ('extra_info', 'created_by'),
        }),
    )

    @staticmethod
    def ready_to_use(obj):
        return obj.ready_to_use()
