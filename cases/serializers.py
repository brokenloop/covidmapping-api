from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import CoronaCaseRaw


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
    
class CoronaCaseRawSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CoronaCaseRaw
        fields = [
            'case_type',
            'name',
            'description',
            'latitude',
            'longitude',
        ]