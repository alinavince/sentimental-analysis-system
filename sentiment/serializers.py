from rest_framework import serializers
from .models import SentimentAnalysis


class SentimentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model  = SentimentAnalysis
        fields = [
            'id',
            'text',
            'sentiment',
            'confidence',
            'positive_score',
            'negative_score',
            'neutral_score',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class PredictRequestSerializer(serializers.Serializer):
    text = serializers.CharField(
        min_length=3,
        max_length=5000,
        error_messages={
            'blank':      'Text cannot be empty.',
            'min_length': 'Text must be at least 3 characters.',
            'max_length': 'Text cannot exceed 5000 characters.',
        }
    )
