from django.urls import path
from .views import PublicReviewList, SubmitReview

urlpatterns = [
    path('reviews/', PublicReviewList.as_view(), name='review-list'),
    path('reviews/submit/', SubmitReview.as_view(), name='submit-review'),
]
