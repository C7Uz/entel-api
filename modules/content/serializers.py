from rest_framework import serializers
from .models import Home, Page, Country, Teacher, Event, Topic, EventTeacher, SocialNetwork


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'


class SocialNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = '__all__'


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['photo', 'full_name', 'professional_summary', 'country']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'
        
        
class EventTeacherSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    teacher = TeacherSerializer(read_only=True)
    
    class Meta:
        model = EventTeacher
        fields = ['teacher', 'title', 'description', 'topics_title', 'topics']


class EventSerializer(serializers.ModelSerializer):
    event_teacher = EventTeacherSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'slug', 'image', 'title', 'description', 'summary', 'address', 'tag', 'place', 'date', 'event_teacher',]


class EventSimpleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = ['id', 'slug', 'image', 'title', 'description', 'summary', 'address', 'tag', 'place', 'date','flag_endinscriptions']
