from substitute.models.product import Product
from substitute.models.user import User


class Favorite:
    def __init__(self, request, pk_prod=None):
        self.request = request
        self.pk_prod = pk_prod

    def login_validate(self):
        if self.request.user.is_authenticated:
            return True

    def saved_favorite(self):
        pk_user = User.objects.get(pk=self.request.user.pk)
        pk_product = Product.objects.get(pk=self.pk_prod)
        pk_product.favorite.add(pk_user)

    def return_favorite_list(self):
        favorite = []
        for p in Product.objects.filter(favorite__id=self.request.user.pk):
            favorite.append([p.pk, p.name, p.image_url, p.nutriscore])
        return favorite
