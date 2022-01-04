"""Routines API view"""

import datetime
import json
from django.utils import timezone

from django.views import View
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from routine.api.graph import (StudyChunkScoreCardGraph)

from routine.models import (
    Author, StudyChunkScoreCard, StudyChunkScoreCardPages, JustDoIt, JustDoItDay
)
from routine.api.serializers import (
    AuthorSerializer, StudyChunkScoreCardSerializer, JustDoItSerializer
)


class StudyChunkScoreCardDetailWorkOn(View):
    def get(self, request, pk, reference):
        """
        date = models.DateTimeField()
        achieved = models.IntegerField()
        target = models.IntegerField()
        """
        today_date = timezone.now()
        context = {}
        context['got_data'] = True
        graph_maker = StudyChunkScoreCardGraph(pk, reference)
        context['graph'] = graph_maker.make_graph()
        study_item = StudyChunkScoreCard.objects.get(pk=pk)
        try:
            today = StudyChunkScoreCardPages.objects.get(
                reference=study_item,
                date__year=today_date.year,
                date__month=today_date.month,
                date__day=today_date.day)
            context['achieved'] = today.achieved
            context['target'] = today.target
        except StudyChunkScoreCardPages.DoesNotExist:
            context['got_data'] = False
        return JsonResponse(context)


class StudyChunkScoreCardTodayAchievement(View):
    def put(self, request, pk, achieved):
        context = {}
        study_item = StudyChunkScoreCard.objects.get(pk=pk)
        today_date = timezone.now().date()
        today_page_card = StudyChunkScoreCardPages.objects.get(
            date__year=today_date.year,
            date__month=today_date.month,
            date__day=today_date.day)
        today_page_card.did_today = True
        today_page_card.save()

        try:
            upcoming_days = StudyChunkScoreCardPages.objects.filter(
                reference=study_item,
                date__gte=today_date)
        except StudyChunkScoreCardPages.DoesNotExist:
            return JsonResponse(context)
        upcoming_days.update(achieved=achieved)
        for day in upcoming_days:
            day.save()
        graph_maker = StudyChunkScoreCardGraph(
            pk, study_item.reference, did_today=True)
        context['graph'] = graph_maker.make_graph()
        return JsonResponse(context)


class StudyChunkScoreCardPagesAPIView(APIView):
    def get(self, request):
        type_of_exercise = StudyChunkScoreCard.objects.all()
        serializer = StudyChunkScoreCardSerializer(type_of_exercise, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudyChunkScoreCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorAPIView(APIView):
    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudyChunkScoreCardCurPageAPIView(APIView):
    def get_object(self, pk):
        study_item = get_object_or_404(StudyChunkScoreCard, pk=pk)
        return study_item

    def get(self, request, pk):
        study_item = self.get_object(pk)
        serializer = StudyChunkScoreCardSerializer(study_item)
        return Response(serializer.data)

    def put(self, request, pk):
        study_item = self.get_object(pk)
        serializer = StudyChunkScoreCardSerializer(
            study_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        study_item = self.get_object(pk)
        study_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JustDoItAPIView(APIView):
    def get(self, request, *args, **kwargs):
        just_do_it_items = JustDoIt.objects.all()
        serializer = JustDoItSerializer(just_do_it_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JustDoItSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JustDoItMakeTodayView(View):
    def post(self, request):
        context = {}
        just_do_it_items = JustDoIt.objects.all()
        for i, item in enumerate(just_do_it_items):
            day, _ = JustDoItDay.objects.get_or_create(
                justdoit=item, date=timezone.now().date())
            context[i] = {'id': item.pk, 'checked': day.checked}
            print(context[i])

        return JsonResponse(context)


class JustDoItCheckTodayView(View):
    def get(self, request):
        context = {}
        just_do_it_day = JustDoItDay.objects.filter(date=timezone.now())
        for i, item in enumerate(just_do_it_day):
            context[i] = {'id': item.pk, 'checked': item.checked}
        return JsonResponse(context)

    def put(self, request):
        context = {}
        data = json.loads(request.body)
        for item in data:
            if 'checked' not in item:
                continue
            just_do_it = JustDoIt.objects.get(pk=item['id'])
            just_do_it_day = JustDoItDay.objects.get(justdoit=just_do_it, date=timezone.now())
            just_do_it_day.checked = item['checked']
            just_do_it_day.save()
        return JsonResponse(context)
