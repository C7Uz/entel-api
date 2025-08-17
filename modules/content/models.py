from django.db import models
from .choices import SocialNetworkChoices, TargetChoices
from django.utils.text import slugify
from adminsortable.models import SortableMixin


class Home(models.Model):
    logo = models.ImageField(upload_to='home')
    background_desktop = models.ImageField(upload_to='home')
    background_mobile = models.ImageField(upload_to='home')
    title = models.CharField(max_length=100, verbose_name='Título')
    subtitle = models.CharField(max_length=100, verbose_name='Subtítulo')
    description = models.TextField(verbose_name='Descripción')
    btn_title = models.CharField(max_length=100, verbose_name='Boton')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Home'
        verbose_name_plural = 'Home'


class SocialNetwork(models.Model):
    target = models.CharField(verbose_name="Destino", default=TargetChoices.SELF, max_length=30,
                              choices=TargetChoices.choices)
    icon = models.ImageField(upload_to='social_networks', verbose_name="Icono", null=True, blank=True)
    icon_hover = models.ImageField(upload_to='social_networks', verbose_name="Icono (hover)", null=True, blank=True)
    network = models.CharField(verbose_name="Red social", default=SocialNetworkChoices.FB, max_length=30,
                               choices=SocialNetworkChoices.choices)
    url = models.URLField(max_length=140, null=True, unique=True, blank=False, verbose_name="URL")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return self.network

    class Meta:
        verbose_name = "Red social"
        verbose_name_plural = "Redes sociales"


class Page(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título')
    subtitle = models.CharField(max_length=100, verbose_name='Subtítulo')
    background = models.ImageField(upload_to='page')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", null=True, blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Página"
        verbose_name_plural = "Páginas"


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    flag = models.ImageField(upload_to='country')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'


class Temas(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    flag = models.ImageField(upload_to='tema')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'


class Teacher(models.Model):
    photo = models.ImageField(upload_to='teacher')
    full_name = models.CharField(max_length=100, verbose_name='Nombre')
    professional_summary = models.TextField(verbose_name='Resumen')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = 'Conferencista'
        verbose_name_plural = 'Conferencistas'


class Event(SortableMixin):
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL', null=True, blank=True)
    image = models.ImageField(upload_to='event')
    logo_event = models.ImageField(upload_to='logo_event', null=True, blank=True)
    title = models.CharField(max_length=100, verbose_name='Título')
    summary = models.TextField(verbose_name='Resumen', null=True, blank=True)
    description = models.TextField(verbose_name='Descripción')
    tag = models.CharField(max_length=100, verbose_name='Etiqueta', null=True, blank=True)
    place = models.CharField(max_length=100, verbose_name='Lugar')
    address = models.CharField(max_length=100, verbose_name='Dirección', null=True, blank=True)
    date = models.DateTimeField(verbose_name='Fecha')
    infobip_code = models.CharField(max_length=100, verbose_name='Código Infobip', null=True, blank=True, default=None)
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    
    flag_endinscriptions = models.BooleanField(default=False, verbose_name='Inscripciones Abiertas', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Event.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['the_order']


class Topic(models.Model):
    icon = models.ImageField(upload_to='topic')
    text = models.CharField(max_length=100, verbose_name='Título')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", null=True, blank=True)
    
    def __str__(self):
        return "{0}...".format(self.text[:30])


class EventTeacher(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título', null=True, blank=False)
    description = models.TextField(verbose_name='Descripción', null=True, blank=False)
    topics_title = models.CharField(max_length=100, verbose_name='Título topicos', null=True, blank=False)
    topics = models.ManyToManyField(Topic, verbose_name='topicos', null=True, blank=True)
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_teacher', verbose_name='Evento')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_event', verbose_name='Conferencista')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event.title


