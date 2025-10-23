from django.contrib import admin

from .models import *
from .models.onboarding import *
from users.models.home import *
from users.models.event import Event

admin.site.register(User)
admin.site.register(UserAim)
admin.site.register(Goal)
admin.site.register(UserGoal)
admin.site.register(ChooseTopics)
admin.site.register(SelectLevel)
admin.site.register(Home)
admin.site.register(Event)
admin.site.register(GoalRelation)
admin.site.register(UserTopicsRelation)
admin.site.register(UserGoalRelation)
admin.site.register(Friendship)
admin.site.register(UserProfile)
admin.site.register(Report)
admin.site.register(ContactUs)
admin.site.register(EnglishLevel)

