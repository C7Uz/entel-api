from django.shortcuts import render
from rest_framework import status, viewsets


# Create your views here.
from rest_framework.response import Response
from .serializers import InscriptionsSerializer
from .models import Inscriptions

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import datetime
from django.utils import timezone
import requests


class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Inscriptions.objects.all()
    serializer_class = InscriptionsSerializer
    authentication_classes = []
    permission_classes = []
    pagination_class = None
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        event = serializer.instance.event
        
        # Send infobip
        infobip_response = self.send_infobip(request, event)
        serializer.instance.response_infobip = str(infobip_response)
        serializer.instance.save()
        
        # Send emails
        """
        subject = 'Entel Empresas ✨💪 Tu registro fue exitoso'
        html_content = render_to_string('emails/event_register.html', {
            
            'event': event, 
            'date': self._formatear_fecha(event.date),
            'hour': event.date.astimezone(timezone.get_default_timezone()).strftime("%I:%M %p"),
            'fullname': request.data['fullname']
        })
        msg = EmailMultiAlternatives(subject, html_content, settings.DEFAULT_FROM_EMAIL, [request.data['email']])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        """
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def _formatear_fecha(self, fecha):
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        mes = meses[fecha.month - 1]
        fecha_formateada = fecha.strftime(f"%d de {mes}")
        return fecha_formateada

    def send_infobip(self, request, event):
        try:
            fullname = request.data['fullname']
            words = fullname.split()
            num_words = len(words)
            firstName = "-"
            lastName = "-"

            if num_words == 1:
                firstName = words[0]
                lastName = "-"
                
            elif num_words == 2:
                firstName = words[0]
                lastName = words[1]
                
            elif num_words >= 3:
                firstName = " ".join(words[:-2])
                lastName = " ".join(words[-2:])
            
            infobip_data = {
                "participants": [
                    {
                        "identifyBy": {
                            "identifier": request.data['email'],
                            "type": "EMAIL"
                        },
                        "person": {
                            "firstName": firstName,
                            "lastName": lastName,
                            "customAttributes": {
                                "Job": request.data['job'],
                                "flag_business": bool(request.data['flag_business']),
                                "Compañia": request.data['company'] or "-",
                                "RUC": request.data['ruc'] or "-"
                            },
                            "contactInformation": {
                                "email": [{"address": request.data['email']}],
                                "phone": [{"number": "51" + request.data['cellphone']}]
                            }
                        }
                    },
                    {
                        "identifyBy": {
                            "identifier": "51" + request.data['cellphone'],
                            "type": "PHONE"
                        },
                        "person": {
                            "firstName": firstName,
                            "lastName": lastName,
                            "customAttributes": {
                                "Job": request.data['job'],
                                "flag_business": bool(request.data['flag_business']),
                                "Compañia": request.data['company'] or "-",
                                "RUC": request.data['ruc'] or "-"
                            },
                            "contactInformation": {
                                "email": [{"address": request.data['email']}]
                            }
                        }
                    }
                ]
            }

            headers = {
                'Authorization': 'App 0f60d969390639fb191a98f125cc2d82-faa3f75e-5b4c-4846-9fbb-9ed68b59961e',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            infobip_url = f"https://4myg16.api.infobip.com/moments/1/flows/{event.infobip_code}/participants?phone=51{request.data['cellphone']}"
            response = requests.post(infobip_url, json=infobip_data, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Error en la solicitud: Código de estado {response.status_code}", "details": response.text}
        except ValueError as e:
            return {"error": "Error al decodificar JSON", "details": str(e)}