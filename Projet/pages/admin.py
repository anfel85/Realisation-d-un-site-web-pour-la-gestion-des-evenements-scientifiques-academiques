from django.contrib import admin
from .models import Evénement ,participation,soumission,CoAuteur , Evaluation ,Invitation , Affectation ,Encheres , Presentation ,Guide
# Register your models here.

admin.site.register(Evénement)
admin.site.register(participation)
admin.site.register(soumission)
admin.site.register(CoAuteur)
admin.site.register(Evaluation)
admin.site.register(Invitation)
admin.site.register(Affectation)
admin.site.register(Encheres)
admin.site.register(Presentation)
admin.site.register(Guide)