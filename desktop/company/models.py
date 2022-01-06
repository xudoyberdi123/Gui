from django.db import models

from geo.models import Region, District
from . import PositionChoice, MemberChoice
from company import PositionChoice, MemberChoice

#
# class Profile(models.Model):
#     title = models.CharField(max_length=200, blank=False, null=False, )
#     email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
#     description = models.CharField(max_length=800, blank=True, null=True, )
#     phone_number = models.CharField(max_length=20, blank=True, null=True, )
#     lat = models.DecimalField("Latitude", max_digits=18, decimal_places=12, blank=True, null=True)
#     lng = models.DecimalField("Longitude", max_digits=18, decimal_places=12, blank=True, null=True)
#     address = models.CharField(max_length=500, blank=True, null=True, )
    # region = models.ForeignKey(
    #     Region, related_name='company_region', null=True, blank=True,
    #     on_delete=models.SET_NULL)
    #
    # district = models.ForeignKey(
    #     District, related_name='company_district', null=True, blank=True,
    #     on_delete=models.SET_NULL)

    # class Meta:
    #     verbose_name = "company"
    #     verbose_name_plural = "Companies"
    #
    # def __str__(self):
    #     return self.title


class Position(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    status = models.SmallIntegerField(choices=PositionChoice.STATUS_CHOICES, default=2, null=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Lavozim"
        verbose_name_plural = "Lavozimlar"


class Member(models.Model):
    firstname = models.CharField(max_length=30, blank=False, null=False)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    middlename = models.CharField(max_length=30, blank=True, null=True)
    social = models.JSONField(default={'fb': "", "ins": "", "git": "", 'tg': ""}, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.DateField(auto_now=False, blank=True, null=True)
    gender = models.BooleanField(default=True, null=False, )
    is_student = models.BooleanField(default=True, null=False, )
    join_date = models.DateField(auto_now=False, blank=False, null=False)
    address = models.CharField(max_length=255, blank=True, null=True)
    pass_serial = models.CharField(max_length=30, blank=True, null=True)
    position = models.ForeignKey(Position, related_name='position', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.SmallIntegerField(choices=MemberChoice.STATUS_CHOICES, default=2, null=False)
    region = models.ForeignKey(Region, related_name='member_region', null=True, blank=True, on_delete=models.SET_NULL)
    district = models.ForeignKey(District, related_name='member_district', null=True, blank=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return self.firstname

    class Meta:
        verbose_name = 'Xodim va a`zo'
        verbose_name_plural = "Xodimlar va A`zolar"
