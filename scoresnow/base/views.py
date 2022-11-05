import imp
from django.http import HttpResponse

from django.shortcuts import render
from scoresnow.blog.models import BlogPage
from scoresnow.series.models import SeriesIndexPage, SeriesPage
from scoresnow.teams.models import TeamsPage


def home_view(request):
    series = SeriesPage.objects.all()
    teams = TeamsPage.objects.all()
    blog = BlogPage.objects.all()
    ctx = {
        "series": series,
        "teams": teams,
        "blog": blog
    }
    return render(request, "base/home_page.html", context=ctx)