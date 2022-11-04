from rest_framework import serializers
from scoresnow.series.models import Stadium
from scoresnow.series.models import MatchStatus
from scoresnow.series.models import Match



#create serializers here
class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model=Match
        fields="__all__"

