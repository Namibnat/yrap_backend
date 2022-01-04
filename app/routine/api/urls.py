from django.urls import path

from routine.api.views import (StudyChunkScoreCardPagesAPIView, AuthorAPIView,
                               StudyChunkScoreCardCurPageAPIView, StudyChunkScoreCardDetailWorkOn,
                               StudyChunkScoreCardTodayAchievement, JustDoItAPIView, JustDoItMakeTodayView,
                               JustDoItCheckTodayView)

urlpatterns = [
    path(
        "studychunkscorecard/",
        StudyChunkScoreCardPagesAPIView.as_view(),
        name="studychunkscorecardpages-list"
    ),
    path(
        "authors/",
        AuthorAPIView.as_view(),
        name="author-list"
    ),
    path(
        "studychunkscorecard/<int:pk>/",
        StudyChunkScoreCardCurPageAPIView.as_view(),
        name='studychunkscorecardpages-detail'
    ),
    path("studychunkscorecard_workon/<int:pk>/<str:reference>/",
         StudyChunkScoreCardDetailWorkOn.as_view(),
         name='studychunkscorecard-work-on'
         ),
    path(
        'studychunkscorecard_achieved/<int:pk>/<int:achieved>/',
        StudyChunkScoreCardTodayAchievement.as_view(),
        name="study-chunk-today-achieved"
    ),
    path(
        'justdoit/',
        JustDoItAPIView.as_view(),
        name="justdoit-list"
    ),
    path(
        'justdoit/make_today/',
        JustDoItMakeTodayView.as_view(),
        name="justdoit-make_today"
    ),
    path(
        'justdoit/checked/',
        JustDoItCheckTodayView.as_view(),
        name='justdoit-checked'
    )

]
