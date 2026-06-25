from django.contrib import admin
from .models import SentimentAnalysis, AnalyticsSummary


@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display  = ('id', 'sentiment', 'confidence', 'text_preview', 'created_at')
    list_filter   = ('sentiment', 'created_at')
    search_fields = ('text',)
    readonly_fields = ('created_at',)

    def text_preview(self, obj):
        return obj.text[:80] + '...' if len(obj.text) > 80 else obj.text
    text_preview.short_description = 'Text Preview'


@admin.register(AnalyticsSummary)
class AnalyticsSummaryAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_analyses', 'positive_count', 'negative_count', 'neutral_count')
    ordering     = ('-date',)
