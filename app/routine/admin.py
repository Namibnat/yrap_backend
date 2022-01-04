from django.contrib import admin

from .models import (
    Author, JustDoIt, StudyChunkScoreCard,
    StudyChunkScoreCardPages, JustDoItDay
)


admin.site.register(Author)
admin.site.register(JustDoIt)
admin.site.register(JustDoItDay)
admin.site.register(StudyChunkScoreCard)
admin.site.register(StudyChunkScoreCardPages)
