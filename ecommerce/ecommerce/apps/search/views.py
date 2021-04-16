from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchForm
from django.http.response import HttpResponseRedirect
from apps.product.models import Category, Product
import json
from apps.order.models import ShopCart



def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            current_user = request.user
            image_default = "user.png"
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            total = 0
            for rs in shopcart:
                total += rs.product.price * rs.quantity
            quantity = 0
            for rs in shopcart:
                quantity += rs.quantity
            query = form.cleaned_data['query']
            products = Product.objects.filter(title__icontains=query)
            category = Category.objects.all()
            context = {
                'category':category,
                'products': products,
                'query': query,
                'total': total,
                'quantity': quantity,
            }
            
            return render(request, 'search/search.html', context)
        
    return HttpResponseRedirect('/search')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)