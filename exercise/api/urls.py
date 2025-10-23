from django.urls import path
from exercise.api.views import *


urlpatterns = [
    path("api/", ExerciseApiView.as_view(), name="exercise_api"),
    path("grammar/",GrammarApiView.as_view(), name="grammar_exercise"),
    path("vocabulary/",VocabularyApiView.as_view(), name="vocabulary_exercise"),
    path("song/",SongApiView.as_view(), name="songs"),
    path("book/", BookApiView.as_view(), name="books"),
    path("article/", ArticleApiView.as_view(), name="articles"),
    path("interview/", InterviewApiView.as_view(), name="interviews"),
    path("question/", QuestionApiView.as_view(), name="questions"),
]