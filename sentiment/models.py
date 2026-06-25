from django.db import models


class SentimentAnalysis(models.Model):
    """
    Stores every text submitted for sentiment analysis.
    """
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral',  'Neutral'),
    ]

    text        = models.TextField(verbose_name="Input Text")
    sentiment   = models.CharField(
                    max_length=10,
                    choices=SENTIMENT_CHOICES,
                    verbose_name="Predicted Sentiment"
                  )
    confidence  = models.FloatField(verbose_name="Confidence Score (%)")
    # Probabilities for each class (stored as percentage)
    positive_score = models.FloatField(default=0.0)
    negative_score = models.FloatField(default=0.0)
    neutral_score  = models.FloatField(default=0.0)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table  = 'sentiment_results'
        ordering  = ['-created_at']
        verbose_name        = 'Sentiment Analysis'
        verbose_name_plural = 'Sentiment Analyses'

    def __str__(self):
        return f"[{self.sentiment.upper()}] {self.text[:60]}..."


class AnalyticsSummary(models.Model):
    """
    Tracks daily summary counts for the dashboard.
    Auto-updated via signals or periodic tasks.
    """
    date            = models.DateField(unique=True)
    total_analyses  = models.IntegerField(default=0)
    positive_count  = models.IntegerField(default=0)
    negative_count  = models.IntegerField(default=0)
    neutral_count   = models.IntegerField(default=0)

    class Meta:
        db_table = 'analytics_summary'
        ordering = ['-date']

    def __str__(self):
        return f"Summary for {self.date}"
