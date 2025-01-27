from django.contrib import admin
from .models import User, StudentParent, Parent

# Register your models here.
admin.site.register(User)
admin.site.register(Parent)
admin.site.register(StudentParent)