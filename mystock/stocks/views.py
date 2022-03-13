import csv
import io
import pandas as pd
import numpy as np
import requests as r
import openpyxl
from nsepy import get_history
from nsepy.history import get_price_list
from django.db.models.functions import Cast
# from django.http import HttpResponseRedirect
# from django.urls import reverse_lazy
from django.http import HttpResponse, FileResponse
from django.views.generic import *
# from .models import *
from django.db.models import *
from datetime import *
from django.db.models import Subquery
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import *
from django.contrib.auth.forms import *
from django.shortcuts import redirect, get_object_or_404
import yfinance as yf
from datetime import datetime, timedelta, date, time
import xlsxwriter
from django.utils import timezone

TODAY_DATETIME = datetime.now()
TODAY_DATE = datetime.now().date()
TODAY_S = TODAY_DATE.strftime('%Y-%m-%d') + ' 15:31:00'
MARKET_CLOSE_DATETIME = pd.to_datetime(TODAY_S)

pd.set_option('display.width', 1500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 50)


class PermissionDeniedView(TemplateView):
    template_name = 'stocks/permission_denied.html'


class UserAccessMixin(PermissionRequiredMixin, LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('toris:permissiondenied')
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'stocks/registration.html'
    success_url = reverse_lazy('stocks:login')


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'stocks/login.html'
    next_page = 'stocks:index'
    # redirect_field_name = 'stocks:index'


class UserLogoutView(LogoutView):
    # template_name = 'stocks/logout.html'
    next_page = 'stocks:login'


class IndexView(UserAccessMixin, ListView):
    permission_required = ('stocks.view_stockmap',)

    template_name = 'portfolio/index.html'
    context_object_name = 'stock_list'

    # paginate_by = 20

    def get_queryset(self):
        stockdata_subqs = StockData.objects.filter(company=OuterRef("pk")).filter(
            company__is_portfolio_stock=True).values(
            'company').annotate(qty_sum=Sum(F('quantity') * F('side')),
                                price_sum=Sum(F('price') * F('side') * F('quantity')),
                                average_price=Sum(F('price') * F('side') * F('quantity')) / Sum(
                                    F('quantity') * F('side')))
        nsedata_subqs = NSEData.objects.filter(symbol=OuterRef("pk"))

        data = StockMap.objects.filter(is_portfolio_stock=True).annotate(
            qty_sum=Subquery(stockdata_subqs.values('qty_sum')),
            price_sum=Subquery(stockdata_subqs.values('price_sum')[:1]),
            average_price=Subquery(stockdata_subqs.values('average_price')[:1]),
            close=Subquery(nsedata_subqs.values('lastprice')[:1]),
            date=Subquery(nsedata_subqs.values('date')[:1]),
            w52_high=Subquery(nsedata_subqs.values('yearhigh')[:1]),
            w52_low=Subquery(nsedata_subqs.values('yearlow')[:1]),
            change=Subquery(nsedata_subqs.values('change')[:1]),
            pchange=Subquery(nsedata_subqs.values('pchange')[:1]),
            per_down=F('close') * 100 / F('w52_high') - 100,
            today_value=F('close') * F('qty_sum'),
            profit=F('today_value') - F('price_sum')
        ).order_by('name')
        # for item in data:
        #     print(item.name,item.profit)
        total_investment = 0
        profit_sum = 0

        for item in data:
            total_investment += item.price_sum
            profit_sum += item.profit

        data = data.annotate(
            total_investment=Cast(total_investment, output_field=DecimalField(max_digits=12, decimal_places=2)),
            profit_sum=Cast(profit_sum, output_field=DecimalField(max_digits=12, decimal_places=2)))
        data = data.annotate(portweight=F('price_sum') * 100 / F('total_investment'),
                             profit_percentage=F('today_value') * 100 / F('price_sum') - 100,
                             port_per_up=F('profit_sum') * 100 / F('total_investment'))
        # print(data)
        return data


class SectorStockListView(UserAccessMixin, ListView):  ################
    permission_required = ('stocks.view_stockmap',)

    template_name = 'portfolio/index.html'
    context_object_name = 'stock_list'

    def get_queryset(self):
        print(self.kwargs['sector'])
        stockdata_subqs = StockData.objects.filter(company=OuterRef("pk")).filter(
            company__sector__sector=self.kwargs['sector']).values(
            'company').annotate(qty_sum=Sum(F('quantity') * F('side')),
                                price_sum=Sum(F('price') * F('side') * F('quantity')),
                                average_price=Sum(F('price') * F('side') * F('quantity')) / Sum(
                                    F('quantity') * F('side')))
        nsedata_subqs = NSEData.objects.filter(symbol=OuterRef("pk"))

        data = StockMap.objects.filter(is_portfolio_stock=True).filter(sector__sector =self.kwargs['sector'] ).annotate(
            qty_sum=Subquery(stockdata_subqs.values('qty_sum')),
            price_sum=Subquery(stockdata_subqs.values('price_sum')[:1]),
            average_price=Subquery(stockdata_subqs.values('average_price')[:1]),
            close=Subquery(nsedata_subqs.values('lastprice')[:1]),
            date=Subquery(nsedata_subqs.values('date')[:1]),
            w52_high=Subquery(nsedata_subqs.values('yearhigh')[:1]),
            w52_low=Subquery(nsedata_subqs.values('yearlow')[:1]),
            change=Subquery(nsedata_subqs.values('change')[:1]),
            pchange=Subquery(nsedata_subqs.values('pchange')[:1]),
            per_down=F('close') * 100 / F('w52_high') - 100,
            today_value=F('close') * F('qty_sum'),
            profit=F('today_value') - F('price_sum')
        ).order_by('name')
        data = data.filter(qty_sum__gt=0)
        print(data)

        for item in data:
            print(item.name, item.profit)

        total_investment = 0
        profit_sum = 0

        for item in data:
            total_investment += item.price_sum
            profit_sum += item.profit

        data = data.annotate(
            total_investment=Cast(total_investment, output_field=DecimalField(max_digits=12, decimal_places=2)),
            profit_sum=Cast(profit_sum, output_field=DecimalField(max_digits=12, decimal_places=2)))
        data = data.annotate(portweight=F('price_sum') * 100 / F('total_investment'),
                             profit_percentage=F('today_value') * 100 / F('price_sum') - 100,
                             port_per_up=F('profit_sum') * 100 / F('total_investment'))
        # print(data)
        return data


class StockDetailView(UserAccessMixin, ListView):
    permission_required = ('stocks.view_stockmap',)

    model = StockMap
    template_name = 'stocks/portfolio_stock_detail.html'
    context_object_name = 'stock_list'

    def get_queryset(self):
        start_date = TODAY_DATE - timedelta(days=365)

        self.stockmap = get_object_or_404(StockMap, id=self.kwargs['pk'])
        nse_data = NSEData.objects.filter(symbol=self.stockmap).first()
        # print(nse_data.date)
        hist_data = HistoricalData.objects.filter(Q(company=self.stockmap) & Q(date__gte=start_date)).order_by('date')
        year_avg = hist_data.aggregate(Avg('close'))
        # print(year_avg['close__avg'])
        historical_data = HistoricalData.objects.filter(Q(company=self.stockmap) & Q(date__gte=start_date)).order_by(
            'date').annotate(
            avg_200=Window(expression=Avg('close'), order_by=F('date').asc(), frame=RowRange(start=-199, end=0)),
            avg_100=Window(expression=Avg('close'), order_by=F('date').asc(), frame=RowRange(start=-99, end=0)),
            avg_50=Window(expression=Avg('close'), order_by=F('date').asc(), frame=RowRange(start=-49, end=0)))
        # print(historical_data)
        historical_data_last_obj = historical_data.order_by('date').last()
        # Fibonacci Pivot Points
        # Pivot Point(P) = (High + Low + Close) / 3
        # Support 1(S1) = P - {.382 * (High - Low)}
        # Support 2(S2) = P - {.618 * (High - Low)}
        # Support 3(S3) = P - {1 * (High - Low)}
        # Resistance 1(R1) = P + {.382 * (High - Low)}
        # Resistance 2(R2) = P + {.618 * (High - Low)}
        # Resistance 3(R3) = P + {1 * (High - Low)}
        pivot = (historical_data_last_obj.close + historical_data_last_obj.low + historical_data_last_obj.high) / 3
        h_l = historical_data_last_obj.high - historical_data_last_obj.low
        s1 = pivot - h_l * 382 / 1000
        s2 = pivot - h_l * 618 / 1000
        s3 = pivot - h_l * 1
        r1 = pivot + h_l * 382 / 1000
        r2 = pivot + h_l * 618 / 1000
        r3 = pivot + h_l * 1

        maximum_price = historical_data.order_by('-close').first()
        minimum_price = historical_data.order_by('close').first()
        difference = maximum_price.close - minimum_price.close
        first_level = maximum_price.close - difference * 236 / 1000
        second_level = maximum_price.close - difference * 382 / 1000
        third_level = maximum_price.close - difference * 5 / 10
        fourth_level = maximum_price.close - difference * 618 / 1000

        queryset = StockData.objects.filter(company=self.stockmap).values(
            'company__name', 'company').annotate(
            qty_sum=Sum(F('quantity') * F('side')),
            price_sum=Sum(F('price') * F('side') * F('quantity')),
            average_price=Sum(F('price') * F('side') * F('quantity')) / Sum(F('quantity') * F('side')),
            today_value=Sum(F('quantity') * F('side') * nse_data.lastprice),
            profit=Sum(F('quantity') * F('side')) * nse_data.lastprice - Sum(F('price') * F('side') * F('quantity')),
            close=Value(nse_data.lastprice, output_field=DecimalField(max_digits=12, decimal_places=2)),
            date=Value(nse_data.date, output_field=DateTimeField()),
            w52_high=Value(nse_data.yearhigh, output_field=DecimalField(max_digits=12, decimal_places=2)),
            w52_low=Value(nse_data.yearlow, output_field=DecimalField(max_digits=12, decimal_places=2)),
            per_down=F('close') * 100 / F('w52_high') - 100,
            w52_avg=Value(year_avg['close__avg'], output_field=DecimalField(max_digits=12, decimal_places=2)),
            profit_percentage=F('today_value') * 100 / F('price_sum') - 100,
            corporate_action=Value(nse_data.corporate_action, output_field=CharField(max_length=100)),
            x_date=Value(nse_data.x_date, output_field=DateTimeField()),
            year_high=Value(maximum_price.close, output_field=DecimalField(max_digits=12, decimal_places=2)),
            year_high_date=Value(maximum_price.date, output_field=DateTimeField()),
            year_low=Value(minimum_price.close, output_field=DecimalField(max_digits=12, decimal_places=2)),
            year_low_date=Value(minimum_price.date, output_field=DateTimeField()),
            first_level=Value(first_level, output_field=DecimalField(max_digits=12, decimal_places=2)),
            second_level=Value(second_level, output_field=DecimalField(max_digits=12, decimal_places=2)),
            third_level=Value(third_level, output_field=DecimalField(max_digits=12, decimal_places=2)),
            fourth_level=Value(fourth_level, output_field=DecimalField(max_digits=12, decimal_places=2)),
            avg_200=Value(historical_data_last_obj.avg_200, output_field=DecimalField(max_digits=12, decimal_places=2)),
            avg_100=Value(historical_data_last_obj.avg_100, output_field=DecimalField(max_digits=12, decimal_places=2)),
            avg_50=Value(historical_data_last_obj.avg_50, output_field=DecimalField(max_digits=12, decimal_places=2)),
            s1=Value(s1, output_field=DecimalField(max_digits=12, decimal_places=2)),
            s2=Value(s2, output_field=DecimalField(max_digits=12, decimal_places=2)),
            s3=Value(s3, output_field=DecimalField(max_digits=12, decimal_places=2)),
            r1=Value(r1, output_field=DecimalField(max_digits=12, decimal_places=2)),
            r2=Value(r2, output_field=DecimalField(max_digits=12, decimal_places=2)),
            r3=Value(r3, output_field=DecimalField(max_digits=12, decimal_places=2)),
            pivot=Value(pivot, output_field=DecimalField(max_digits=12, decimal_places=2)),

        )
        # print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        end_date = TODAY_DATE - timedelta(days=365)
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        queryset = HistoricalData.objects.filter(
            Q(company=self.kwargs['pk']) & Q(date__range=(end_date, TODAY_DATE))).order_by(
            'date')
        maximum_price = queryset.order_by('-close').first()
        minimum_price = queryset.order_by('close').first()
        difference = maximum_price.close - minimum_price.close
        first_level = maximum_price.close - difference * 236 / 1000
        second_level = maximum_price.close - difference * 382 / 1000
        third_level = maximum_price.close - difference * 5 / 10
        fourth_level = maximum_price.close - difference * 618 / 1000
        data = queryset.annotate(
            year_high=Value(maximum_price.close, output_field=DecimalField(max_digits=12, decimal_places=2)),
            year_high_date=Value(maximum_price.date, output_field=DateTimeField()),
            year_low=Value(minimum_price.close, output_field=DecimalField(max_digits=12, decimal_places=2)),
            year_low_date=Value(minimum_price.date, output_field=DateTimeField()),
            first_level=Value(first_level, output_field=DecimalField(max_digits=12, decimal_places=2)),
            second_level=Value(second_level, output_field=DecimalField(max_digits=12, decimal_places=2)),
            third_level=Value(third_level, output_field=DecimalField(max_digits=12, decimal_places=2)),
            fourth_level=Value(fourth_level, output_field=DecimalField(max_digits=12, decimal_places=2)),
            avg_200=Window(expression=Avg('close'), order_by=F('date').asc(), frame=RowRange(start=-199, end=0)),
            avg_100=Window(expression=Avg('close'), order_by=F('date').asc(), frame=RowRange(start=-99, end=0)),
            avg_50=Window(expression=Avg('close'), order_by=F('date').asc(), frame=RowRange(start=-49, end=0)),
        ).order_by('date')

        context['stock_hist'] = data
        context['stockdata_list'] = StockMap.objects.get(id=self.kwargs['pk']).stockdata_set.all().order_by('date')

        return context


class HistoricalDataView(UserAccessMixin, ListView):
    permission_required = ('stocks.view_stockmap',)

    template_name = 'stocks/portfolio_stock_history.html'
    context_object_name = 'stock_hist'

    # paginate_by = 20

    def get_queryset(self):
        end_date = TODAY_DATE - timedelta(days=365)
        queryset = HistoricalData.objects.filter(
            Q(company=self.kwargs['pk']) & Q(date__range=(end_date, TODAY_DATE))).order_by(
            'date')
        maximum_price = queryset.order_by('-close').first()
        minimum_price = queryset.order_by('close').first()
        difference = maximum_price.close - minimum_price.close
        first_level = maximum_price.close - difference * 236 / 1000
        second_level = maximum_price.close - difference * 382 / 1000
        third_level = maximum_price.close - difference * 5 / 10
        fourth_level = maximum_price.close - difference * 618 / 1000
        data = queryset.annotate(
            year_high=Value(maximum_price.close, output_field=DecimalField(max_digits=12, decimal_places=2)),
            year_high_date=Value(maximum_price.date, output_field=DateTimeField()),
            year_low=Value(minimum_price.close, output_field=DecimalField(max_digits=12, decimal_places=2)),
            year_low_date=Value(minimum_price.date, output_field=DateTimeField()),
            first_level=Value(first_level, output_field=DecimalField(max_digits=12, decimal_places=2)),
            second_level=Value(second_level, output_field=DecimalField(max_digits=12, decimal_places=2)),
            third_level=Value(third_level, output_field=DecimalField(max_digits=12, decimal_places=2)),
            fourth_level=Value(fourth_level, output_field=DecimalField(max_digits=12, decimal_places=2)),
            avg_200=Window(expression=Avg('close'), order_by=F('date').asc(), frame=RowRange(start=-199, end=0)),
            avg_100=Window(expression=Avg('close'), order_by=F('date').asc(), frame=RowRange(start=-99, end=0)),
            avg_50=Window(expression=Avg('close'), order_by=F('date').asc(), frame=RowRange(start=-49, end=0)),
        ).order_by('date')
        # print(data)
        return data


class SectorAnalysis(UserAccessMixin, ListView):
    raise_exception = True
    permission_required = ('stocks.view_stockmap',)
    permission_denied_message = 'No permission'
    login_url = 'stocks:login'
    redirect_field_name = 'next'

    template_name = 'stocks/portfolio_stock_sector.html'
    context_object_name = 'stock_sector'

    def get_queryset(self):
        stockdata_subqs = StockData.objects.filter(company=OuterRef("pk")).values('company').alias(
            sumzero=Sum(F('quantity') * F('side'))).filter(
            sumzero__gt=0).annotate(price_sum=Sum(F('price') * F('side') * F('quantity')))

        stockmap_sector_sum_subqs = StockMap.objects.filter(sector=OuterRef("pk")).values('sector').annotate(
            comp_sec_sum=Sum(Subquery(stockdata_subqs.values('price_sum'))))

        sector_sum = Sector.objects.annotate(sector_sum=Sum((stockmap_sector_sum_subqs.values('comp_sec_sum')))).filter(
            sector_sum__gt=0)

        sector_total = 0
        for item in sector_sum:
            sector_total += item.sector_sum
        data = sector_sum.annotate(
            sector_total=Cast(sector_total, output_field=DecimalField(max_digits=12, decimal_places=2)),
            weight=F('sector_sum') * 100 / F('sector_total'))
        # print(data)
        return data


class MarketCapAnalysis(UserAccessMixin, ListView):
    permission_required = ('stocks.view_stockmap',)

    template_name = 'stocks/portfolio_stock_marketcap.html'
    context_object_name = 'stock_marketcap'

    def get_queryset(self):
        stockdata = StockData.objects.filter(company=OuterRef("pk")).values('company').alias(
            sumzero=Sum(F('quantity') * F('side'))).filter(
            sumzero__gt=0).annotate(price_sum=Sum(F('price') * F('side') * F('quantity')))
        stockmap_m_cap_sum = StockMap.objects.filter(m_cap=OuterRef("pk")).values('m_cap').annotate(
            comp_sec_sum=Sum(Subquery(stockdata.values('price_sum'))))
        m_cap_sum = MarketCap.objects.annotate(m_cap_sum=Sum((stockmap_m_cap_sum.values('comp_sec_sum')))).filter(
            m_cap_sum__gt=0)

        mcap_total = 0
        for item in m_cap_sum:
            mcap_total += item.m_cap_sum
        data = m_cap_sum.annotate(
            mcap_total=Cast(mcap_total, output_field=DecimalField(max_digits=12, decimal_places=2)),
            weight=F('m_cap_sum') * 100 / F('mcap_total'))

        # for i in data:
        #     print(i.__dict__)
        return data


class SearchView(UserAccessMixin, ListView):
    permission_required = ('stocks.view_stockmap',)

    template_name = 'stocks/search.html'
    context_object_name = 'all_search_results'

    # paginate_by = 9

    def get_queryset(self):

        qs = self.request.GET.get('search')
        if qs == 'new_closing_low':
            qsr = HistoricalData.objects.filter(company=OuterRef("pk"))

            get_data365 = qsr.filter(date__gte=date.today() - timedelta(days=365))
            today_hist = get_data365.order_by('-date')
            get_max = get_data365.order_by('-close')
            get_min = get_data365.order_by('close')
            get_avg = get_data365.values('company').annotate(average_price=Avg(F('close')))

            result = StockMap.objects.all().filter(is_portfolio_stock=True).annotate(
                max_close=Subquery(get_max.values('high')[:1]),
                max_date=Subquery(get_max.values('date')[:1]),
                min_close=Subquery(get_min.values('low')[:1]),
                min_date=Subquery(get_min.values('date')[:1]),
                close=Subquery(today_hist.values('close')[:1]),
                low=Subquery(today_hist.values('low')[:1]),
                high=Subquery(today_hist.values('high')[:1]),
                date=Subquery(today_hist.values('date')[:1]),
                avg_price=Subquery(get_avg.values('average_price')), ).filter(close__lte=F('min_close') * 1.05)

        elif qs == 'new_closing_high':
            qsr = HistoricalData.objects.filter(company=OuterRef("pk"))

            get_data365 = qsr.filter(date__gte=date.today() - timedelta(days=365))
            today_hist = get_data365.order_by('-date')
            get_max = get_data365.order_by('-close')
            get_min = get_data365.order_by('close')
            get_avg = get_data365.values('company').annotate(average_price=Avg(F('close')))

            result = StockMap.objects.all().filter(is_portfolio_stock=True).annotate(
                max_close=Subquery(get_max.values('high')[:1]),
                max_date=Subquery(get_max.values('date')[:1]),
                min_close=Subquery(get_min.values('low')[:1]),
                min_date=Subquery(get_min.values('date')[:1]),
                close=Subquery(today_hist.values('close')[:1]),
                low=Subquery(today_hist.values('low')[:1]),
                high=Subquery(today_hist.values('high')[:1]),
                date=Subquery(today_hist.values('date')[:1]),
                avg_price=Subquery(get_avg.values('average_price')), ).filter(close__gte=F('max_close') * 1.01)
        else:
            result = StockMap.objects.order_by('name')
        # print(result)
        return result


class StockMapListView(UserAccessMixin, ListView):
    permission_required = ('stocks.view_stockmap',)

    model = StockMap
    template_name = 'stocks/stockmap_list.html'
    context_object_name = 'stockmap_list'
    queryset = StockMap.objects.order_by('name')


class StockMapDetailView(UserAccessMixin, DetailView):
    permission_required = ('stocks.view_stockmap',)

    model = StockMap
    template_name = 'stocks/stockmap_detail.html'
    # context_object_name = 'stockmapdetail'


class StockMapUpdateView(UserAccessMixin, UpdateView):
    permission_required = ('stocks.change_stockmap',)

    model = StockMap
    form_class = StockForm
    # fields = ['name','m_cap','sector','nse_symbol','moneycontrol_symbol',
    # 'yahoo_symbol','scrip_code','is_portfolio_stock']
    template_name_suffix = '_update_form'


class StockMapCreateView(UserAccessMixin, CreateView):
    permission_required = ('stocks.add_stockmap',)

    model = StockMap
    form_class = StockForm
    template_name = 'stocks/stockmap_add_form.html'


class StockMapDeleteView(UserAccessMixin, DeleteView):
    permission_required = ('stocks.delete_stockmap',)

    model = StockMap
    template_name = 'stocks/stockmap_delete.html'
    success_url = reverse_lazy('stocks:stockmap_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)


class SectorListView(UserAccessMixin, ListView):
    permission_required = ('stocks.view_sector',)

    model = Sector
    template_name = 'stocks/sector_list.html'
    context_object_name = 'sector_list'
    queryset = Sector.objects.order_by('sector')


class SectorDetailView(UserAccessMixin, DetailView):
    permission_required = ('stocks.view_sector',)

    model = Sector
    template_name = 'stocks/sector_detail.html'


class SectorUpdateView(UserAccessMixin, UpdateView):
    permission_required = ('stocks.change_sector',)

    model = Sector
    form_class = SectorForm
    # fields = ['name','m_cap','sector','nse_symbol','moneycontrol_symbol',
    # 'yahoo_symbol','scrip_code','is_portfolio_stock']
    template_name_suffix = '_update_form'


class SectorCreateView(UserAccessMixin, CreateView):
    permission_required = ('stocks.add_sector',)

    model = Sector
    form_class = SectorForm
    template_name = 'stocks/sector_add_form.html'


class SectorDeleteView(UserAccessMixin, DeleteView):
    permission_required = ('stocks.delete_sector',)

    model = Sector
    template_name = 'stocks/sector_delete.html'
    success_url = reverse_lazy('stocks:sector_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)


class StockDataListView(UserAccessMixin, ListView):
    permission_required = ('stocks.view_stockdata',)

    start_date = date.today()
    end_date = start_date - timedelta(days=365)

    model = StockData
    template_name = 'stocks/stockdata_list.html'
    context_object_name = 'stockdata_list'
    queryset = StockData.objects.filter(date__range=(end_date, start_date)).order_by('-date')


class StockDataDetailView(UserAccessMixin, DetailView):
    permission_required = ('stocks.view_stockdata',)

    model = StockData
    template_name = 'stocks/stockdata_detail.html'


class StockDataUpdateView(UserAccessMixin, UpdateView):
    permission_required = ('stocks.change_stockdata',)

    model = StockData
    form_class = StockDataForm
    template_name_suffix = '_update_form'


class StockDataCreateView(UserAccessMixin, CreateView):
    permission_required = ('stocks.add_stockdata',)

    model = StockData
    form_class = StockDataForm
    template_name = 'stocks/stockdata_add_form.html'


class StockDataDeleteView(UserAccessMixin, DeleteView):
    permission_required = ('stocks.delete_stockdata',)

    model = StockData
    template_name = 'stocks/stockdata_delete.html'
    success_url = reverse_lazy('stocks:stockdata_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)


class HistoricalDataListView(UserAccessMixin, ListView):
    permission_required = ('stocks.view_historicaldata',)

    model = HistoricalData
    template_name = 'stocks/historicaldata_list.html'
    context_object_name = 'historicaldata_list'
    queryset = HistoricalData.objects.order_by('-date')[:100]


class HistoricalDataDetailView(UserAccessMixin, DetailView):
    permission_required = ('stocks.view_historicaldata',)

    model = HistoricalData
    template_name = 'stocks/historicaldata_detail.html'


class HistoricalDataUpdateView(UserAccessMixin, UpdateView):
    permission_required = ('stocks.change_historicaldata',)

    model = HistoricalData
    form_class = HistoricalDataForm
    # fields = ['name','m_cap','sector','nse_symbol','moneycontrol_symbol',
    # 'yahoo_symbol','scrip_code','is_portfolio_stock']
    template_name_suffix = '_update_form'


class HistoricalDataCreateView(UserAccessMixin, CreateView):
    permission_required = ('stocks.add_historicaldata',)

    model = HistoricalData
    form_class = HistoricalDataForm
    template_name = 'stocks/historicaldata_add_form.html'


class HistoricalDataDeleteView(UserAccessMixin, DeleteView):
    permission_required = ('stocks.delete_historicaldata',)

    model = HistoricalData
    template_name = 'stocks/historicaldata_delete.html'
    success_url = reverse_lazy('stocks:historicaldata_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)


def refresh_price_data(request):
    # ticker_list = StockMap.objects.filter(is_portfolio_stock=True).order_by('id').values_list('id', 'yahoo_symbol')
    def convert_float(val):
        return float(val)

    def convert_int(val):
        val = float(val)
        val_n = val * 100000
        return int(val_n)

    def convert_val(val):
        val_n = val.replace('-', ' ')
        val_n = datetime.strptime(val_n, '%d %b %Y')
        return val_n

    def get_nse_data():
        url = 'https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/nifty500StockWatch.json'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            "Accept-Language": 'en-US,en;q=0.9', "Accept-Encoding": 'gzip, deflate'}
        cookie_dict = {
            'bm_sv': 'bm_sv=B683127B319CDEE635D5372C90911E65~9bcie0JgYimO/ip/zZyr7MogxfyXlHq+Tz5Ui7Zhe2uEabg2yRXR4tGEB6fLuPo5NOfwvNh+fLoL+24U2NS/6RnomTLCaKkqrvMGVymRDeXQvV0BPqISClZsOss1CDEbSSLSCr0PBEZlCovszNGVtGObdpFqxB7xlKx'}

        session = r.session()
        dicts = session.get(url, headers=headers).json()
        df = pd.DataFrame(dicts['data'])
        df = df.sort_values('symbol')
        # print(df)
        df = df[['symbol', 'cAct', 'xDt', 'open', 'high', 'low', 'ltP', 'ptsC', 'per', 'trdVol', 'wkhi', 'wklo',
                 'previousClose', 'dayEndClose', 'iislPtsChange', 'iislPercChange', 'yPC', 'mPC']]
        column = ['symbol', 'c_act', 'xdt', 'open', 'high', 'low', 'ltp', 'ptsc', 'per', 'trdvol', 'wkhi', 'wklo',
                  'previousclose', 'dayendclose', 'iislptschange', 'iislpercchange', 'ypct', 'mpct']
        df.columns = column
        df = df.replace('-', 0)
        # print(df)
        # print(df.info())
        df = df.sort_values(by="symbol")
        df = df.replace({',': ''}, regex=True)
        df = df.reset_index(drop='index')
        df['xdt'] = df['xdt'].apply(convert_val)
        col = df.columns

        for col_name in df.columns:
            if col_name == col[0] or col_name == col[1] or col_name == col[2]:
                continue
            elif col_name == col[9]:
                df[col_name] = df[col_name].apply(convert_int)
            else:
                df[col_name] = df[col_name].apply(convert_float)
        df = df.round(2)
        return df

    df = get_nse_data()
    # print(df)
    # print(df.info())
    ticker_list = StockMap.objects.order_by('id').values_list('id', 'nse_symbol')
    # print(ticker_list)

    for i, (id, comp) in enumerate(ticker_list):
        nsedf = df.loc[df['symbol'] == comp]
        if nsedf.empty:
            pass
        else:
            nse = nsedf.values.tolist()
            nse = nse[0]
            # print(nse)
            try:
                obj = NSEData.objects.get(symbol=id)

                obj.open = nse[3]
                obj.dayhigh = nse[4]
                obj.daylow = nse[5]
                obj.lastprice = nse[6]
                obj.change = nse[7]
                obj.pchange = nse[8]
                obj.totaltradedvolume = nse[9]
                obj.yearhigh = nse[10]
                obj.yearlow = nse[11]
                obj.previousclose = nse[12]
                obj.perchange365d = nse[16]
                obj.perchange30d = nse[17]
                obj.dayendclose = nse[13]
                obj.corporate_action = nse[1]
                obj.x_date = nse[2]
                obj.date = datetime.today()
                obj.save()
                print(obj)
            except NSEData.DoesNotExist:
                lastobj = NSEData(
                    is_deleted=False,
                    deleted_at=None,
                    symbol=StockMap.objects.get(nse_symbol=comp),
                    date=datetime.today(),
                    open=nse[3],
                    dayhigh=nse[4],
                    daylow=nse[5],
                    lastprice=nse[6],
                    change=nse[7],
                    pchange=nse[8],
                    totaltradedvolume=nse[9],
                    yearhigh=nse[10],
                    yearlow=nse[11],
                    previousclose=nse[12],
                    perchange365d=nse[16],
                    perchange30d=nse[17],
                    dayendclose=nse[13],
                    corporate_action=nse[1],
                    x_date=nse[2]
                )
                lastobj.save()
                print(lastobj)
    return redirect(reverse('stocks:index'))


def BulkCreateHistoricalData(request):
    ticker_list = StockMap.objects.filter(is_portfolio_stock=True).order_by('id').values_list('id', 'yahoo_symbol')
    for i, (id, ticker) in enumerate(ticker_list):

        start_date = None
        end_date = None
        if TODAY_DATETIME < MARKET_CLOSE_DATETIME:
            end_date = TODAY_DATE - timedelta(days=1)
        else:
            end_date = TODAY_DATE

        last_obj = HistoricalData.objects.filter(company=id).order_by('date').last()
        # last_obj.date = last_obj.date- timedelta(days=2)
        if last_obj is None:
            start_date = date(2007, 1, 1)
            pass
        else:
            last_obj_date = last_obj.date.date()
            print(last_obj_date)
            # current_date = TODAY_DATE
            # print(current_date)
            ed = last_obj.date.strftime("%A")
            print(ed)
            # hist = yf.download(ticker, start=start_date, end=end_date)
            if ed == 'Friday' and last_obj_date == TODAY_DATE:
                print(f"1.Already Upto Date no need to update")
                pass
            elif ed == 'Friday' and last_obj_date + timedelta(days=1) == TODAY_DATE:
                print(f"2.Already Upto Date no need to update")
                pass
            elif ed == 'Friday' and last_obj_date + timedelta(days=2) == TODAY_DATE:
                print(f"3.Already Upto Date no need to update")
                pass
            else:
                start_date = last_obj_date + timedelta(days=1)

        if start_date >= end_date:
            print('start=', start_date, 'end=', end_date)
            print(f"4.Already Upto Date no need to update")
            pass

        else:
            # print(start_date)
            print('start=', start_date, 'end=', end_date)
            try:
                hist = yf.download(ticker, start=start_date, end=end_date)
                hist['Date'] = hist.index
                hist['company_id'] = id
                hist['ticker'] = ticker
                hist = hist[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'company_id', 'ticker']]
                hist = hist.dropna(
                    subset=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'company_id', 'ticker'])
                print(hist)
                datas = hist.values.tolist()

                bulkdata = []
                for data in datas:
                    obj = HistoricalData(
                        is_deleted=False,
                        deleted_at=None,
                        date=data[0],
                        open=data[1],
                        high=data[2],
                        low=data[3],
                        close=data[4],
                        adj_close=data[5],
                        volume=data[6],
                        company_id=data[7])
                    bulkdata.append(obj)
                    print(obj)
                    # obj.save()
                HistoricalData.objects.bulk_create(bulkdata)
            except:
                print("error")
                pass

    return redirect(reverse('stocks:historicaldata_list'))


def BulkCreateNSEHistorical(request):
    ticker_list = StockMap.objects.filter(is_portfolio_stock=True).order_by('id').values_list('id', 'nse_symbol')
    ticker_list = ticker_list
    for i, (id, ticker) in enumerate(ticker_list):

        start_date = None
        end_date = None
        if TODAY_DATETIME < MARKET_CLOSE_DATETIME:
            end_date = TODAY_DATE - timedelta(days=1)
        else:
            end_date = TODAY_DATE

        last_obj = NSEHistorical.objects.filter(symbol=id).order_by('date').last()
        # last_obj.date = last_obj.date- timedelta(days=2)
        if last_obj is None:
            start_date = date(2007, 1, 1)
            pass
        else:
            last_obj_date = last_obj.date
            # print(last_obj_date)
            # current_date = TODAY_DATE
            # print(current_date)
            ed = last_obj.date.strftime("%A")
            print(ed)
            # hist = yf.download(ticker, start=start_date, end=end_date)
            if ed == 'Friday' and last_obj_date == TODAY_DATE:
                print(f"1.Already Upto Date no need to update")
                pass
            elif ed == 'Friday' and last_obj_date + timedelta(days=1) == TODAY_DATE:
                print(f"2.Already Upto Date no need to update")
                pass
            elif ed == 'Friday' and last_obj_date + timedelta(days=2) == TODAY_DATE:
                print(f"3.Already Upto Date no need to update")
                pass
            else:
                start_date = last_obj_date + timedelta(days=1)
        print('start=', start_date, 'end=', end_date)
        if start_date >= end_date:
            print(f"4.Already Upto Date no need to update")
            pass
        else:
            print('-----------------------------------------------------------')
            print(f'Downloading data for {ticker}')
            try:
                hist = get_history(symbol=ticker, start=start_date, end=end_date)
                hist['Date'] = hist.index
                hist['symbol_id'] = id
                hist['ticker'] = ticker
                hist = hist[
                    ['Date', 'Symbol', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'Volume',
                     'Deliverable Volume',
                     '%Deliverble']]
                hist = hist.dropna(
                    subset=['Date', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'Volume',
                            'Deliverable Volume',
                            '%Deliverble'])
                print(hist)
                if hist.empty:
                    pass
                else:
                    datas = hist.values.tolist()
                    for data in datas:
                        obj = NSEHistorical(
                            is_deleted=False,
                            deleted_at=None,
                            date=data[0],
                            symbol=StockMap.objects.get(nse_symbol=ticker),
                            prv_close=data[2],
                            open=data[3],
                            high=data[4],
                            low=data[5],
                            last=data[6],
                            close=data[7],
                            volume=data[8],
                            deliverable_volume=data[9],
                            deliverble_per=data[10])

                        print(obj)
                        obj.save()
            except:
                print("error")
                pass

    return redirect(reverse('stocks:historicaldata_list'))


def BulkCreateNSEBhavcopy(requests):
    # file = f'C:\\Users\\raj\\Desktop\\stocks_marketcap.csv'
    # with open(file, 'r') as f:
    #     csvreader = csv.reader(f)
    #     fields = next(csvreader)
    #     for row in csvreader:
    #         obj = MarketCap(market_cap=row[3],is_deleted = False,deleted_at = None)
    #         print(obj)
    #         obj.save()
    #
    # file = f'C:\\Users\\raj\\Desktop\\stocks_sector.csv'
    # with open(file, 'r') as f:
    #     csvreader = csv.reader(f)
    #     fields = next(csvreader)
    #     for row in csvreader:
    #         obj = Sector(sector=row[3], is_deleted=row[1], deleted_at=None)
    #         print(obj)
    #         obj.save()
    #
    #
    #
    # file = f'C:\\Users\\raj\\Desktop\\stocks_stockmap.csv'
    # with open(file, 'r') as f:
    #     csvreader = csv.reader(f)
    #     fields = next(csvreader)
    #     for row in csvreader:
    #         # print(row[8])
    #         obj = StockMap(name=row[3],nse_symbol=row[4],moneycontrol_symbol=row[5],
    #                      yahoo_symbol=row[6],scrip_code=row[7],is_portfolio_stock=row[8],
    #                      m_cap_id=row[9],sector_id=row[10],is_deleted=False, deleted_at=None)
    #         print(obj)
    #         obj.save()
    #
    # file = f'C:\\Users\\raj\\Desktop\\stocks_stockdata.csv'
    # with open(file, 'r') as f:
    #     csvreader = csv.reader(f)
    #     fields = next(csvreader)
    #     for row in csvreader:
    #         # print(row[8])
    #         obj = StockData(date=row[3],side=row[4],quantity=row[5],
    #                      price=row[6],trade_num=row[7],company_id=row[8],
    #                      is_deleted=row[1], deleted_at=None)
    #         print(obj)
    #         obj.save()

    PREVIOUS_DAY = TODAY_DATE - timedelta(days=1)
    ticker_list = StockMap.objects.filter(is_portfolio_stock=True).order_by('id').values_list('id', 'nse_symbol')
    bhavcopy = get_price_list(dt=TODAY_DATE)
    print(bhavcopy)
    for i, (id, comp) in enumerate(ticker_list):
        last_obj = HistoricalData.objects.filter(company=id).order_by('date').last()
        if last_obj.date.date() == TODAY_DATE:
            print(f'Already updated {comp}')
            pass
        else:
            bdf = bhavcopy.loc[bhavcopy['SYMBOL'] == comp]
            if bdf.empty:
                pass
            else:
                data = bdf.values.tolist()
                data = data[0]
                print(data)

                lastobj = HistoricalData(
                    is_deleted=False,
                    deleted_at=None,
                    company=StockMap.objects.get(nse_symbol=comp),
                    date=TODAY_DATE,
                    open=data[2],
                    high=data[3],
                    low=data[4],
                    close=data[5],
                    adj_close=data[5],
                    volume=data[8])
                lastobj.save()
                print(lastobj)
    return redirect(reverse('stocks:historicaldata_list'))


def str_to_float(string):
    bad_chars = [';', ':', '!', "*",
                 '?', '/', '₹', ',']
    test_string = string
    for i in bad_chars:
        test_string = test_string.replace(i, '')

    return float(test_string)


# def bulkCreateStockData(request):
#     excel_read_file = r'C:\Users\raj\Desktop\my_trade.xlsx'
#     df = pd.read_excel(excel_read_file, sheet_name="Data")
#     column = df.columns
#     df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y/%d/%m')
#     df['price'] = df['price'].apply(str_to_float)
#     df = df.astype({'date': 'str', 'trade_time': 'str'})
#     df['DateAndTime'] = df['date'].str.cat(df['trade_time'], sep=" ")
#     df['date'] = pd.to_datetime(df['DateAndTime'])
#     df = df.drop(columns=['DateAndTime'])
#     df.sort_values("date", inplace=True)
#     df = df.reset_index(drop='index')
#     # print(df)
#     df = df.replace([np.nan], 0.0)
#     df['side'] = df['side'].map({'B': 1, 'S': -1, 'Buy': 1, 'Sell': -1})
#     df = df.astype(
#         {'date': 'datetime64[ns]', 'company': 'str', 'trade_num': 'int64', 'side': 'int', 'quantity': 'int',
#          'price': 'float'})
#     df = df.drop_duplicates(keep='first')
#     df = df[['date', 'company', 'side', 'quantity', 'price', 'trade_num']]
#     # print(df)
#     if df.empty:
#         print(f'There is no Data in {excel_read_file} for Upload in stocks_stockdata table')
#         ans = input(f'Enter any key for continue....... ')
#         pass
#     else:
#         df = df[['date', 'side', 'quantity', 'price', 'trade_num', 'company']]
#         print(df)
#         datas = df.values.tolist()
#         print(datas)
#         for data in datas:
#             obj = StockData(
#                 is_deleted=False,
#                 deleted_at=None,
#                 date=data[0],
#                 side=data[1],
#                 quantity=data[2],
#                 price=data[3],
#                 trade_num=data[4],
#                 company=StockMap.objects.get(name=data[5])
#             )
#             print(obj)
#             obj.save()
#         dfe = pd.DataFrame(columns=column)
#         outXLSX = pd.ExcelWriter(excel_read_file, engine='xlsxwriter')
#         dfe.to_excel(outXLSX, sheet_name='Data', index=False)
#         while True:
#             try:
#                 outXLSX.save()
#             except xlsxwriter.exceptions.FileCreateError as e:
#                 # For Python 3 use input() instead of raw_input().
#                 decision = input("Exception caught in workbook.close(): %s\n"
#                                  "Please close the file if it is open in Excel.\n"
#                                  "Try to write file again? [Y/n]: " % e)
#                 if decision != 'n':
#                     continue
#             break
#     return redirect(reverse('stocks:stockdata_list'))


def bulkCreateStockData(request):
    excel_read_file = r'C:\Users\raj\Desktop\my_trade.xlsx'
    # print(excel_read_file)
    workbook = openpyxl.load_workbook(filename=excel_read_file)
    sheet = workbook.active

    def side(data):
        data.strip()
        if data == 'Buy':
            return 1
        elif data == 'Sell':
            return -1

    for row in sheet.iter_rows(min_row=2, values_only=True):
        print(row)
        spread_date = row[0].strip()
        spread_time = row[9].strip()
        date_time = f'{spread_date} {spread_time}'
        parsed_date = datetime.strptime(date_time, "%d/%m/%Y %H:%M:%S")
        price = str_to_float(row[12].strip())
        comp_name = row[1].strip()
        obj = StockData(
            is_deleted=False,
            deleted_at=None,
            date=parsed_date,
            side=side(row[10]),
            quantity=int(float(row[11])),
            price=price,
            trade_num=int(row[8]),
            company=StockMap.objects.get(name=comp_name)
        )
        print(obj.__dict__)
        obj.save()

    while (sheet.max_row > 1):
        # this method removes the row 2
        sheet.delete_rows(2)
    workbook.save(excel_read_file)

    return redirect(reverse('stocks:stockdata_list'))


def export_data_csv(request):
    buffer = io.BytesIO()
    wb = xlsxwriter.Workbook(buffer)
    ws = wb.add_worksheet()

    stockdata_subqs = StockData.objects.filter(company=OuterRef("pk")).filter(company__is_portfolio_stock=True).values(
        'company').alias(sumzero=Sum(F('quantity') * F('side'))).filter(
        sumzero__gt=0).annotate(qty_sum=Sum(F('quantity') * F('side')),
                                price_sum=Sum(F('price') * F('side') * F('quantity')),
                                average_price=Sum(F('price') * F('side') * F('quantity')) / Sum(
                                    F('quantity') * F('side')))

    nsedata_subqs = NSEData.objects.filter(symbol=OuterRef("pk"))

    queryset = StockMap.objects.filter(is_portfolio_stock=True).annotate(
        qty_sum=Subquery(stockdata_subqs.values('qty_sum')),
        price_sum=Subquery(stockdata_subqs.values('price_sum')[:1]),
        average_price=Subquery(stockdata_subqs.values('average_price')[:1]),
        close=Subquery(nsedata_subqs.values('lastprice')[:1]),
        date=Subquery(nsedata_subqs.values('date')[:1]),
        w52_high=Subquery(nsedata_subqs.values('yearhigh')[:1]),
        w52_low=Subquery(nsedata_subqs.values('yearlow')[:1]),
        change=Subquery(nsedata_subqs.values('change')[:1]),
        pchange=Subquery(nsedata_subqs.values('pchange')[:1]),
        per_down=F('close') * 100 / F('w52_high') - 100,
        today_value=F('close') * F('qty_sum'),
        profit=F('today_value') - F('price_sum')
    ).order_by('name')
    # for item in data:
    #     print(item.name,item.profit)
    total_investment = 0
    profit_sum = 0

    for item in queryset:
        total_investment += item.price_sum
        profit_sum += item.profit

    queryset = queryset.annotate(
        total_investment=Cast(total_investment, output_field=DecimalField(max_digits=12, decimal_places=2)),
        profit_sum=Cast(profit_sum, output_field=DecimalField(max_digits=12, decimal_places=2)))
    # print(str(queryset.query))
    queryset = queryset.annotate(portweight=F('price_sum') * 100 / F('total_investment'),
                                 profit_percentage=F('today_value') * 100 / F('price_sum') - 100)

    datalist = queryset.values('name', 'nse_symbol', 'sector__sector', 'm_cap__market_cap', 'qty_sum',
                               'average_price', 'price_sum', 'today_value', 'profit', 'close', 'w52_high', 'w52_low',
                               'change', 'pchange', 'per_down', 'profit_percentage', 'portweight', 'date')

    # print(datalist)
    row = 0
    col = 0

    bold_1 = wb.add_format({'bold': 1, 'font_size': 12})

    column_data = wb.add_format({'font_size': 11})
    date = wb.add_format({'font_size': 11, 'num_format': 'dd/mm/yyyy'})
    keys = datalist[0].keys()

    for key in keys:
        ws.write(row, col, key, bold_1)
        col += 1

    column_setting = [{'header': key} for key in keys]

    ws.add_table(0, 0, len(datalist), len(keys) - 1,
                 {'columns': column_setting, 'autofilter': True,
                  'style': 'Table Style Light 11'})
    col = 0
    row = 1

    for index, rows in enumerate(datalist):

        for i, (k, v) in enumerate(rows.items(), start=1):
            money = wb.add_format({'font_size': 11, 'num_format': '₹#,##0.00', 'font_color': 'black'})
            if col == 0:
                ws.write(row, col, v, bold_1)
            elif col > 4 and col <= 7:
                ws.write(row, col, v, money)
            elif col == 8:
                ws.write_datetime(row, col, v, date)
            elif col >= 9 and col <= 11:
                ws.write(row, col, v, money)
            elif col == 15:
                if v < 0:
                    money.set_font_color('red')
                    ws.write(row, col, v, money)
                else:
                    ws.write(row, col, v, money)
            else:
                ws.write(row, col, v, column_data)
            col += 1
        col = 0
        row += 1

    ws.write(row, col, "total investment:")
    col_1 = col + 1
    ws.write(row, col_1, f'=SUM(F2:F{row})')
    row_1 = row + 1
    ws.write(row_1, col_1 - 1, "today value:")
    ws.write(row_1, col_1, f'=SUM(O2:O{row})')
    row_2 = row_1 + 1
    ws.write(row_2, col_1 - 1, "total profit:")
    ws.write(row_2, col_1, f'=SUM(O2:O{row})-SUM(F2:F{row})')

    row_3 = row_2 + 1
    ws.write(row_3, col_1 - 1, "profit %:")
    ws.write(row_3, col_1, f'=(SUM(O2:O{row})-SUM(F2:F{row}))*100/SUM(F2:F{row})')

    column = [key for key in keys]
    length_list = [len(x) for x in column]

    for i, width in enumerate(length_list):
        ws.set_column(i, i, width)

    while True:
        try:
            wb.close()
        except xlsxwriter.exceptions.FileCreateError as e:
            decision = input("Exception caught in workbook.close(): %s\n"
                             "Please close the file if it is open in Excel.\n"
                             "Try to write file again? [Y/n]: " % e)
            if decision != 'n':
                continue
        break
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f'report{datetime.now()}.xlsx')
