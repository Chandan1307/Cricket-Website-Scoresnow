from scoresnow.series.models import Match, Stadium, Country, City
from django.conf import Settings
import requests


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
            match, created = Match.objects.get_or_create(key=litz_match["key"])
            stadium, created = Stadium.objects.get_or_create(key=litz_match["stadium"]["key"])
            country, created = Country.objects.get_or_create(name=litz_match["stadium"]["country"])
            city, created = City.objects.get_or_create(name=litz_match["stadium"]["city"])
            
            
            try:
                match.name = litz_match["name"]
                stadium.name = litz_match["stadium"]["name"]
                stadium.city = city
                stadium.country = country
            except:
                import ipdb
                ipdb.set_trace()
                pass
            
            match.title = litz_match.get("title")
            
            stadium.save()
            match.save()

