from .models import Expenses
import django_filters
from datetime import timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta
class ExpenseFilter(django_filters.FilterSet):
    week=django_filters.NumberFilter(field_name='date',label='week',method='filter_week')
    month=django_filters.NumberFilter(field_name='date',label='month',method='filter_month')
    start_date = django_filters.DateFilter(
        field_name='date', 
        lookup_expr='gte',
        label='Fecha de inicio (YYYY-MM-DD)'
    )
    end_date = django_filters.DateFilter(
        field_name='date', 
        lookup_expr='lte',
        label='Fecha de fin (YYYY-MM-DD)'
    )
    def filter_week(self,queryset,name,value):
        if value:
            try:
                value = int(value)
                if value<=0:
                    return queryset.none()
            except (ValueError,TypeError):
                return queryset.none
            end_date = timezone.now().date()
            start_date = end_date - timedelta(weeks=value)
            return queryset.filter(date__gte=start_date,date__lte=end_date)
        return queryset
    def filter_month(self, queryset,name,value):
        if value:
            end_date = timezone.now().date()
            start_date = end_date - relativedelta(months=value)
            return queryset.filter(date__gte=start_date,date__lte=end_date)
        return queryset
    class Meta:
        model=Expenses
        fields=[]