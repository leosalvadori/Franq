from rest_framework import serializers
from .models import LogModel
  
class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogModel
        fields = ('typewh','origin','operation', 'created_at', 'payload')

