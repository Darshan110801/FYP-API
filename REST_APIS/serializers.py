from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
  class Meta:
    model= Message
    fields = ['id', 'sentence','sentence_type']
    extra_kwargs = {"sentence_type": {"required": False, "allow_null": True}}