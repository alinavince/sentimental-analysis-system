from django.db.models import Count
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import SentimentAnalysis
from .serializers import SentimentAnalysisSerializer, PredictRequestSerializer
from .ml_model import predict_sentiment


# ─────────────────────────────────────────────────────────────────────────────
# POST /api/predict/   →  analyse a single text and save to DB
# ─────────────────────────────────────────────────────────────────────────────
class PredictSentimentView(APIView):
    def post(self, request):
        req_ser = PredictRequestSerializer(data=request.data)
        if not req_ser.is_valid():
            return Response(
                {'error': req_ser.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        text = req_ser.validated_data['text']

        try:
            result = predict_sentiment(text)
        except FileNotFoundError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {'error': f'Prediction failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Save to MySQL
        analysis = SentimentAnalysis.objects.create(
            text           = text,
            sentiment      = result['sentiment'],
            confidence     = result['confidence'],
            positive_score = result['positive_score'],
            negative_score = result['negative_score'],
            neutral_score  = result['neutral_score'],
        )

        serializer = SentimentAnalysisSerializer(analysis)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/history/   →  paginated list of past analyses
# ─────────────────────────────────────────────────────────────────────────────
class AnalysisHistoryView(APIView):
    def get(self, request):
        queryset = SentimentAnalysis.objects.all()

        # Optional filter by sentiment
        sentiment_filter = request.query_params.get('sentiment')
        if sentiment_filter in ('positive', 'negative', 'neutral'):
            queryset = queryset.filter(sentiment=sentiment_filter)

        # Simple pagination
        try:
            page  = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', 10))
        except ValueError:
            page, limit = 1, 10

        page  = max(1, page)
        limit = max(1, min(50, limit))

        start = (page - 1) * limit
        end   = start + limit

        total    = queryset.count()
        records  = queryset[start:end]
        ser      = SentimentAnalysisSerializer(records, many=True)

        return Response({
            'total':   total,
            'page':    page,
            'limit':   limit,
            'pages':   (total + limit - 1) // limit,
            'results': ser.data,
        })


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/stats/   →  dashboard statistics
# ─────────────────────────────────────────────────────────────────────────────
class StatisticsView(APIView):
    def get(self, request):
        total = SentimentAnalysis.objects.count()

        counts = (
            SentimentAnalysis.objects
            .values('sentiment')
            .annotate(count=Count('id'))
        )
        count_map = {item['sentiment']: item['count'] for item in counts}

        positive = count_map.get('positive', 0)
        negative = count_map.get('negative', 0)
        neutral  = count_map.get('neutral',  0)

        def pct(n):
            return round((n / total * 100), 1) if total else 0

        # Recent 5 records
        recent = SentimentAnalysisSerializer(
            SentimentAnalysis.objects.all()[:5], many=True
        ).data

        return Response({
            'total':              total,
            'positive_count':     positive,
            'negative_count':     negative,
            'neutral_count':      neutral,
            'positive_percent':   pct(positive),
            'negative_percent':   pct(negative),
            'neutral_percent':    pct(neutral),
            'recent_analyses':    recent,
        })


# ─────────────────────────────────────────────────────────────────────────────
# DELETE /api/history/<id>/   →  delete a single record
# ─────────────────────────────────────────────────────────────────────────────
class DeleteAnalysisView(APIView):
    def delete(self, request, pk):
        try:
            record = SentimentAnalysis.objects.get(pk=pk)
            record.delete()
            return Response({'message': 'Record deleted successfully.'})
        except SentimentAnalysis.DoesNotExist:
            return Response(
                {'error': 'Record not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/health/   →  quick health check
# ─────────────────────────────────────────────────────────────────────────────
class HealthCheckView(APIView):
    def get(self, request):
        from pathlib import Path
        from django.conf import settings
        model_exists = (
            Path(settings.ML_MODEL_PATH / 'sentiment_model.pkl').exists()
        )
        return Response({
            'status':       'ok',
            'model_loaded': model_exists,
            'server_time':  timezone.now().isoformat(),
        })
