import imp
from django.http import HttpResponse

from django.shortcuts import render
from scoresnow.series.models import SeriesPage

# from rest_framework import viewsets
# from scoresnow.series.models import Company
# from scoresnow.series.serializers import CompanySerializer



def series_view(request):
    post_objs = SeriesPage.objects.all()
    ctx = {
        "series": post_objs
    }
    return render(request, "series/series_index_page.html", context=ctx)



# # API
# class CompanyViewSet(viewsets.ModelViewSet):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
