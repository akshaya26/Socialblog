from django.contrib import admin
from . import models

# Register your models here.
#for showing group members with group in admin
class GroupMemberInline(admin.TabularInline):
    model=models.GroupMember

admin.site.register(models.Group)