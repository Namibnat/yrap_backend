from django.contrib import admin

from project.models import Project, Action, WeeklyReview


admin.site.register(Project)
admin.site.register(Action)
admin.site.register(WeeklyReview)