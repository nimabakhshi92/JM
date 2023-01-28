from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Imam)
admin.site.register(Narration)
admin.site.register(NarrationSubject)
admin.site.register(NarrationVerse)
admin.site.register(NarrationFootnote)
admin.site.register(Book)
admin.site.register(QuranVerse)
admin.site.register(ContentSummaryTree)
