from django.contrib.postgres.search import SearchQuery, SearchVector
from django.utils.datastructures import MultiValueDictKeyError
from substitute.models.product import Product


class SearchSubstitute:
    def __init__(self, request):
        self.request = request
        self.product_substitute = []
        self.product_img = ""
        self.query = self._query_get_product_name()
        self.search_product = self._save_search_product()
        self.nutriscore = self._query_get_nutriscore()
        self.vote = self._query_get_vote()

    def _query_get_product_name(self):
        return self.request.GET['name_product']

    def _query_get_nutriscore(self):
        try:
            return self.request.GET['nutriscore']
        except MultiValueDictKeyError:
            return 'no_filter'

    def _query_get_vote(self):
        try:
            return self.request.GET['vote']
        except MultiValueDictKeyError:
            return 'no_filter'

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
        if self.nutriscore != 'no_filter' and self.vote != 'no_filter':
            search_substitute = Product.objects\
                .filter(category_id=product_category) \
                .exclude(id=product_pk) \
                .filter(nutriscore=self.nutriscore) \
                .order_by(self.vote).reverse()
        elif self.nutriscore != 'no_filter' and self.vote == 'no_filter':
            search_substitute = Product.objects \
                .filter(category_id=product_category) \
                .exclude(id=product_pk) \
                .filter(nutriscore=self.nutriscore)
        elif self.nutriscore == 'no_filter' and self.vote != 'no_filter':
            search_substitute = Product.objects \
                .filter(category_id=product_category) \
                .exclude(id=product_pk) \
                .order_by('nutriscore') \
                .order_by(self.vote).reverse()
        else:
            search_substitute = Product.objects \
                .filter(category_id=product_category) \
                .exclude(id=product_pk) \
                .order_by('nutriscore')

        for p in search_substitute:
            self.product_substitute.append(
                [p.pk, p.name, p.image_url, p.nutriscore, p.like, p.dislike])
        return self.product_substitute
