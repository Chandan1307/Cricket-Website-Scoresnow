
# import logging

# from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
# from django.db.models import Sum
# from django.shortcuts import render
# from django.views.generic import TemplateView
# from rest_framework.authtoken.models import Token


# logger = logging.getLogger("justicepoker")

# # Create your views here.
# class HomePageView(TemplateView):
#     template_name = "home/index.html"

#     def get(self, request, format=None, **kwargs):
#         try:
#             link = DynamicSettings.objects.get(key="ANDROID_APP_LINK").value
#         except ObjectDoesNotExist:
#             link = ""
#         except MultipleObjectsReturned:
#             link = ""

#         return render(request, self.template_name, context={
#             "android_app_link": link
#         })
