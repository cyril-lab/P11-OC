from django.shortcuts import render, get_object_or_404, redirect
from .models.product import Product
from .services.searchsubstitute import SearchSubstitute
from .services.favorite import Favorite


def homepage(request):
    """this function displays the home page"""
    return render(request, 'substitute/index.html')


def search(request):
    """this function allows you to search for products"""
    search = SearchSubstitute(request)
    if search.validate_search_product():
        search.get_product_substitute()
        context = {'product_substitute': search.product_substitute,
                   'product_img': search.product_img,
                   'search_product': search.query}
        return render(request, 'substitute/product.html', context)
    else:
        return render(request, 'substitute/no_result.html',
                      {'search_product': search.query})


def product(request, pk):
    """this function returns displays a particular product"""
    product_detail = get_object_or_404(Product, pk=pk)
    return render(request, 'substitute/product_detail.html',
                  {'product': product_detail})


def save_favorite(request, pk_prod):
    """this function allows you to save a favorite"""
    favorite = Favorite(request, pk_prod)
    if favorite.login_validate():
        favorite.saved_favorite()
        product = favorite.return_favorite_list()
        return render(request, 'substitute/favorite.html',
                      {'product': product})


def favorite(request):
    """this function is used to display the favorites"""
    favorite = Favorite(request)
    if favorite.login_validate():
        product = []
        product = favorite.return_favorite_list()
        return render(request, 'substitute/favorite.html',
                      {'product': product})
    else:
        return redirect('homepage')


def favorite_detail(request, pk):
    """this function is used to display the details of a favorite"""
    product_detail = get_object_or_404(Product, pk=pk)
    return render(request, 'substitute/favorite_detail.html',
                  {'product': product_detail})


def contact(request):
    """this function is used to display contact"""
    return render(request, 'substitute/contact.html')


def legal(request):
    """this function is used to display legal notice"""
    return render(request, 'substitute/legal.html')
