from django.core.management.base import BaseCommand
from app_inventory.models import LumberCategory, LumberProduct, Inventory


class Command(BaseCommand):
    help = 'Populate the database with sample lumber products'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {
                'name': 'Hardwood',
                'description': 'Premium hardwood lumber for fine furniture and flooring'
            },
            {
                'name': 'Softwood',
                'description': 'Cost-effective softwood for general construction and framing'
            },
            {
                'name': 'Engineered',
                'description': 'Engineered lumber for structural applications'
            },
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = LumberCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat.name}'))
            else:
                self.stdout.write(f'Category already exists: {cat.name}')

        # Create sample products
        products_data = [
            {
                'name': '2x4 Pressure Treated Pine',
                'category': 'Softwood',
                'thickness': 1.5,
                'width': 3.5,
                'length': 8,
                'price_per_board_foot': 5.50,
                'price_per_piece': 14.99,
                'sku': 'PTP-2x4-8'
            },
            {
                'name': '2x6 Pressure Treated Pine',
                'category': 'Softwood',
                'thickness': 1.5,
                'width': 5.5,
                'length': 10,
                'price_per_board_foot': 6.75,
                'price_per_piece': 34.99,
                'sku': 'PTP-2x6-10'
            },
            {
                'name': '1x6 Oak Hardwood',
                'category': 'Hardwood',
                'thickness': 0.75,
                'width': 5.5,
                'length': 8,
                'price_per_board_foot': 18.50,
                'price_per_piece': 49.99,
                'sku': 'OAK-1x6-8'
            },
            {
                'name': '1x8 Walnut Hardwood',
                'category': 'Hardwood',
                'thickness': 0.75,
                'width': 7.25,
                'length': 10,
                'price_per_board_foot': 28.00,
                'price_per_piece': 129.99,
                'sku': 'WAL-1x8-10'
            },
            {
                'name': '2x12 LVL Beam',
                'category': 'Engineered',
                'thickness': 1.75,
                'width': 11.875,
                'length': 16,
                'price_per_board_foot': 8.25,
                'price_per_piece': 159.99,
                'sku': 'LVL-2x12-16'
            },
            {
                'name': '1x12 Pine Common',
                'category': 'Softwood',
                'thickness': 0.75,
                'width': 11.25,
                'length': 12,
                'price_per_board_foot': 7.50,
                'price_per_piece': 79.99,
                'sku': 'PIN-1x12-12'
            },
            {
                'name': '4x4 Pressure Treated Cedar',
                'category': 'Softwood',
                'thickness': 3.5,
                'width': 3.5,
                'length': 8,
                'price_per_board_foot': 9.99,
                'price_per_piece': 44.99,
                'sku': 'PTC-4x4-8'
            },
            {
                'name': '2x8 Engineered Joist',
                'category': 'Engineered',
                'thickness': 1.75,
                'width': 7.25,
                'length': 14,
                'price_per_board_foot': 7.00,
                'price_per_piece': 89.99,
                'sku': 'ENG-2x8-14'
            },
        ]

        created_count = 0
        for prod_data in products_data:
            category = categories[prod_data.pop('category')]
            
            product, created = LumberProduct.objects.get_or_create(
                sku=prod_data['sku'],
                defaults={**prod_data, 'category': category}
            )
            
            if created:
                # Create inventory for new product
                inventory, _ = Inventory.objects.get_or_create(
                    product=product,
                    defaults={
                        'quantity_pieces': 100 if created_count % 3 != 0 else 15,  # Vary stock levels
                        'total_board_feet': product.board_feet * (100 if created_count % 3 != 0 else 15)
                    }
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created product: {product.name} with {inventory.quantity_pieces} pcs in stock')
                )
                created_count += 1
            else:
                self.stdout.write(f'Product already exists: {product.name}')

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} new products!')
        )
