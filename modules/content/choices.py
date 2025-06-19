from django.db.models import TextChoices


class TargetChoices(TextChoices):
    BLANK = '_blank', '_blank'
    SELF = 'self', 'self'


class SocialNetworkChoices(TextChoices):
    FB = 'Facebook', 'Facebook'
    IG = 'Instagram', 'Instagram'
    YT = 'Youtube', 'Youtube'
    TW = 'Twitter', 'Twitter'
    IN = 'LinkedIn', 'LinkedIn'

