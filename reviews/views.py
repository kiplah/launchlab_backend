from rest_framework import generics, status
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer

# 🟢 Public endpoint — Only show approved reviews
class PublicReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # Only show approved reviews, newest first
        return Review.objects.filter(is_approved=True).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


# 🟡 Endpoint to submit a new review (pending admin approval)
class SubmitReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        # Provide request for absolute image URLs
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_approved=False)  # Automatically mark as unapproved
        return Response(
            {"message": "Review submitted successfully. Pending admin approval."},
            status=status.HTTP_201_CREATED,
        )
