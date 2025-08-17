from django.contrib import admin
from unfold.admin import ModelAdmin
from adminsortable2.admin import SortableAdminMixin

from .models import Home, SocialNetwork, Page, Country, Teacher, Event, Topic, EventTeacher


# Clase base para mantener consistencia en Unfold
class BaseUnfoldAdmin(ModelAdmin):
    """Clase base para garantizar estilos consistentes con Django Unfold"""
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Garantiza widgets consistentes en Django Unfold"""
        
        # Campos de imagen - usar el widget de Unfold
        if db_field.get_internal_type() == 'ImageField':
            # Unfold maneja automáticamente los campos de imagen
            pass
            
        # Campos de texto largo
        elif db_field.get_internal_type() == 'TextField':
            from django import forms
            kwargs['widget'] = forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full'
            })
            
        # Campos URL
        elif db_field.get_internal_type() == 'URLField':
            from django import forms
            kwargs['widget'] = forms.URLInput(attrs={
                'class': 'w-full'
            })
            
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Home)
class HomeAdmin(BaseUnfoldAdmin):
    list_filter = ('created_at',)
    list_display = ('title', 'subtitle', 'created_at')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Imágenes', {
            'fields': ('logo', 'background_desktop', 'background_mobile'),
            'classes': ('wide',)
        }),
        ('Contenido Principal', {
            'fields': ('title', 'subtitle', 'description', 'btn_title'),
            'classes': ('wide',)
        }),
        ('Información del Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SocialNetwork)
class SocialNetworkAdmin(BaseUnfoldAdmin):
    list_filter = ('network', 'target', 'created_at')
    list_display = ('network', 'url', 'target', 'created_at')
    search_fields = ('url', 'network')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Configuración de Red Social', {
            'fields': ('network', 'target', 'url'),
            'classes': ('wide',)
        }),
        ('Iconos', {
            'fields': ('icon', 'icon_hover'),
            'classes': ('wide',)
        }),
        ('Información del Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Page)
class PageAdmin(BaseUnfoldAdmin):
    list_filter = ('created_at',)
    list_display = ('title', 'subtitle', 'created_at')
    search_fields = ('title', 'subtitle')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Contenido de la Página', {
            'fields': ('title', 'subtitle', 'background'),
            'classes': ('wide',)
        }),
        ('Información del Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Country)
class CountryAdmin(BaseUnfoldAdmin):
    list_filter = ('created_at',)
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Información del País', {
            'fields': ('name', 'flag'),
            'classes': ('wide',)
        }),
        ('Información del Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Teacher)
class TeacherAdmin(BaseUnfoldAdmin):
    list_filter = ('country', 'created_at')
    list_display = ('full_name', 'country', 'created_at')
    search_fields = ('full_name',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Información del Conferencista', {
            'fields': ('photo', 'full_name', 'professional_summary', 'country'),
            'classes': ('wide',)
        }),
        ('Información del Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Topic)
class TopicAdmin(BaseUnfoldAdmin):
    list_filter = ('created_at',)
    list_display = ('text', 'created_at')
    search_fields = ('text',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Información del Tópico', {
            'fields': ('text', 'icon'),
            'classes': ('wide',)
        }),
        ('Información del Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


# Inline para EventTeacher con Unfold
class EventTeacherInline(admin.TabularInline):
    model = EventTeacher
    extra = 0
    verbose_name = 'Conferencia'
    verbose_name_plural = 'Conferencias'
    
    # Usar filter_horizontal para ManyToMany en Unfold
    filter_horizontal = ('topics',)
    
    fields = ('teacher', 'title', 'description', 'topics_title', 'topics')
    
    # Configuración específica para Unfold
    classes = ('wide',)


# Remove the first duplicate registration and fix the second one
@admin.register(Event)
class EventAdmin(BaseUnfoldAdmin, SortableAdminMixin):
    list_filter = ('date', 'place', 'tag', 'created_at')
    list_display = ('title', 'place', 'date', 'tag', 'created_at')
    search_fields = ('title', 'place', 'description')
    readonly_fields = ('created_at',)  # Removed 'slug' from readonly_fields
    # prepopulated_fields = {'slug': ('title',)}  # Commented out since slug doesn't exist
    inlines = (EventTeacherInline,)
    
    # Exclude the_order from the form
    exclude = ('the_order',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'tag'),  # Removed 'slug' from fields
            'classes': ('wide',)
        }),
        ('Contenido', {
            'fields': ('summary', 'description'),
            'classes': ('wide',)
        }),
        ('Imágenes', {
            'fields': ('image', 'logo_event'),
            'classes': ('wide',)
        }),
        ('Ubicación y Fecha', {
            'fields': ('place', 'address', 'date'),
            'classes': ('wide',)
        }),
        ('Cerrar Inscripciones', {
            'fields': ('flag_endinscriptions',),  # Removed 'the_order' from here
            'classes': ('collapse',)
        }),
        ('Configuración Avanzada', {
            'fields': ('infobip_code',),  # Removed 'the_order' from here
            'classes': ('collapse',)
        }),
        ('Información del Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
# Registro opcional de EventTeacher como modelo independiente
@admin.register(EventTeacher)
class EventTeacherAdmin(BaseUnfoldAdmin):
    list_display = ('event', 'teacher', 'title', 'created_at')
    list_filter = ('event', 'teacher', 'created_at')
    search_fields = ('title', 'description', 'event__title', 'teacher__full_name')
    readonly_fields = ('created_at',)
    filter_horizontal = ('topics',)
    
    fieldsets = (
        ('Relaciones', {
            'fields': ('event', 'teacher'),
            'classes': ('wide',)
        }),
        ('Contenido de la Presentación', {
            'fields': ('title', 'description', 'topics_title'),
            'classes': ('wide',)
        }),
        ('Tópicos', {
            'fields': ('topics',),
            'classes': ('wide',)
        }),
        ('Información del Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )