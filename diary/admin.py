from django.contrib import admin

from .models import Comment, Note, PhotoPage, PlanPage, Stamp

admin.site.register(Note)
admin.site.register(PlanPage)
admin.site.register(PhotoPage)
admin.site.register(Comment)
admin.site.register(Stamp)
