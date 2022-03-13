from django.contrib import admin

# Register your models here.
from .models import StockMap,StockData,HistoricalData,Sector,MarketCap

class StockMapAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','nse_symbol','yahoo_symbol','moneycontrol_symbol','m_cap','sector','is_portfolio_stock']
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['nse_symbol']}),
        (None, {'fields': ['yahoo_symbol']}),
        (None, {'fields': ['moneycontrol_symbol']}),
        (None, {'fields': ['m_cap']}),
        (None, {'fields': ['sector']}),
        (None, {'fields': ['is_portfolio_stock']}),
    ]
class StockDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'company','date','side','quantity','price','trade_num']
class HistoricalDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'company','date','open','high','low','close','adj_close','volume']


admin.site.register(StockMap,StockMapAdmin)
admin.site.register(StockData,StockDataAdmin)
admin.site.register(HistoricalData,HistoricalDataAdmin)
admin.site.register(Sector)
admin.site.register(MarketCap)