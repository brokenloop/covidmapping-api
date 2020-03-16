from rest_framework import serializers
from .models import CoronaCaseRaw


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