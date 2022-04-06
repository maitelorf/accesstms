from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(Societe)
admin.site.register(Flotte)
admin.site.register(Equipement)
admin.site.register(Conducteur)
admin.site.register(Tournee)
admin.site.register(Etape)
admin.site.register(Client)



admin.site.register(User, UserAdmin)