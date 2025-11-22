from django.contrib import admin
from .models import UserProfile  # Only register your Django models here

admin.site.register(UserProfile)
