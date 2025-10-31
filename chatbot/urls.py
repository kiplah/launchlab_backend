from django.urls import path
from .views import chat, get_faqs

urlpatterns = [
    path("chat/", chat, name="chat"),
    path("api/faqs/", get_faqs, name="get_faqs"),
]
