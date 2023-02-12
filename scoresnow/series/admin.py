from django.contrib import admin

from scoresnow.series.models import SeriesPage, Match, Stadium

admin.site.register(SeriesPage)
admin.site.register(Match)
admin.site.register(Stadium)