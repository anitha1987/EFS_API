from django.contrib import admin
from .models import Customer, Investment, Stock, Mutualfund

class CustomerList(admin.ModelAdmin):
    list_display = ('cust_number', 'name', 'city', 'cell_phone')
    list_filter = ('cust_number', 'name', 'city')
    search_fields = ('cust_number', 'name')
    ordering = ['cust_number']

class InvestmentList(admin.ModelAdmin):
    list_display = ('customer', 'category', 'description', 'recent_value')
    list_filter = ('customer', 'category')
    search_fields = ('customer', 'category')
    ordering = ['customer']

class StockList(admin.ModelAdmin):
    list_display = ('customer','symbol', 'name', 'shares', 'purchase_price')
    list_filter = ('customer','symbol', 'name')
    search_fields = ('customer','symbol', 'name')
    ordering = ['customer']


class MutualfundList(admin.ModelAdmin):
    list_display = ('customer', 'bondtype', 'description', 'recent_value')
    list_filter = ('customer', 'bondtype')
    search_fields = ('customer', 'bondtype')
    ordering = ['customer']


admin.site.register(Customer, CustomerList)
admin.site.register(Investment, InvestmentList)
admin.site.register(Stock, StockList)
admin.site.register(Mutualfund, MutualfundList)
