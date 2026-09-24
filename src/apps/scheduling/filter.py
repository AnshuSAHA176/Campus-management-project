import django_filters
from .models import ClassSession

class ClassSeasionFilter(django_filters.FilterSet):

    date = django_filters.DateFilter()
    date__gt = django_filters.DateFilter(field_name='date',lookup_expr='gt')
    date__lt = django_filters.DateFilter(field_name='date',lookup_expr='lt')
    date_range = django_filters.DateFromToRangeFilter(field_name='date',label='Filter by Date Range')
    teacher = django_filters.NumberFilter(field_name='teacher',lookup_expr='exact')
    batch = django_filters.NumberFilter(field_name='batch',lookup_expr='exact')

    room = django_filters.NumberFilter(field_name='room',lookup_expr='exact')
    subject = django_filters.NumberFilter(field_name='subject',lookup_expr='exact')

    status = django_filters.CharFilter(field_name='status',lookup_expr='exact')

    class Meta:
        model = ClassSession
        fields = [
            'date',
            'teacher',
            'batch',
            'room',
            'subject',
            'status',
        ]