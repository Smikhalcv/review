from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm

def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    if 'reviewed_products' not in request.session:
        request.session['reviewed_products'] = {}     # create list into session
    form = ReviewForm
    context = {
        'form': form,
        'product': product,
        'reviews': Product.objects.get(id=pk).review_set.all()
    }
    if pk in request.session['reviewed_products']:# if id product is in the session list, then output massage
        del context['form']
        context['is_review_exist'] = True
    else: # if id product is not in the session list, add commit in the db
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data['text']
                Review.objects.create(text=data, product=Product.objects.get(id=pk))
                del context['form']
                request.session['reviewed_products'].append(pk)
                request.session.save()


    return render(request, template, context)
