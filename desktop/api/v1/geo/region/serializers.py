from rest_framework import serializers

from geo.models import Region


class RegionSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        region = Region(**validated_data)
        region.save()
        return region

    class Meta:
        model = Region
        exclude = ['id']
