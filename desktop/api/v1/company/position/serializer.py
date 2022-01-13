from rest_framework import serializers

from company.models import Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        models = Position
        fields = "__all__"


