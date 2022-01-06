from rest_framework import serializers

from company.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        models = Member
        fields = "__all__"


