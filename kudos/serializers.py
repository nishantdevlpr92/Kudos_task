from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Kudos, Organization


User = get_user_model()

class KudosSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    receiver = serializers.StringRelatedField()

    class Meta:
        model = Kudos
        fields = ['sender', 'receiver', 'message', 'created_at']

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']  # or any other fields you want to include

class UserSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()  # Use the OrganizationSerializer for the 'organization' field

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'organization', 'remaining_kudos']