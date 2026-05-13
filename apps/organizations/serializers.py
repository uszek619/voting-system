from rest_framework import serializers
from .models import Organization, Cadence, Body

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CadenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cadence
        fields = ['id', 'organization', 'name', 'start_date', 'end_date', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class BodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Body
        fields = ['id', 'organization', 'name', 'description', 'body_type', 'created_at']
        read_only_fields = ['id', 'created_at']