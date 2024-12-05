from django_filters import rest_framework as filters
from .models import Project


class ProjectFilter(filters.FilterSet):
    min_budget = filters.NumberFilter(field_name="budget", lookup_expr='gte')  # Минимальный бюджет
    max_budget = filters.NumberFilter(field_name="budget", lookup_expr='lte')  # Максимальный бюджет

    class Meta:
        model = Project
        fields = ['min_budget', 'max_budget']  # Настраиваемые поля фильтра
