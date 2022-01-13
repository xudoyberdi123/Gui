from rest_framework import serializers

from education.models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        models = Group
        fields = "__all__"


