from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    """
    Creates products
    """
    def handle(self, *args, **options):
        self.stdout.write('Create products')
        products_names = [
            'Laptop',
            'Desktop',
            'Smartphone'
        ]
        db_process = 'created'
        for product_name in products_names:
            product, created = Product.objects.get_or_create(name=product_name)
            if not created:
                db_process = "retrived from database"
            self.stdout.write(f'Product {product.name, created} {db_process}')
        self.stdout.write(self.style.SUCCESS(f"Products created"))