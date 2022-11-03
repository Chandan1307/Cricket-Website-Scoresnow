from django.contrib import admin
from django.urls import path, include
from scoresnow.blog.views import BlogPageViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'blogi', BlogPageViewSet, basename='blogs')



urlpatterns = [
    path('',include(router.urls))
]
