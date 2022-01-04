from django.db import models


class State(models.TextChoices):
    ACTIVE = "AC", "Active"
    DONE = "DO", "Done"
    DELETED = "DE", "Deleted"
    SOMEDAY = "SO", "Someday/Maybe"


class Project(models.Model):
    name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    done = models.DateTimeField(blank=True, null=True)
    done_when = models.CharField(max_length=250)
    state = models.CharField(
        max_length=2,
        choices=State.choices,
        default=State.ACTIVE,
    )

    def __str__(self):
        return self.name


class Action(models.Model):
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
    )
    action = models.CharField(max_length=250)
    added = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(
        default=False,
        verbose_name="Is it done"
    )
    is_next_action = models.BooleanField(default=False)

    def __str__(self):
        return self.action


class WeeklyReview(models.Model):
    week_start = models.DateTimeField()
    week_end = models.DateTimeField()
    actions = models.ManyToManyField(Action)

    def __str__(self):
        return f"{self.week_start:%d/%m/%Y} to {self.week_end:%d/%m/%Y}"
