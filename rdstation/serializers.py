from rest_framework import serializers
from .models import AuthModel
  
class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthModel
        fields = ('access_token', 'expires_in', 'refresh_token')

class AuthUpdateTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthModel
        fields = ['id']
        read_only_fields = ['access_token','expires_in','refresh_token','updated']

class TokenRequestSerializer(serializers.Serializer):
    client_id = serializers.CharField(max_length=200)
    client_secret = serializers.CharField(max_length=200)
    refresh_token = serializers.CharField(max_length=200)

class EmailSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=200)
    primary = serializers.CharField(max_length=10)

class PhoneSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=200)
    primary = serializers.CharField(max_length=10)

class RdStationPersonSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = EmailSerializer(many=True)
    phone = PhoneSerializer(many=True)
