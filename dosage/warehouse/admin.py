import csv
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponse
from .models import Storage, ApprovedDrug, User, Product, DrugFormChoice


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)

        for item in queryset:
            row = writer.writerow([getattr(item, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export to CSV file"


@admin.register(DrugFormChoice)
class DrugFormChoiceAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'value', 'description', 'short_extra_info', 'created_at', 'created_by', 'updated_at')
    search_fields = ['value', 'description']
    list_filter = ['value', 'description']
    readonly_fields = ['created_by', 'updated_at', 'extra_info', 'created_at']
    LIST_PER_PAGE = 50
    actions = [ExportCsvMixin.export_as_csv]

    def short_extra_info(self, obj):
        first_row = obj.extra_info.splitlines()[:1]
        return first_row

    short_extra_info.short_description = 'Extra Info'

    fieldsets = (
        (None, {
            'fields': ('value', 'description'),
        }),
        ('Basic Information', {
            'fields': ('extra_info', 'created_by', 'created_at'),
        }),
    )


@admin.action(description='List as staff',)
def make_staff(modeladmin, request, queryset):
    queryset.update(is_staff=True)


@admin.action(description='Remove from staff',)
def unmake_staff(modeladmin, request, queryset):
    queryset.update(is_staff=False)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ['email', 'name', 'surname', 'is_staff', 'is_active', 'display_group']
    list_filter = ['is_staff', 'is_active']
    ordering = ['surname', 'name']
    actions = [make_staff, unmake_staff]
    LIST_PER_PAGE = 50

    fieldsets = (
        (None, {'fields': ('email', 'name', 'surname', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Groups', {'fields': ('groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}),
    )
    search_fields = ('email', 'surname', 'name')

    def save_model(self, request, obj, form, change):
        obj.save()
        obj.groups.set(form.cleaned_data['groups'])


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('rack', 'box', 'short_extra_info', 'created_at', 'created_by', 'updated_at')
    search_fields = ['rack', 'box']
    list_filter = ['rack']
    readonly_fields = ['created_by', 'updated_at', 'extra_info', 'created_at']
    LIST_PER_PAGE = 50
    actions = [ExportCsvMixin.export_as_csv]

    def short_extra_info(self, obj):
        first_row = obj.extra_info.splitlines()[:1]
        return first_row

    short_extra_info.short_description = 'Extra Info'

    fieldsets = (
        (None, {
            'fields': ('rack', 'box'),
        }),
        ('Basic Information', {
            'fields': ('extra_info', 'created_by', 'created_at'),
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
    list_display = ('name', 'main_component_dosage', 'main_component_unit', 'short_components', 'form', 'created_at',
                    'created_by', 'updated_at', 'usage_time', 'usage_time_unit', 'is_approved', 'is_controlled',
                    'short_extra_info')
    search_fields = ['name', 'form', 'created_at']
    list_filter = ['form', 'is_approved', 'usage_time_unit']
    readonly_fields = ['created_by', 'updated_at', 'extra_info', 'created_at']
    actions = [make_approved, make_unapproved, ExportCsvMixin.export_as_csv]
    LIST_PER_PAGE = 50

    def short_components(self, obj):
        first_row = obj.components[:10] + '...'
        return first_row

    short_components.short_description = 'components'

    def short_extra_info(self, obj):
        first_row = obj.extra_info.splitlines()[:1]
        return first_row

    short_extra_info.short_description = 'Extra Info'

    fieldsets = (
        (None, {
            'fields': ('name', 'components', 'main_component_dosage', 'main_component_unit', 'form', 'usage_time', 'usage_time_unit',
                       'label', 'is_approved', 'is_controlled'),
        }),
        ('Basic Information', {
            'fields': ('extra_info', 'created_by', 'created_at'),
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
    list_display = ('approved_drug', 'serial_number', 'storage', 'packaging_quantity', 'packaging_quantity_unit',
                    'best_before_date', 'is_opened', 'ready_to_use', 'created_at', 'created_by', 'updated_at')
    search_fields = ['approved_drug', 'serial_number', 'storage', 'created_by', 'is_opened']
    list_filter = ['is_opened', 'created_by']
    readonly_fields = ['created_by', 'updated_at', 'extra_info', 'created_at']
    actions = [make_opened, make_unopened, ExportCsvMixin.export_as_csv]
    LIST_PER_PAGE = 50

    fieldsets = (
        (None, {
            'fields': ('approved_drug', 'serial_number', 'packaging_quantity', 'packaging_quantity_unit', 'storage',
                       'best_before_date', 'is_opened', 'opened_date'),
        }),
        ('Basic Information', {
            'fields': ('extra_info', 'created_by', 'created_at'),
        }),
    )

    def short_extra_info(self, obj):
        first_row = obj.extra_info.splitlines()[:1]
        return first_row

    short_extra_info.short_description = 'Extra Info'

    @staticmethod
    def ready_to_use(obj):
        return obj.ready_to_use()

    ready_to_use.short_description = 'Ready to Use'
