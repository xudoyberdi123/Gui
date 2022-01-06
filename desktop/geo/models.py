from django.db import models


class Region(models.Model):
    id = models.AutoField(primary_key=True, null=False, )
    name = models.CharField(max_length=100, db_index=True, verbose_name="rus name")
    ordering = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class District(models.Model):
    id = models.AutoField(primary_key=True, null=False, )
    name = models.CharField(max_length=100, db_index=True, verbose_name="rus name")
    region = models.ForeignKey(Region, related_name="district_region", on_delete=models.CASCADE)
    ordering = models.PositiveIntegerField(default=0)

    @property
    def parent(self):
        return self.region

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
