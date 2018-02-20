from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from django.http import HttpResponse
from currency_converter import CurrencyConverter


from .forms import *
from .models import *

currency = 'USD'
value = 0
toReturn = None
call_type = 0

def eur(request):
    global currency, call_type, value
    currency = 'EUR'
    call_type = 99
    portfolio(request, value)
    call_type = 0
    return toReturn

def cad(request):
    global currency, value, call_type
    currency = 'CAD'
    call_type = 99
    portfolio(request,value)
    call_type = 0
    return toReturn

def inr(request):
    global currency, value, call_type
    currency = 'INR'
    call_type = 99
    portfolio(request,value)
    call_type = 0
    return toReturn

def home(request):
    return render(request, 'portfolio/home.html',
                  {'portfolio': home})


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
            customer = Customer.objects.filter(created_date__lte=timezone.now())
            return render(request, 'portfolio/customer_list.html',
                          {'customers': customer})
    else:
        # edit
        form = CustomerForm(instance=customer)
    return render(request, 'portfolio/customer_edit.html', {'form': form})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('portfolio:customer_list')


@login_required
def stock_list(request):
    stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
    return render(request, 'portfolio/stock_list.html', {'stocks': stocks})


@login_required
def stock_new(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.created_date = timezone.now()
            stock.save()
            stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
            return render(request, 'portfolio/stock_list.html',
                          {'stocks': stocks})
    else:
        form = StockForm()
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
            stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
            return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
    else:
        # print("else")
        form = StockForm(instance=stock)
    return render(request, 'portfolio/stock_edit.html', {'form': form})


@login_required
def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    stock.delete()
    stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
    return render(request, 'portfolio/stock_list.html', {'stocks': stocks})


@login_required
def investment_list(request):
    investments = Investment.objects.filter(acquired_date__lte=timezone.now())
    return render(request, 'portfolio/investment_list.html', {'investments': investments})


@login_required
def investment_new(request):
    if request.method == "POST":
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.created_date = timezone.now()
            investment.save()
            investments = Investment.objects.filter(acquired_date__lte=timezone.now())
            return render(request, 'portfolio/investment_list.html',
                          {'investments': investments})
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
            investments = Investment.objects.filter(acquired_date__lte=timezone.now())
            return render(request, 'portfolio/investment_list.html', {'investments': investments})
    else:
        # print("else")
        form = InvestmentForm(instance=investment)
    return render(request, 'portfolio/investment_edit.html', {'form': form})


@login_required
def investment_delete(request, pk):
    investment = get_object_or_404(Stock, pk=pk)
    investment.delete()
    investments = Investment.objects.filter(acquired_date__lte=timezone.now())
    return render(request, 'portfolio/investment_list.html', {'investments': investments})


@login_required
def mutualfund_list(request):
    mutualfunds = MutualFunds.objects.filter(start_date__lte=timezone.now())
    return render(request, 'portfolio/mutualfund_list.html', {'mutualfunds': mutualfunds})


@login_required
def mutualfund_new(request):
    if request.method == "POST":
        form = MutualFundForm(request.POST)
        if form.is_valid():
            mutualfund = form.save(commit=False)
            mutualfund.start_date = timezone.now()
            mutualfund.save()
            mutualfunds = MutualFunds.objects.filter(start_date__lte=timezone.now())
            return render(request, 'portfolio/mutualfund_list.html',
                          {'mutualfunds': mutualfunds})
    else:
        form = MutualFundForm()
        # print("Else")
    return render(request, 'portfolio/mutualfund_new.html', {'form': form})


@login_required
def mutualfund_edit(request, pk):
    mutualfund = get_object_or_404(MutualFunds, pk=pk)
    if request.method == "POST":
        form = MutualFundForm(request.POST, instance=mutualfund)
        if form.is_valid():
            mutualfund = form.save()
            # investment.customer = investment.id
            mutualfund.updated_date = timezone.now()
            mutualfund.save()
            mutualfunds = MutualFunds.objects.filter(start_date__lte=timezone.now())
            return render(request, 'portfolio/mutualfund_list.html', {'mutualfunds': mutualfunds})
    else:
        # print("else")
        form = MutualFundForm(instance=mutualfund)
    return render(request, 'portfolio/mutualfund_edit.html', {'form': form})


@login_required
def mutualfund_delete(request, pk):
    mutualfund = get_object_or_404(Stock, pk=pk)
    mutualfund.delete()
    mutualfunds = MutualFunds.objects.filter(start_date__lte=timezone.now())
    return render(request, 'portfolio/mutualfund_list.html', {'mutualfunds': mutualfunds})

def stock_Converter(stocks, curr):
     c = CurrencyConverter()
     for stock in stocks:
         if curr == 'EUR':
             stock.purchase_price = c.convert(stock.purchase_price, 'USD', 'EUR')
             stock.current_stock_price = c.convert(stock.current_stock_price(), 'USD', 'EUR')
             stock.stock_profit = c.convert(stock.stock_profit, 'USD', 'EUR')
         elif curr == 'CAD':
             stock.purchase_price = c.convert(stock.purchase_price, 'USD', 'CAD')
             stock.current_stock_price = c.convert(stock.current_stock_price(), 'USD', 'CAD')
             stock.stock_profit = c.convert(stock.stock_profit, 'USD', 'CAD')
         elif curr == 'INR':
             stock.purchase_price = c.convert(stock.purchase_price, 'USD', 'INR')
             stock.current_stock_price = c.convert(stock.current_stock_price(), 'USD', 'INR')
             stock.stock_profit = c.convert(stock.stock_profit, 'USD', 'INR')
     return stocks


@login_required
def portfolio(request, pk):
    global value,currency, toReturn
    customer = get_object_or_404(Customer, pk=pk)
    value = pk
    c = CurrencyConverter()

    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
    sum_current_stocks_value = 0
    sum_of_initial_stock_value = 0
    for stock in stocks:
        sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()
    if call_type == 0:
        return render(request, 'portfolio/portfolio.html', {'customers': customers, 'investments': investments,
                        	'stocks': stocks,
                        	'sum_acquired_value': float(sum_acquired_value['acquired_value__sum']),
                        	'sum_recent_value': float(sum_recent_value['recent_value__sum']),
                        	'sum_current_stocks_value': float(sum_current_stocks_value),
                        	'sum_of_initial_stock_value': float(sum_of_initial_stock_value),
                            'portfolio_initial_investments': float(sum_of_initial_stock_value)+float(sum_acquired_value['acquired_value__sum']),
                            'portfolio_current_investments': float(sum_current_stocks_value)+float(sum_recent_value['recent_value__sum']),
                            'grand_total': -(float(sum_of_initial_stock_value)+float(sum_acquired_value['acquired_value__sum']))+(float(sum_current_stocks_value)+float(sum_recent_value['recent_value__sum'])),
                            'results': float(sum_current_stocks_value)-float(sum_of_initial_stock_value),
                            'investment_results': float(sum_recent_value['recent_value__sum'])-float(sum_acquired_value['acquired_value__sum']),
                            })
    elif currency == 'EUR':
        toReturn = render(request, 'portfolio/portfolio.html', {'customers': customers, 'investments': investments,
                                                            'stocks': stock_Converter(stocks, currency),
                                                            'sum_acquired_value': float(
                                                                c.convert(sum_acquired_value['acquired_value__sum'], 'USD', 'EUR')),
                                                            'sum_recent_value': float(
                                                                c.convert(sum_recent_value['recent_value__sum'], 'USD', 'EUR')),
                                                            'sum_current_stocks_value': float(c.convert(sum_current_stocks_value, 'USD', 'EUR')),
                                                            'sum_of_initial_stock_value': float(
                                                                c.convert( sum_of_initial_stock_value, 'USD', 'EUR')),
                                                            'portfolio_initial_investments': float(c.convert(sum_of_initial_stock_value, 'USD', 'EUR')) + float(
                                                                c.convert(sum_acquired_value['acquired_value__sum'], 'USD', 'EUR')),
                                                            'portfolio_current_investments': float(c.convert(sum_current_stocks_value, 'USD', 'EUR')) + float(c.convert(sum_recent_value['recent_value__sum'], 'USD', 'EUR')),
                                                            'grand_total': (float(c.convert(sum_of_initial_stock_value, 'USD', 'EUR'))) +
                                                            float(c.convert(sum_acquired_value['acquired_value__sum'], 'USD', 'EUR')) +
                                                                           float(c.convert(sum_current_stocks_value, 'USD', 'EUR')) + float(
                                                                               c.convert(sum_recent_value['recent_value__sum'], 'USD', 'EUR')),
                                                            'results': float(c.convert(sum_current_stocks_value, 'USD', 'EUR')) - float(
                                                                c.convert(sum_of_initial_stock_value, 'USD', 'EUR')),
                                                            'investment_results': float(
                                                                c.convert(sum_recent_value['recent_value__sum'], 'USD', 'EUR') - float(
                                                                c.convert(sum_acquired_value['acquired_value__sum'], 'USD', 'EUR'))),})


    elif currency == 'CAD':
        toReturn = render(request, 'portfolio/portfolio.html', {'customers': customers, 'investments': investments,
                                                            'stocks': stock_Converter(stocks, currency),
                                                            'sum_acquired_value': float(
                                                                c.convert(sum_acquired_value['acquired_value__sum'], 'USD', 'CAD')),
                                                            'sum_recent_value': float(
                                                                c.convert(sum_recent_value['recent_value__sum'], 'USD', 'CAD')),
                                                            'sum_current_stocks_value': float(c.convert(sum_current_stocks_value, 'USD', 'CAD')),
                                                            'sum_of_initial_stock_value': float(
                                                                c.convert( sum_of_initial_stock_value, 'USD', 'CAD')),
                                                            'portfolio_initial_investments': float(c.convert(sum_of_initial_stock_value, 'USD', 'CAD')) + float(
                                                                c.convert(sum_acquired_value['acquired_value__sum'], 'USD', 'CAD')),
                                                            'portfolio_current_investments': float(c.convert(sum_current_stocks_value, 'USD', 'CAD')
                                                                ) + float(c.convert(sum_recent_value['recent_value__sum'], 'USD', 'CAD')),
                                                            'grand_total': (float(c.convert(sum_of_initial_stock_value, 'USD', 'CAD'))) +
                                                            float(c.convert(sum_acquired_value['acquired_value__sum'], 'USD', 'CAD')) +
                                                                           float(c.convert(sum_current_stocks_value, 'USD', 'CAD')) + float(
                                                                               c.convert(sum_recent_value['recent_value__sum'], 'USD', 'CAD')),
                                                            'results': float(c.convert(sum_current_stocks_value, 'USD', 'CAD')) - float(
                                                                c.convert(sum_of_initial_stock_value, 'USD', 'CAD')),
                                                            'investment_results': float(
                                                                c.convert(sum_recent_value['recent_value__sum'], 'USD', 'CAD') - float(
                                                                c.convert(sum_acquired_value['acquired_value__sum'], 'USD', 'CAD'))),})

    elif currency == 'INR':
        toReturn = render(request, 'portfolio/portfolio.html', {'customers': customers, 'investments': investments,
                                                            'stocks': stock_Converter(stocks, currency),
                                                            'sum_acquired_value': float(
                                                                c.convert(sum_acquired_value['acquired_value__sum'], 'USD', 'INR')),
                                                            'sum_recent_value': float(
                                                                c.convert(sum_recent_value['recent_value__sum'], 'USD', 'INR')),
                                                            'sum_current_stocks_value': float(c.convert(sum_current_stocks_value, 'USD', 'INR')),
                                                            'sum_of_initial_stock_value': float(
                                                                c.convert( sum_of_initial_stock_value, 'USD', 'INR')),
                                                            'portfolio_initial_investments': float(c.convert(sum_of_initial_stock_value, 'USD', 'INR')) + float(
                                                                c.convert(sum_acquired_value['acquired_value__sum'], 'USD', 'INR')),
                                                            'portfolio_current_investments': float(c.convert(sum_current_stocks_value, 'USD', 'INR')
                                                                ) + float(c.convert(sum_recent_value['recent_value__sum'], 'USD', 'INR')),
                                                            'grand_total': (float(c.convert(sum_of_initial_stock_value, 'USD', 'INR'))) +
                                                            float(c.convert(sum_acquired_value['acquired_value__sum'], 'USD', 'INR')) +
                                                                           float(c.convert(sum_current_stocks_value, 'USD', 'INR')) + float(
                                                                               c.convert(sum_recent_value['recent_value__sum'], 'USD', 'INR')),
                                                            'results': float(c.convert(sum_current_stocks_value, 'USD', 'INR')) - float(
                                                                c.convert(sum_of_initial_stock_value, 'USD', 'INR')),
                                                            'investment_results': float(
                                                                c.convert(sum_recent_value['recent_value__sum'], 'USD', 'INR') - float(
                                                                c.convert(sum_acquired_value['acquired_value__sum'], 'USD', 'INR'))),})



    return render(request, 'portfolio/portfolio.html', {'customers': customers, 'investments': investments,
                                                        'stocks': stocks,
                                                        'sum_acquired_value': float(
                                                            sum_acquired_value['acquired_value__sum']),
                                                        'sum_recent_value': float(
                                                            sum_recent_value['recent_value__sum']),
                                                        'sum_current_stocks_value': float(sum_current_stocks_value),
                                                        'sum_of_initial_stock_value': float(sum_of_initial_stock_value),
                                                        'portfolio_initial_investments': float(
                                                            sum_of_initial_stock_value) + float(
                                                            sum_acquired_value['acquired_value__sum']),
                                                        'portfolio_current_investments': float(
                                                            sum_current_stocks_value) + float(
                                                            sum_recent_value['recent_value__sum']),
                                                        'grand_total': -(float(sum_of_initial_stock_value) + float(
                                                            sum_acquired_value['acquired_value__sum'])) + (
                                                                       float(sum_current_stocks_value) + float(
                                                                           sum_recent_value['recent_value__sum'])),
                                                        'results': float(sum_current_stocks_value) - float(
                                                            sum_of_initial_stock_value),
                                                        'investment_results': float(
                                                            sum_recent_value['recent_value__sum']) - float(
                                                            sum_acquired_value['acquired_value__sum']),
                                                        })



class CustomerList(APIView):

    def get(self,request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)
