from .models import *
from rest_framework import serializers

class PerevalAddedSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerevalAdded
        fields = '__all__'
class PerevalUpdateSerializer(serializers.ModelSerializer):
    user = serializers.JSONField(read_only=True)
    user_email = serializers.JSONField(read_only=True)
    class Meta:

        model = PerevalAdded
        fields = '__all__'