from rest_framework import serializers

from geo.models import District


class DistrictSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['region_id'] = validated_data.pop("region")
        district = District(**validated_data)
        district.save()
        return district

    class Meta:
        model = District
        exclude = ['id']
