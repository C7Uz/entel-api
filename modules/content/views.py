from rest_framework import viewsets
from django.utils import timezone

from .models import Home, Event, Page, SocialNetwork
from .serializers import HomeSerializer, EventSerializer, EventSimpleSerializer, PageSerializer, SocialNetworkSerializer


class HomeViewSet(viewsets.ModelViewSet):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    authentication_classes = []
    permission_classes = []
    pagination_class = None
    http_method_names = ['get']
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Models
        home = Home.objects.first()
        event = Event.objects.filter(date__gte=timezone.now()).order_by('the_order')[:3]
        
        # Serializers
        serializer_home = HomeSerializer(home, many=False, context={'request': request})
        serializer_event = EventSimpleSerializer(event, many=True, context={'request': request})
        
        response.data = {
            'success': True,
            'message': 'Data retrieved successfully',
            'data': {
                'header': serializer_home.data,
                'events': serializer_event.data
            }
        }
        return response


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = []
    permission_classes = []
    pagination_class = None
    http_method_names = ['get']
    lookup_field = 'slug'
    
    def get_serializer_context(self):
        context = super(EventViewSet, self).get_serializer_context()
        context.update({
            'request': self.request
        })
        return context


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    authentication_classes = []
    permission_classes = []
    pagination_class = None
    http_method_names = ['get']
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Models
        page = Page.objects.first()
        social = SocialNetwork.objects.all()
        
        # Serializers
        serializer_page = PageSerializer(page, many=False, context={'request': request})
        serializer_social = SocialNetworkSerializer(social, many=True, context={'request': request})
        
        response.data = {
            'success': True,
            'message': 'Data retrieved successfully',
            'data': {
                'page': serializer_page.data,
                'social': serializer_social.data
            }
        }
        return response