from django.contrib import admin
from django.db.models.base import ModelBase
from backend import models

class CardAdmin(admin.ModelAdmin):
    list_display= ('name', 'admin_thumbnail')

admin.site.register(models.Card, CardAdmin)



for model_name in dir(models):
    m = getattr(models, model_name)
    if isinstance(m, ModelBase) and not m._meta.abstract:
        try:
            admin.site.register(m)
        except admin.sites.AlreadyRegistered:
            pass