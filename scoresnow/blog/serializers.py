from rest_framework import serializers
from scoresnow.blog.models import BlogPage



#create serializers here
class BlogPageSerializer(serializers.ModelSerializer):
    class Meta:
        model=BlogPage
        fields="__all__"