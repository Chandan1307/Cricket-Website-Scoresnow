import imp
from django.http import HttpResponse

from django.shortcuts import render
from scoresnow.blog.models import BlogPage




def blog_view(request):
    post_objs = BlogPage.objects.all()
    ctx = {
        "posts": post_objs
    }
    return render(request, "blog/blog_index_page.html", context=ctx)