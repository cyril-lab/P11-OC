from django.contrib.postgres.search import SearchQuery, SearchVector
from substitute.models.product import Product


class SearchSubstitute:
    def __init__(self, request):
        self.request = request
        self.product_substitute = []
        self.product_img = ""
        self.query = self._query_get_product_name()
        self.search_product = self._save_search_product()

    def _query_get_product_name(self):
        return self.request.GET['name_product']

    def _save_search_product(self):
        return Product.objects.annotate(
            search=SearchVector('name'))\
            .filter(search=SearchQuery(self.query))

    def validate_search_product(self):
        if len(self.search_product) != 0:
            return True
        else:
            return False

    def get_product_substitute(self):
        product = self.search_product[0]
        product_category = str(product.category_id)
        product_pk = str(product.id)
        self.product_img = product.image_url
        search_substitute = Product.objects.annotate(
            search=SearchVector('category_id'))\
            .filter(search=product_category).exclude(id=product_pk)
        for p in search_substitute:
            self.product_substitute.append(
                [p.pk, p.name, p.image_url, p.nutriscore])
        return self.product_substitute
