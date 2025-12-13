import os
import requests
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from app_inventory.models import LumberCategory, LumberProduct, Inventory
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate lumber products with images'

    def handle(self, *args, **options):
        # Ensure categories exist
        categories = {
            'Hardwood': 'Premium hardwood lumber for fine woodworking',
            'Softwood': 'Construction grade softwood lumber',
            'Engineered': 'Engineered lumber and composite materials',
        }

        for cat_name, desc in categories.items():
            LumberCategory.objects.get_or_create(
                name=cat_name,
                defaults={'description': desc}
            )

        # Product data with image URLs (using Pexels for reliable wood lumber images)
        products_data = [
            # Hardwood
            {
                'name': 'Red Oak 1x4x8',
                'sku': 'RO-1x4-8',
                'category': 'Hardwood',
                'thickness': Decimal('0.75'),
                'width': Decimal('3.50'),
                'length': Decimal('8'),
                'price_per_board_foot': Decimal('8.50'),
                'price_per_piece': Decimal('18.00'),
                'image_url': 'https://images.pexels.com/photos/172289/pexels-photo-172289.jpeg',
                'inventory_qty': 45,
            },
            {
                'name': 'White Oak 1x6x8',
                'sku': 'WO-1x6-8',
                'category': 'Hardwood',
                'thickness': Decimal('0.75'),
                'width': Decimal('5.50'),
                'length': Decimal('8'),
                'price_per_board_foot': Decimal('12.75'),
                'price_per_piece': Decimal('35.00'),
                'image_url': 'https://images.pexels.com/photos/163999/pexels-photo-163999.jpeg',
                'inventory_qty': 32,
            },
            {
                'name': 'Maple 1x8x10',
                'sku': 'MAP-1x8-10',
                'category': 'Hardwood',
                'thickness': Decimal('0.75'),
                'width': Decimal('7.50'),
                'length': Decimal('10'),
                'price_per_board_foot': Decimal('15.00'),
                'price_per_piece': Decimal('95.00'),
                'image_url': 'https://images.pexels.com/photos/172288/pexels-photo-172288.jpeg',
                'inventory_qty': 28,
            },
            {
                'name': 'Walnut 2x4x8',
                'sku': 'WAL-2x4-8',
                'category': 'Hardwood',
                'thickness': Decimal('1.50'),
                'width': Decimal('3.50'),
                'length': Decimal('8'),
                'price_per_board_foot': Decimal('18.00'),
                'price_per_piece': Decimal('42.00'),
                'image_url': 'https://images.pexels.com/photos/172296/pexels-photo-172296.jpeg',
                'inventory_qty': 22,
            },
            {
                'name': 'Ash 1x10x12',
                'sku': 'ASH-1x10-12',
                'category': 'Hardwood',
                'thickness': Decimal('0.75'),
                'width': Decimal('9.50'),
                'length': Decimal('12'),
                'price_per_board_foot': Decimal('10.50'),
                'price_per_piece': Decimal('75.00'),
                'image_url': 'https://images.pexels.com/photos/301378/pexels-photo-301378.jpeg',
                'inventory_qty': 35,
            },
            # Softwood
            {
                'name': 'Pine 2x4x8',
                'sku': 'PIN-2x4-8',
                'category': 'Softwood',
                'thickness': Decimal('1.50'),
                'width': Decimal('3.50'),
                'length': Decimal('8'),
                'price_per_board_foot': Decimal('3.25'),
                'price_per_piece': Decimal('7.50'),
                'image_url': 'https://images.pexels.com/photos/518245/pexels-photo-518245.jpeg',
                'inventory_qty': 128,
            },
            {
                'name': 'Spruce 2x6x10',
                'sku': 'SPR-2x6-10',
                'category': 'Softwood',
                'thickness': Decimal('1.50'),
                'width': Decimal('5.50'),
                'length': Decimal('10'),
                'price_per_board_foot': Decimal('2.85'),
                'price_per_piece': Decimal('14.50'),
                'image_url': 'https://images.pexels.com/photos/172289/pexels-photo-172289.jpeg',
                'inventory_qty': 95,
            },
            {
                'name': 'Fir 4x4x8',
                'sku': 'FIR-4x4-8',
                'category': 'Softwood',
                'thickness': Decimal('3.50'),
                'width': Decimal('3.50'),
                'length': Decimal('8'),
                'price_per_board_foot': Decimal('4.50'),
                'price_per_piece': Decimal('42.00'),
                'image_url': 'https://images.pexels.com/photos/269063/pexels-photo-269063.jpeg',
                'inventory_qty': 52,
            },
            {
                'name': 'Cedar 1x6x6',
                'sku': 'CED-1x6-6',
                'category': 'Softwood',
                'thickness': Decimal('0.75'),
                'width': Decimal('5.50'),
                'length': Decimal('6'),
                'price_per_board_foot': Decimal('5.75'),
                'price_per_piece': Decimal('15.00'),
                'image_url': 'https://images.pexels.com/photos/518245/pexels-photo-518245.jpeg',
                'inventory_qty': 68,
            },
            {
                'name': 'Hem-Fir 2x8x12',
                'sku': 'HF-2x8-12',
                'category': 'Softwood',
                'thickness': Decimal('1.50'),
                'width': Decimal('7.50'),
                'length': Decimal('12'),
                'price_per_board_foot': Decimal('3.15'),
                'price_per_piece': Decimal('28.00'),
                'image_url': 'https://images.pexels.com/photos/163999/pexels-photo-163999.jpeg',
                'inventory_qty': 78,
            },
            # Engineered
            {
                'name': 'LVL Beam 1.75x11.875x16',
                'sku': 'LVL-175x1187-16',
                'category': 'Engineered',
                'thickness': Decimal('1.75'),
                'width': Decimal('11.875'),
                'length': Decimal('16'),
                'price_per_board_foot': Decimal('5.50'),
                'price_per_piece': Decimal('125.00'),
                'image_url': 'https://images.pexels.com/photos/172288/pexels-photo-172288.jpeg',
                'inventory_qty': 18,
            },
            {
                'name': 'OSB Plywood 3/4x4x8',
                'sku': 'OSB-3/4-4x8',
                'category': 'Engineered',
                'thickness': Decimal('0.75'),
                'width': Decimal('4'),
                'length': Decimal('8'),
                'price_per_board_foot': Decimal('2.15'),
                'price_per_piece': Decimal('28.50'),
                'image_url': 'https://images.pexels.com/photos/172296/pexels-photo-172296.jpeg',
                'inventory_qty': 45,
            },
            {
                'name': 'Laminated Beam 2x10x14',
                'sku': 'LAM-2x10-14',
                'category': 'Engineered',
                'thickness': Decimal('1.75'),
                'width': Decimal('9.50'),
                'length': Decimal('14'),
                'price_per_board_foot': Decimal('6.85'),
                'price_per_piece': Decimal('85.00'),
                'image_url': 'https://images.pexels.com/photos/301378/pexels-photo-301378.jpeg',
                'inventory_qty': 12,
            },
            {
                'name': 'MDF Board 3/4x4x8',
                'sku': 'MDF-3/4-4x8',
                'category': 'Engineered',
                'thickness': Decimal('0.75'),
                'width': Decimal('4'),
                'length': Decimal('8'),
                'price_per_board_foot': Decimal('1.75'),
                'price_per_piece': Decimal('22.50'),
                'image_url': 'https://images.pexels.com/photos/172289/pexels-photo-172289.jpeg',
                'inventory_qty': 56,
            },
            {
                'name': 'Glulam Beam 1.5x12x20',
                'sku': 'GLUL-1.5x12-20',
                'category': 'Engineered',
                'thickness': Decimal('1.50'),
                'width': Decimal('12'),
                'length': Decimal('20'),
                'price_per_board_foot': Decimal('7.25'),
                'price_per_piece': Decimal('180.00'),
                'image_url': 'https://images.pexels.com/photos/518245/pexels-photo-518245.jpeg',
                'inventory_qty': 8,
            },
        ]

        created_count = 0
        updated_count = 0

        for product_data in products_data:
            image_url = product_data.pop('image_url')
            inventory_qty = product_data.pop('inventory_qty')
            category_name = product_data.pop('category')

            # Get category
            category = LumberCategory.objects.get(name=category_name)
            product_data['category'] = category

            # Download and attach image
            try:
                response = requests.get(image_url, timeout=10)
                response.raise_for_status()
                image_name = f"{product_data['sku']}.jpg"
                image_content = ContentFile(response.content, name=image_name)
                product_data['image'] = image_content
            except Exception as e:
                self.stdout.write(self.style.WARNING(
                    f"Failed to download image for {product_data['sku']}: {str(e)}"
                ))

            # Create or update product
            product, created = LumberProduct.objects.update_or_create(
                sku=product_data['sku'],
                defaults=product_data
            )

            # Create or update inventory
            Inventory.objects.update_or_create(
                product=product,
                defaults={
                    'quantity_pieces': inventory_qty,
                    'total_board_feet': Decimal(product.board_feet) * inventory_qty
                }
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'[+] Created: {product.name} ({product.sku})'
                ))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(
                    f'[*] Updated: {product.name} ({product.sku})'
                ))

        self.stdout.write(self.style.SUCCESS(
            f'\nSummary: {created_count} created, {updated_count} updated'
        ))
