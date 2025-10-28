from rest_framework import generics
from .models import Review
from .serializers import ReviewSerializer

# Public endpoint (only approved reviews)
class PublicReviewList(generics.ListAPIView):
    queryset = Review.objects.filter(is_approved=True).order_by('-created_at')
    serializer_class = ReviewSerializer

# Endpoint to submit a review
class SubmitReview(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
