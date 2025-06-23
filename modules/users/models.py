from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager as BaseUserManager
from django.contrib.auth.hashers import make_password
from .choices import DocumentTypeChoices, SexoChoices
from datetime import datetime
from modules.content.models import Event

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('Email'), max_length=250, unique=True, null=True, default=None, blank=False, db_index=True)
    
    first_name = models.CharField(verbose_name=_('Nombres'), blank=False, null=False, max_length=150)
    last_name = models.CharField(verbose_name=_('Apellidos'), blank=False, null=True, max_length=150)
    
    is_staff = models.BooleanField(verbose_name=_('Staff'), default=True)
    is_active = models.BooleanField(verbose_name=_('¿Activo?'), default=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now_add=False, default=datetime.now(), null=True, verbose_name="Última de modificación")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    objects = UserManager()

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name or '', self.last_name or '')

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class Inscriptions(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Evento')
    fullname = models.CharField(max_length=100, verbose_name='Nombre')
    cellphone = models.CharField(max_length=100, verbose_name='Celular')
    job = models.CharField(max_length=100, verbose_name='Puesto', null=True, blank=True)
    flag_business = models.BooleanField(default=False, verbose_name='Empresa', null=True, blank=True)
    company = models.CharField(max_length=100, verbose_name='Empresa', null=True, blank=True)
    ruc = models.CharField(max_length=100, verbose_name='RUC', null=True, blank=True)
    email = models.EmailField(verbose_name='Email')
    response_infobip = models.TextField(null=True, blank=True, default=None, verbose_name='Respuesta Infobip')
    publicidad = models.BooleanField(null=True, blank=True, default=None, verbose_name='Acepto el envío de publicidad')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")


    class Meta:
        verbose_name = "Inscripciones"
        verbose_name_plural = "Inscripciones"

    def __str__(self):
        return self.fullname

