from django.core.management.base import BaseCommand
from substitute.models import Category, Product
from substitute.services.saveproductdatabase import SaveProductDatabase


class Command(BaseCommand):
    help = 'Download data from openfoodfacts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='truncate database',
        )

    def handle(self, *args, **options):
        if options['delete']:
            Category.objects.all().delete()
            Product.objects.all().delete()
            self.stdout.write('Données supprimées')
        else:
            application = SaveProductDatabase('Snack', 'Desserts')
            application.main()
