from django.contrib import admin

# Register your models here.
from company.models import Member, Position

admin.site.register(Member)
admin.site.register(Position)


