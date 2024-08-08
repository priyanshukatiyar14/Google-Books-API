from rest_framework import serializers
from .models import BookRecommendation, UserInteraction

class BookRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRecommendation
        fields = '__all__'

class UserInteractionSerializer(serializers.Serializer):
    class Meta:
        model = UserInteraction
        fields = '__all__'

    def create(self, validated_data):
        return UserInteraction.objects.create(**validated_data)