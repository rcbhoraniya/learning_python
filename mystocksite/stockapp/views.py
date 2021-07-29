from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .models import Stock,Stock_price
from django.http import HttpResponseRedirect,HttpResponse
from .forms import StockForm,FilterForm
from django.shortcuts import render
from django.views import View
from datetime import date,datetime,timedelta
from django.db.models import Avg, Max, Min, Sum, Count
from django.db.models import OuterRef, Subquery
from django.db.models.functions import Lower
from django.db import connection
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mystocksite.mystocksite.settings'



class StockListView(ListView):
    template_name = 'stockapp/index.html'
    context_object_name = 'stockslist'
    paginate_by = 9

    def get_queryset(self):  # new
        return Stock.objects.order_by('name')

class StockDetailListView(ListView):
    template_name = 'stockapp/detail.html'
    context_object_name = 'stocksdetail'
    paginate_by = 50
    def get_queryset(self):
        self.id = get_object_or_404(Stock, id=self.kwargs['id'])
        stock_obj = Stock_price.objects.order_by('date').filter(stock_id_id=self.id)
            # .filter(date__year = '2021')
        return stock_obj

    def get_context_data(self, **kwargs):
        name = get_object_or_404(Stock, id=self.kwargs['id'])
        data = super().get_context_data(**kwargs)
        data['stockname'] = name
        data['exchange'] = 'NSE'
        return data


class AddStockFormView(View):
    form_class = StockForm
    initial = {'key': 'value'}
    template_name = 'stockapp/stock-add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            # <process form cleaned data>
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})
import pandas as pd
today = datetime.today().strftime('%Y-%m-%d')
date1 = pd.to_datetime(today)
class SearchView(ListView):
    template_name = 'stockapp/search.html'
    context_object_name = 'all_search_results'
    # paginate_by = 9

    def get_queryset(self):

        query = self.request.GET.get('search')
        if query == 'new_closing_high':
            postresult= Stock_price.objects.filter(stock_id_id =OuterRef("pk")).filter(date__gte=datetime.today()-timedelta(days=365)).values('stock_id_id').annotate(max_close=Max('close')).order_by('-max_close')
            postresult1 = Stock.objects.all().annotate( max_close=Subquery(postresult.values('max_close')[:1] ),date =Subquery(postresult.values('date')[:1] ) ).order_by('nse_symbol')
            postresult2 = postresult1.filter(date = date1.date() )
            print(postresult2)
            print(date1.date())
            result = postresult1
        else:

           result = Stock.objects.order_by('name')
        return result




