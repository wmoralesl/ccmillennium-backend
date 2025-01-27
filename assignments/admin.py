from django.contrib import admin
from .models import Assignment, Submission, Content

# Register your models here.

admin.site.register(Assignment)
admin.site.register(Submission)

admin.site.register(Content)