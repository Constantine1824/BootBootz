from rest_framework.filters import BaseFilterBackend
from django.utils.timezone import now
from rest_framework import exceptions
from datetime import timedelta


class DateTimeCustomFilter(BaseFilterBackend):
    def __init__(self):
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
        print(view.queryset.get(id=1))
        query = self.get_filter_query_type(request)
        if query == 'days':
            return self.filter_by_days(request,queryset)
        if query == 'hours':
            return self.filter_by_hours(request,queryset)
        if query == 'month':
            return self.filter_by_month(request,queryset)
        return queryset
    
    def get_filter_query_type(self,request):
        """This gets the exact field by which it is being filtered"""
        if 'days' in request.GET:
            return 'days'
        if 'month' in request.GET:
            return 'month'
        if 'hours' in request.GET:
            return 'hours'
        return None
    
    def get_filter_field(self,request):
            filter_by = request.GET.get('filter_by', None)
            if filter_by == 'last_modified':
                return filter_by
            return None

    def get_operator(self,request):
       try:
            arg = request.GET.get('arg')
            if arg == 'gt':
                return 'gt'
            if arg == 'lt':
                return 'lt'
       except KeyError:
            return 'eq'
    
    
    def filter_by_days(self,request,queryset):
        query = int(request.GET.get('days'))
        if self.get_filter_field(request) is not None:
            return self.filter_by_last_modified(queryset,request=request,days=query)
        return self.filter_by_date_added(queryset,request=request,days=query)

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
        if self.get_filter_field(request) is not None:
            return self.filter_by_last_modified(queryset,year=year,month=month)
        return self.filter_by_date_added(queryset,year=year,month=month)

    def filter_by_hours(self,request,queryset):
            hour = request.GET['hours']
            hour = int(hour)
            if self.get_filter_field(request) is not None:
                return self.filter_by_last_modified(queryset,request=request,hour=hour)
            return self.filter_by_date_added(queryset,request=request,hour=hour)

    def filter_by_date_added(self,queryset,*args, **kwargs):
        #For month 
        try:
            if kwargs['month'] and kwargs['year'] is not None:
                month = kwargs['month']
                year = kwargs['year']
                print(queryset)
                filtered_queryset = queryset.filter(date_added__month = self.months[month],date_added__year=int(year))
                return filtered_queryset 
            if kwargs['month']:
                month = kwargs['month']
                print(queryset)
                filtered_queryset = queryset.filter(date_added__month=self.months[month],date_added__year=now().year)
                return filtered_queryset
        except KeyError:
            pass
        #for hour
        try:
            if kwargs['hour']:
                hour = kwargs['hour']
                threshold = now() - timedelta(hours=hour)
                operator = self.get_operator(kwargs['request'])
                if operator == 'Gt':
                    return queryset.filter(date_added__gt=threshold)
                    
                if operator == 'lt':
                    return queryset.filter(date_added__lt=threshold)
                    
                if operator == 'eq':
                    return queryset.filter(date_added__lte=threshold)
        except KeyError:
            pass
         #for days
        if kwargs['days']:
            days = kwargs['days']
            threshold = now() - timedelta(days=days)
            operator = self.get_operator(kwargs['request'])
            if operator == 'Gt':
                return queryset.filter(date_added__gt=threshold)
                
            if operator == 'lt':
                return queryset.filter(date_added__lt=threshold)
                
            if operator == 'eq':
                return queryset.filter(date_added__lte=threshold)

    def filter_by_last_modified(self,queryset,*args, **kwargs):
         #For month 
        try:
            if kwargs['month'] and kwargs['year']:
                month = kwargs['month']
                year = kwargs['year']
                return queryset.filter(last_modified__month = self.months[month],last_modified__year=int(year))
            
            if kwargs['month']:
                month = kwargs['month']
                return queryset.filter(last_modified__month=self.months[month],last_modified__year=now().year)
        except KeyError:
            pass
        #for hour
        try:
            if kwargs['hour']:
                hour = kwargs['hour']
                threshold = now() - timedelta(hours=hour)
                operator = self.get_operator(kwargs['request'])
                if operator == 'Gt':
                    return queryset.filter(last_modified__gt=threshold)
                    
                if operator == 'lt':
                    return queryset.filter(last_modified__lt=threshold)
                    
                if operator == 'eq':
                    return queryset.filter(last_modified__lte=threshold)
        except KeyError:
            pass
        #for days
        if kwargs['days']:
            days = kwargs['days']
            threshold = now() - timedelta(days=days)
            operator = self.get_operator(kwargs['request'])
            if operator == 'Gt':
                return queryset.filter(last_modified__gt=threshold)
                
            if operator == 'lt':
                return queryset.filter(last_modified__lt=threshold)
                
            if operator == 'eq':
                return queryset.filter(last_modified__lte=threshold)
