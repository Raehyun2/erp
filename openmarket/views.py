from django.shortcuts import render


def market_page(request):
    return render(request, 'openmarket/market_page.html')

def auction(request):
    return render(request, 'openmarket/auction.html')

def market_11(request):
    return render(request, 'openmarket/market_11.html')