from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from django.template.loader import render_to_string
from django.conf import settings



def home(request):
   return render(request, 'portfolio/home.html',
                 {'portfolio': home})


@login_required
def customer_new(request):
   if request.method == "POST":
       form = CustomerForm(request.POST)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.created_date = timezone.now()
           customer.save()
           customers = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customers})
   else:
       form = CustomerForm()
       # print("Else")
   return render(request, 'portfolio/customer_new.html', {'form': form})

@login_required
def customer_list(request):
   customer = Customer.objects.filter(created_date__lte=timezone.now())
   return render(request, 'portfolio/customer_list.html',
                 {'customers': customer})


@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           # customer = Customer.objects.filter(created_date__lte=timezone.now())
           return HttpResponseRedirect('/customer_list/')

   else:
       form = CustomerForm(instance=customer)
   return render(request, 'portfolio/customer_edit.html', {'form': form})


@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('portfolio:customer_list')

@login_required
def investment_list(request):
   # investments = Investment.objects.filter(acquired_date__lte=timezone.now())
   investments = Investment.objects.all()
   return render(request, 'portfolio/investment_list.html', {'investments': investments})

@login_required
def investment_new(request):
   if request.method == "POST":
       form = InvestmentForm(request.POST)
       if form.is_valid():
           investment = form.save(commit=False)
           investment.created_date = timezone.now()
           investment.save()
           return redirect('portfolio:investment_list')
   else:
       form = InvestmentForm()
       # print("Else")
   return render(request, 'portfolio/investment_new.html', {'form': form})


@login_required
def investment_edit(request, pk):
   investment = get_object_or_404(Investment, pk=pk)
   if request.method == "POST":
       form = InvestmentForm(request.POST, instance=investment)
       if form.is_valid():
           investment = form.save()
           # investment.customer = investment.id
           investment.updated_date = timezone.now()
           investment.save()
           return redirect('portfolio:investment_list')
   else:
       # print("else")
       form = InvestmentForm(instance=investment)
   return render(request, 'portfolio/investment_edit.html', {'form': form})


@login_required
def investment_delete(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    investment.delete()
    return redirect('portfolio:investment_list')

@login_required
def stock_list(request):
   stocks = Stock.objects.all()
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})


@login_required
def stock_new(request):
   if request.method == "POST":
       form = StockForm(request.POST)
       if form.is_valid():
           stock = form.save(commit=False)
           stock.created_date = timezone.now()
           stock.save()
           return redirect('portfolio:stock_list')
   else:
       form = StockForm()
       # print("Else")
   return render(request, 'portfolio/stock_new.html', {'form': form})


@login_required
def stock_edit(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   if request.method == "POST":
       form = StockForm(request.POST, instance=stock)
       if form.is_valid():
           stock = form.save()
           # stock.customer = stock.id
           stock.updated_date = timezone.now()
           stock.save()
           return redirect('portfolio:stock_list')
   else:
       # print("else")
       form = StockForm(instance=stock)
   return render(request, 'portfolio/stock_edit.html', {'form': form})


@login_required
def stock_delete(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   stock.delete()
   return redirect('portfolio:stock_list')

def contact(request):
    form_class = ContactForm

    return render(request, 'portfolio/contact.html', {
        'form': form_class,
    })

def about(request):
 return render(request, 'portfolio/about.html', {'portfolio': about})

#Mutual Funds

@login_required
def mutualfund_list(request):
   mutualfunds = Mutualfund.objects.all()
   return render(request, 'portfolio/mutualfund_list.html', {'mutualfunds': mutualfunds})

@login_required
def mutualfund_new(request):
   if request.method == "POST":
       form = MutualfundForm(request.POST)
       if form.is_valid():
           mutualfund = form.save(commit=False)
           mutualfund.created_date = timezone.now()
           mutualfund.save()
           return redirect('portfolio:mutualfund_list')
   else:
       form = MutualfundForm()
       # print("Else")
   return render(request, 'portfolio/mutualfund_new.html', {'form': form})


@login_required
def mutualfund_edit(request, pk):
   mutualfund = get_object_or_404(Mutualfund, pk=pk)
   if request.method == "POST":
       form = MutualfundForm(request.POST, instance=mutualfund)
       if form.is_valid():
           mutualfund = form.save()
           mutualfund.updated_date = timezone.now()
           mutualfund.save()
           return redirect('portfolio:mutualfund_list')
   else:
       # print("else")
       form = MutualfundForm(instance=mutualfund)
   return render(request, 'portfolio/mutualfund_edit.html', {'form': form})


@login_required
def mutualfund_delete(request, pk):
    mutualfund = get_object_or_404(Mutualfund, pk=pk)
    mutualfund.delete()
    return redirect('portfolio:mutualfund_list')

@login_required
def portfolio(request,pk):
   customer = get_object_or_404(Customer, pk=pk)
   customers = Customer.objects.filter(created_date__lte=timezone.now())
   investments =Investment.objects.filter(customer=pk)
   stocks = Stock.objects.filter(customer=pk)
   mutualfunds = Mutualfund.objects.filter(customer=pk)

   sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
   sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))

   sum_acquired_value_mf = Mutualfund.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
   sum_recent_value_mf = Mutualfund.objects.filter(customer=pk).aggregate(Sum('recent_value'))

   # overall_investment_results = sum_recent_value-sum_acquired_value
   # Initialize the value of the stocks
   sum_current_stocks_value = 0
   sum_of_initial_stock_value = 0

   # Loop through each stock and add the value to the total
   for stock in stocks:
        sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()

   portfolio_initial_investments = float(sum_of_initial_stock_value) + \
                                   float(sum_acquired_value['acquired_value__sum']) + \
                                   float(sum_acquired_value_mf['acquired_value__sum'])
   portfolio_current_investments = float(sum_current_stocks_value) + \
                                   float(sum_recent_value['recent_value__sum']) + \
                                   float(sum_recent_value_mf['recent_value__sum'])

   return render(request, 'portfolio/portfolio.html', {'customers': customers, 'investments': investments,
                                                       'stocks': stocks, 'mutualfunds': mutualfunds,
                                                       'sum_acquired_value': sum_acquired_value['acquired_value__sum'],
                                                       'sum_recent_value': sum_recent_value['recent_value__sum'],
                                                       'sum_acquired_value_mf': sum_acquired_value_mf['acquired_value__sum'],
                                                       'sum_recent_value_mf': sum_recent_value_mf['recent_value__sum'],
                                                       'sum_of_current_stocks_value': float(sum_current_stocks_value),
                                                       'sum_of_initial_stocks_value': float(sum_of_initial_stock_value),
                                                       'portfolio_initial_investments': portfolio_initial_investments,
                                                       'portfolio_current_investments': portfolio_current_investments,
                                                      })


# List at the end of the views.py
# Lists all customers
class CustomerList(APIView):

    def get(self,request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)


