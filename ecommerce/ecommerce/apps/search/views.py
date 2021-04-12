from django.shortcuts import render
from .forms import SearchForm
# Create your views here.


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            products = Product.objects.filter(title__icontains=query)
            category = Category.objects.all()
            context = {
                'category':category,
                'products': products,
                'query': query
            }
            return render(request, './search.html', context)
        
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