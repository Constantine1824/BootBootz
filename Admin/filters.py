from rest_framework.filters import BaseFilterBackend


class DateTimeCustomFilter(BaseFilterBackend) -> None |  str:
    def get_filter_query_type(self,request):
        """This gets the exact field by which it is being filtered"""
        if 'days' in request.GET:
            return 'days'
        if 'months' in request.GET:
            return 'months'
        if 'hours' in request.GET:
            return 'hours'
        return None
    
    def filter_queryset(self, request, queryset, view):
        query = self.get_filter_query_type(request)
        return super().filter_queryset(request, queryset, view)
    
    def filter_by_days(self,request):
        pass

    def filter_by_month(self,request):
        pass

    def filter_by_hours(self,request):
        try:
            hour = request.GET['hours']
            hour = int(hour)
            # queryset = 
        except KeyError:
            raise