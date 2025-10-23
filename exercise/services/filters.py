import django_filters
from django.db.models import Q
from exercise.models.exercise import GrammarExercise
# from exercise.models.study import StudyMaterials

class GrammarFilter(django_filters.FilterSet):
    topic_name = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    q =django_filters.CharFilter(method='query_search')

    class Meta:
        model = GrammarExercise
        fields = ["topic_name", "name"]

    def query_search(self, queryset, name, value):
        return queryset.filter(
            Q(topic_name__icontains=value)|
            Q(name__icontains=value)
        )

# class StudyFilter(django_filters.FilterSet):
#     tag = django_filters.CharFilter(lookup_expr='icontains')
#     q =django_filters.CharFilter(method='query_search')
#
#     class Meta:
#         model = StudyMaterials
#         fields = ["tag"]
#
#     def query_search(self, queryset, name, value):
#         return queryset.filter(
#             Q(tag__exact=value)
#         )

