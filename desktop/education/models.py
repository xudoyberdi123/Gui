from django.db import models

# Create your models here.
from base import CourceLangType

from base.models import StatusModel
from company.models import Member


class Course(models.Model):
    name = models.CharField(max_length=256)
    lang = models.CharField(max_length=50, choices=CourceLangType.CHOICES)
    price = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.name


class Group(StatusModel):
    name = models.CharField(max_length=120, blank=False, null=False)
    course = models.ForeignKey(Course, related_name='group_course', blank=True, null=True, on_delete=models.SET_NULL,
                               limit_choices_to={'active_status': 2}, )
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)
    teacher = models.ForeignKey(Member, related_name='teachers1', blank=False, null=False, on_delete=models.CASCADE,
                                  limit_choices_to={'is_student': False}, )
    assistant = models.ForeignKey(Member, related_name='teachers2', blank=True, null=True, on_delete=models.SET_NULL,
                                  limit_choices_to={'is_student': False}, )
    price_month = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'O`quv Gruh'
        verbose_name_plural = 'Gruppalar'


class GroupStudent(StatusModel):
    student = models.ForeignKey(Member, related_name='group_student', blank=False, null=False,
                                on_delete=models.CASCADE, limit_choices_to={'is_student': True}, )
    group = models.ForeignKey(Group, related_name='groups', blank=False, null=False, on_delete=models.CASCADE)
    joined_date = models.DateField(blank=False, null=False)
    leave_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = (('student', 'group'),)
        verbose_name = "Guruh Talabasi"
        verbose_name_plural = "Talabalar"

    def __str__(self):
        return f"{self.student}"


