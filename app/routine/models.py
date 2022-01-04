"""Models for different routines

TODO: There's lots that can be made more dry in the code.
"""

import datetime
from django.utils import timezone
import pytz
import json
from django.db import models


class Author(models.Model):
    """Authors of books I'm working through"""
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20)


def __str__(self):
    return self.name


class StudyChunkScoreCard(models.Model):
    """A routine for things that have a set number of chunks.

    For example, it might be pages of a book, lessons in a course, etc.

    TODO: change datetimes to dates, so that I don't have to do gymnastics to avoid zerodivision errors.
    """
    reference = models.CharField(max_length=25, unique=True)
    goal = models.CharField(max_length=250)
    authors = models.ManyToManyField(Author, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    start_page = models.IntegerField()
    end_page = models.IntegerField()

    def save(self, *args, **kwargs):
        created = not self.pk
        self.end_date = datetime.datetime(
            self.end_date.year,
            self.end_date.month,
            self.end_date.day,
            tzinfo=timezone.utc
        )
        self.start_date = datetime.datetime(
            self.start_date.year,
            self.start_date.month,
            self.start_date.day,
            tzinfo=timezone.utc
        )
        super().save(*args, **kwargs)
        date_marker = self.start_date
        if created:
            page = self.start_page
            while True:
                end = (date_marker.year == self.end_date.year) and (
                    date_marker.month == self.end_date.month) and (date_marker.day == self.end_date.day)
                if end:
                    page = self.end_page
                else:
                    try:
                        page += (self.end_page - page) / \
                            (self.end_date - date_marker).days
                    except ZeroDivisionError:
                        page = self.end_page
                page = int(round(page, 0))
                new_line = StudyChunkScoreCardPages(
                    reference=self,
                    date=date_marker,
                    achieved=self.start_page,
                    target=page
                )
                new_line.save()
                date_marker += datetime.timedelta(days=1)
                if end:
                    break

    def __str__(self):
        return self.reference


class StudyChunkScoreCardPages(models.Model):
    """The day by day goals in chunks, such as up to what lesson to reach in a given day"""
    date = models.DateTimeField()
    achieved = models.IntegerField()
    target = models.IntegerField()
    reference = models.ForeignKey(StudyChunkScoreCard,
                                  on_delete=models.CASCADE)
    did_today = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reference.reference} for {self.date:%d/%m/%Y}"


class TypeOfExercise(models.Model):
    """Simply a description of an exercise type"""
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class Reps(models.Model):
    """Reps per set, can have weight optionally, which for now is just in kilograms"""
    rep = models.IntegerField()
    weight = models.IntegerField(
        help_text="Weight in kilograms", blank=True, null=True)

    def __str__(self):
        if self.weight:
            return f"{self.rep} reps at {self.weight}Kg"
        else:
            return str(self.rep)


class Exercise(models.Model):
    """An exercise, with how many reps and sets were done.

    No date added, so this can be re-used if it happens that there's one that matches,
    which should happen often
    """
    type_of_exercise = models.ForeignKey(
        TypeOfExercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.ManyToManyField(Reps)

    def __str__(self):
        return f"{self.type_of_exercise.description}: {self.reps} reps"


class Workout(models.Model):
    """On a given day, the workout

    A workout here is refering to a reps and sets
    kind of workout.  A cycle or walk would have to be
    recorded as a 'just did it' item
    """
    date = models.DateField(auto_now_add=True)
    exercise = models.ManyToManyField(Exercise)

    def __str__(self):
        return f"{self.pk} - {self.date:%d/%m/%Y}"


class RoutineItem(models.Model):
    """Basically, a checklist item, and a record of it being checked or not"""
    item = models.CharField(max_length=25)
    checked = models.BooleanField(default=False)

    def __str__(self):
        checked = "done" if self.checked else "not done"
        return f"{self.pk} - {self.item} - {checked}"


class RoutineItemOrder(models.Model):
    """A list of items in a routine checklist"""
    item = models.ManyToManyField(RoutineItem)
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.pk} - {self.item} at position {self.order}"


class Routine(models.Model):
    """A reusable checklist"""
    description = models.CharField(max_length=200)
    item = models.ManyToManyField(RoutineItemOrder)

    def __str__(self):
        return f"{self.description} routine"


class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.ManyToManyField(Author)

    def __str__(self):
        return f"{self.pk} - {self.title} book"


# Author, StudyChunkScoreCard, StudyChunkScoreCardPages, TypeOfExercise, Reps, Exercise, Workout, RoutineItem, RoutineItemOrder, Routine, Book,

class BookProgress(models.Model):
    """Reading a book through progress through it

    This allows me, for example, to plan to read a 300 page
    book in a week, and given the number of days in the week,
    automatically divide up the book into the right number of pages
    to read on a given day, ensuring that the book gets done in the
    allocated time if followed.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    start_page = models.IntegerField()
    end_page = models.IntegerField()
    is_done = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """When saving it, I want to lay out the targest for pages to read per day

        This uses the number of days and divides up the pages accordingly in order to
        complete the book.
        """
        created = not self.pk
        self.end_date = datetime.datetime(
            self.end_date.year,
            self.end_date.month,
            self.end_date.day,
            tzinfo=timezone.utc
        )
        self.start_date = datetime.datetime(
            self.start_date.year,
            self.start_date.month,
            self.start_date.day,
            tzinfo=timezone.utc
        )
        super().save(*args, **kwargs)
        date_marker = self.start_date
        if created:
            page = self.start_page
            while True:
                end = (date_marker.year == self.end_date.year) and (
                    date_marker.month == self.end_date.month) and (date_marker.day == self.end_date.day)
                if end:
                    page = self.end_page
                else:
                    try:
                        page += (self.end_page - page) / \
                            (self.end_date - date_marker).days
                    except ZeroDivisionError:
                        page = self.end_page
                page = int(round(page, 0))
                new_line = ReadChunkScoreCardPages(
                    reference=self,
                    date=date_marker,
                    achieved=self.start_page,
                    target=page
                )
                new_line.save()
                date_marker += datetime.timedelta(days=1)
                if end:
                    break


class ReadChunkScoreCardPages(models.Model):
    """The day by day goals in chunks, such as up to what lesson to reach in a given day"""
    date = models.DateTimeField()
    achieved = models.IntegerField()
    target = models.IntegerField()
    reference = models.ForeignKey(BookProgress,
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reference.reference} page {self.pk}"


class BooksReadThisYear(models.Model):
    """Record the books read in a given year

    Ideally this should allow me to set a goal of how many
    books I want to read and complete them in the year.

    Books can be blank so that I can start the year without any books read.

    These don't include things like textbooks, or others that are part of a study
    plan (see StudyChunkScoreCard for that).
    """
    books = models.ManyToManyField(BookProgress, blank=True)
    year = models.IntegerField(default=datetime.datetime.now().year)
    goal = models.IntegerField(help_text="How many books I plan to read")

    def __str__(self):
        return f"Read {self.goal} in {self.year}"


class JustDoIt(models.Model):
    """Items I just want to record as done or not.

    May be short term, or unlimited
    """
    description = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f"{self.description}"


class JustDoItDay(models.Model):
    """Each day a just do it item was done/not done"""
    justdoit = models.ForeignKey(JustDoIt,
                                 on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    checked = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.justdoit.description} on {self.date:%d/%m/%Y}"

    
