from .models import *
from rest_framework import serializers

class PerevalAddedSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerevalAdded
        fields = '__all__'