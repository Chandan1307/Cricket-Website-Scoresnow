import imp
from django.http import HttpResponse

from django.shortcuts import render
from scoresnow.series.models import SeriesPage




def series_view(request):
    post_objs = SeriesPage.objects.all()
    ctx = {
        "series": post_objs
    }
    return render(request, "series/series_index_page.html", context=ctx)