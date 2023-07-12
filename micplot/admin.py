from django.contrib import admin

from .models import Show,Act,Mic,Scene,MicPos

for model in [Show,Act,Mic,Scene,MicPos]:
    admin.site.register(model)