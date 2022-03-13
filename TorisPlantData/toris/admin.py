from django.contrib import admin
from .models import *


class PlantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class PlantProductionAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'shift', 'operator_name', 'no_of_winderman', 'product_code',
                    'end_reading', 'start_reading', 'production', 'wastage']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(production_=(F('end_reading') - F('start_reading'))).order_by('date',
                                                                                                   'end_reading')
        return queryset

    def production(self, obj):
        return obj.production_

    production.admin_order_field = 'production_'


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_code', 'color_marking_on_bobin', 'tape_color', 'denier', 'gramage',
                    'tape_width', 'cutter_spacing', 'stock_of_bobin', 'streanth_per_tape_in_kg', 'elongation_percent',
                    'tenacity', 'pp_percent', 'filler_percent', 'shiner_percent', 'color_percent', 'tpt_percent',
                    'uv_percent', 'color_name']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_date', 'customer_name', 'product_code', 'order_qty', 'pi_number']


admin.site.register(Product, ProductAdmin)
admin.site.register(Plant, PlantAdmin)
admin.site.register(PlantProduction, PlantProductionAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Order, OrderAdmin)
