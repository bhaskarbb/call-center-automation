from django.contrib import admin
from .models import Call, Transcript, Tone

# Register your models here.
admin.site.register(Call)
admin.site.register(Transcript)
admin.site.register(Tone)