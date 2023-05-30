from rest_framework.filters import BaseFilterBackend
from django.utils.timezone import now
from rest_framework import exceptions


class DateTimeCustomFilter(BaseFilterBackend):
    def __init__(self) -> None:
        self.months = {
        'January' :1,
        'February' : 2,
        'March' : 3,
        'April' : 4,
        'May' : 5,
        'June' : 6,
        'July' : 7,
        'August' : 8,
        'September' : 9,
        'October' : 10,
        'November' : 11,
        'December' : 12
    }
        super().__init__()
     
    def filter_queryset(self, request, queryset, view):
        query = self.get_filter_query_type(request)
        return super().filter_queryset(request, queryset, view)
    
    def get_filter_query_type(self,request) -> None | str:
        """This gets the exact field by which it is being filtered"""
        if 'days' in request.GET:
            return 'days'
        if 'months' in request.GET:
            return 'months'
        if 'hours' in request.GET:
            return 'hours'
        return None
    
    def get_filter_field(self,request):
        try:
            filter_by = request.GET['filter_by']
            if filter_by != 'last_modified' or 'date_added':
                raise exceptions.ParseError('filter_by must either be last_modified or date_added')
            return filter_by
        except KeyError:
            raise exceptions.ParseError('Filter_by needs to be part of the query_params')
    
    def filter_by_days(self,request):
        pass

    def filter_by_month(self,request,queryset):
        year = None
        month = request.GET['month']
        # Check if year is part of the query, if it is not, use the current year
        try:
            year = request.GET['year']
        except KeyError:
            pass
        if month not in self.months:
            raise exceptions.ParseError('Month param should be within the range of 1-12')
        if self.get_filter_field(request) == 'last_modified':
            return self.filter_by_last_modified(queryset,year=year,month=month)
        return self.filter_by_date_added(queryset,year=year,month=month)

    def filter_by_hours(self,request):
        try:
            hour = request.GET['hours']
            hour = int(hour)
            # queryset = 
        except KeyError:
            raise

    def filter_by_date_added(self,queryset,*args, **kwargs):
        #For month 
        if kwargs['month'] and kwargs['year'] is not None:
           month = kwargs['month']
           year = kwargs['year']
           filtered_queryset = queryset.objects.filter(date_added__month = self.months[month],date_added__year=int(year))
           return filtered_queryset 
        if kwargs['month']:
            month = kwargs['month']
            filtered_queryset = queryset.objects.filter(date_added__month=self.months[month],date_added__year=now().year)
            return filtered_queryset

    def filter_by_last_modified(self,queryset,*args, **kwargs):
         #For month 
        if kwargs['month'] and kwargs['year']:
           month = kwargs['month']
           year = kwargs['year']
           filtered_queryset = queryset.objects.filter(date_added__month = self.months[month],date_added__year=int(year))
           return filtered_queryset 
        if kwargs['month']:
            month = kwargs['month']
            filtered_queryset = queryset.objects.filter(date_added__month=self.months[month],date_added__year=now().year)
            return filtered_queryset