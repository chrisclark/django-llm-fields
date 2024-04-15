from rest_framework import serializers

from .models import GPTPrompt


class GPTPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPTPrompt
        fields = "__all__"
