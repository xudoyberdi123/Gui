from rest_framework import serializers

from education.models import GroupStudent


class GrSerializer(serializers.ModelSerializer):
    class Meta:
        models = GroupStudent
        fields = "__all__"


