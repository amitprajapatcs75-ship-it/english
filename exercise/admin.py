from django.contrib import admin
from exercise.models.exercise import GrammarExercise, VocabularyExercise
from exercise.models.study import *

admin.site.register(GrammarExercise)
admin.site.register(VocabularyExercise)
admin.site.register(Song)
admin.site.register(Books)
admin.site.register(Article)
admin.site.register(Interview)
admin.site.register(Question)
admin.site.register(UserAnswer)