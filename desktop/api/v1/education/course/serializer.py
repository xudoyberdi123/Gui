from rest_framework import serializers

from education.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        models = Course
        fields = "__all__"


