import imp
from django.http import HttpResponse

from django.shortcuts import render
from scoresnow.blog.models import BlogPage

from rest_framework import viewsets
from scoresnow.blog.models import BlogPage
from scoresnow.blog.serializers import BlogPageSerializer



def blog_view(request):
    post_objs = BlogPage.objects.all()
    ctx = {
        "posts": post_objs
    }
    return render(request, "blog/blog_index_page.html", context=ctx)


class BlogPageViewSet(viewsets.ModelViewSet):
    queryset = BlogPage.objects.all()
    serializer_class = BlogPageSerializer