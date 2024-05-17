from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Utilisateur)
admin.site.register(Donneur)
admin.site.register(Annonce)
admin.site.register(Notification)
admin.site.register(EffectueDon)
admin.site.register(Demande)
admin.site.register(NotifEnvoyer)
admin.site.register(Tokens)
admin.site.register(Problems)

