from os import access
import requests

from scoresnow.series.models import Match


def get_access_token():
    from django.conf import settings
    if not settings.DEBUG:
        access_token = CoreSettings.objects.get(key="CRICKET_API_TOKEN").value
        return access_token
    data = {
        'access_key': 'a04ff762220ed4c43183707e2b23c368',
        'secret_key': 'dd7328f5827e4c506a22e72678f8f721',
        'app_id': 'league11.in',
        'device_id': 'developer'
    }

    response = requests.post('https://rest.cricketapi.com/rest/v2/auth/', data=data)
    access_token = response.json()["auth"]["access_token"]
    return access_token


class LitzMatch():

    def get_matches(self):
        data = []
        access_token = get_access_token()
        url = "https://rest.cricketapi.com/rest/v2/schedule/?access_token={}".format(access_token)
        response = requests.post(url, data=data)

        result = response.json()
        schedule = result["data"]["months"][0]["days"]

        for day in schedule:
            day_matches = day["matches"]

            for litz_match in day_matches:
                match = Match.objects.get_or_create(key=litz_match.get("key"))

                match.name = litz_match.get("name")
                match.country = litz_match.get("country")
                match.city = litz_match.get("city")
                match.start_date = litz_match.get("start_date")
                match.title = litz_match.get("title")

                match.save()


        data = response.json()
        return data
        
    def get_matches_details(self):
        data =[]
        access_token = get_access_token()
        url = "https://rest.cricketapi.com/rest/v2/schedule/?access_token={}".format(access_token)
        response = requests.post(url, data=data)

        data = response.json()
        return data



        # Match Model Object Created/Ignore.
        # Match.objects.create(
        # )


















