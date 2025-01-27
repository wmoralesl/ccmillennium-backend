from django.contrib import admin
from .models import Course, Group, Module, Enrollment
# Register your models here.

admin.site.register(Course)
admin.site.register(Group)
admin.site.register(Module)
admin.site.register(Enrollment)