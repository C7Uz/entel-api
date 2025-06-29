from import_export import resources
from .models import Reference, User
from import_export import fields



class UserExportResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name="ID")
    type = fields.Field(attribute='type', column_name="Tipo")
    username = fields.Field(attribute='username', column_name="Nickname")
    first_name = fields.Field(attribute='first_name', column_name="Nombres")
    last_name = fields.Field(attribute='last_name', column_name="Apellidos")
    cellphone = fields.Field(attribute='cellphone', column_name="Celular")
    gender = fields.Field(attribute='gender', column_name="Genero")
    document_type = fields.Field(attribute='document_type', column_name="Tipo documento")
    document_number = fields.Field(attribute='document_number', column_name="N. documento")
    onboarding = fields.Field(attribute='onboarding', column_name="Onboarding")
    created = fields.Field(attribute='created', column_name="Fech. Creación")
    last_login = fields.Field(attribute='last_login', column_name="Última sesión")
    email_activated = fields.Field(attribute='email_activated', column_name="Email activado")
    is_staff = fields.Field(attribute='is_staff', column_name="Staff")
    is_active = fields.Field(attribute='is_active', column_name="Activo")

    class Meta:
        model = User
        fields = ('id', 'type', 'username', 'email', 'first_name', 'last_name', 'cellphone', 'gender',
                  'document_type', 'document_number', 'onboarding', 'created', 'last_login', 'email_activated', 'is_staff', 'is_active')

