
from django.urls import path
from livescore.views import LiveScorePageView

urlpatterns = [
    path('', LiveScorePageView.as_view()),
]
