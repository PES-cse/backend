from django.contrib import admin
from .models import Certification, Research, User

admin.site.register(User)
admin.site.register(Certification)
admin.site.register(Research)
