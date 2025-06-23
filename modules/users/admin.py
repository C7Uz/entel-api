from typing import Optional
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# Import / Export
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from import_export import fields

# Models
from .models import User, Inscriptions


# Resource
class InscriptionResource(ModelResource):
    event = fields.Field(attribute='event__title', column_name="Evento")
    
    class Meta:
        model = Inscriptions
        fields = ['event', 'fullname', 'cellphone', 'job', 'flag_business', 'company', 'ruc', 'email','publicidad', 'created']

 

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class CustomUserChangeForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Nueva contraseña"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Dejar en blanco para no cambiar la contraseña.")
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)  # Aquí se encripta
        if commit:
            user.save()
            self.save_m2m()
        return user


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('id', 'first_name', 'last_name', 'email')
    ordering = ['first_name']
    list_per_page = 50
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (_('Información Personal'), {'fields': ('first_name', 'last_name', 'email', 'password')}),
        (_('Permisos'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Inscriptions)
class InscriptionsAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('id', 'event', 'fullname','publicidad', 'created')
    list_filter = ('event__title', 'created', 'flag_business', 'response_infobip')
    search_fields = ('event__title', 'fullname', 'email', 'job', 'ruc')
    list_per_page = 50
    import_form_class = ImportForm
    export_form_class = ExportForm
    resource_class = InscriptionResource

    def has_import_permission(self, request):
        return False
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return True
    
