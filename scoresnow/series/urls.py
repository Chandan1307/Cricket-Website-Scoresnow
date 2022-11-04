from django.contrib import admin
from django.urls import path, include
from scoresnow.series.views import MatchViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'Match1', MatchViewSet, basename='Matches')



urlpatterns = [
    path('',include(router.urls))
]