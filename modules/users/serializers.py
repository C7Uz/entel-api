from rest_framework import serializers
from .models import Inscriptions


class InscriptionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Inscriptions
        fields = ['event', 'fullname', 'cellphone', 'job', 'flag_business', 'company', 'ruc', 'email','publicidad', 'response_infobip']
        extra_kwargs = {'company': {'required': False}, 'ruc': {'required': False}}
