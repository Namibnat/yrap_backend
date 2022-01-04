from django.shortcuts import render
from django.views import View



class Routine(View):
    def get(self, request):
        template = 'routine/routine.html'
        context = {'title': 'Routines'}
        return render(request, template, context)