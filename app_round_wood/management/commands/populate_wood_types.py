from django.core.management.base import BaseCommand
from app_round_wood.models import WoodType


class Command(BaseCommand):
    help = 'Populate database with common wood types used in lumber industry'

    def handle(self, *args, **options):
        wood_types_data = [
            {
                'name': 'Oak Logs',
                'species': 'hardwood',
                'default_diameter_inches': 12.0,
                'default_length_feet': 16.0,
                'description': 'Premium hardwood logs suitable for furniture, flooring, and decorative applications. Known for strength and beautiful grain.'
            },
            {
                'name': 'Pine Logs',
                'species': 'softwood',
                'default_diameter_inches': 10.0,
                'default_length_feet': 16.0,
                'description': 'Softwood logs commonly used for general construction, pallets, and pulp production. Cost-effective and readily available.'
            },
            {
                'name': 'Mahogany Logs',
                'species': 'tropical',
                'default_diameter_inches': 14.0,
                'default_length_feet': 16.0,
                'description': 'Premium tropical hardwood with rich reddish-brown color. Ideal for fine furniture and decorative woodwork.'
            },
            {
                'name': 'Maple Logs',
                'species': 'hardwood',
                'default_diameter_inches': 10.0,
                'default_length_feet': 12.0,
                'description': 'Dense hardwood used for flooring, cabinetry, and musical instruments. High strength and excellent workability.'
            },
            {
                'name': 'Birch Logs',
                'species': 'hardwood',
                'default_diameter_inches': 10.0,
                'default_length_feet': 14.0,
                'description': 'Hardwood with fine grain suitable for plywood, veneer, and quality furniture. Light colored with good durability.'
            },
            {
                'name': 'Walnut Logs',
                'species': 'hardwood',
                'default_diameter_inches': 12.0,
                'default_length_feet': 14.0,
                'description': 'Premium hardwood with dark brown color. Highly valued for fine furniture, gunstocks, and decorative applications.'
            },
            {
                'name': 'Cedar Logs',
                'species': 'softwood',
                'default_diameter_inches': 8.0,
                'default_length_feet': 12.0,
                'description': 'Lightweight softwood with natural decay resistance. Excellent for outdoor construction and aromatic applications.'
            },
            {
                'name': 'Ash Logs',
                'species': 'hardwood',
                'default_diameter_inches': 10.0,
                'default_length_feet': 14.0,
                'description': 'Strong hardwood with light color and good shock resistance. Used for tool handles, sports equipment, and furniture.'
            },
            {
                'name': 'Fir Logs',
                'species': 'softwood',
                'default_diameter_inches': 12.0,
                'default_length_feet': 16.0,
                'description': 'Strong softwood used for construction lumber, plywood, and structural applications. High strength-to-weight ratio.'
            },
            {
                'name': 'Spruce Logs',
                'species': 'softwood',
                'default_diameter_inches': 10.0,
                'default_length_feet': 14.0,
                'description': 'Lightweight strong softwood used for construction, aircraft materials, and musical instruments.'
            },
            {
                'name': 'Hemlock Logs',
                'species': 'softwood',
                'default_diameter_inches': 10.0,
                'default_length_feet': 14.0,
                'description': 'Softwood with good strength-to-weight ratio. Used for general construction, framing, and rough lumber applications.'
            },
            {
                'name': 'Teak Logs',
                'species': 'tropical',
                'default_diameter_inches': 14.0,
                'default_length_feet': 12.0,
                'description': 'Exotic hardwood with excellent durability and natural oil content. Premium choice for outdoor furniture and marine applications.'
            },
            {
                'name': 'Cherry Logs',
                'species': 'hardwood',
                'default_diameter_inches': 10.0,
                'default_length_feet': 12.0,
                'description': 'Fine-grained hardwood with warm reddish-brown color. Excellent for furniture, cabinetry, and fine woodworking.'
            },
            {
                'name': 'Poplar Logs',
                'species': 'softwood',
                'default_diameter_inches': 10.0,
                'default_length_feet': 14.0,
                'description': 'Softwood with fine grain and light color. Easy to work with, commonly used for boxes, pallets, and veneer.'
            },
            {
                'name': 'Elm Logs',
                'species': 'hardwood',
                'default_diameter_inches': 12.0,
                'default_length_feet': 14.0,
                'description': 'Hardwood with interlocking grain providing high impact resistance. Used for boat building, furniture, and veneers.'
            },
        ]

        created_count = 0
        updated_count = 0

        for data in wood_types_data:
            wood_type, created = WoodType.objects.update_or_create(
                name=data['name'],
                defaults={
                    'species': data['species'],
                    'default_diameter_inches': data['default_diameter_inches'],
                    'default_length_feet': data['default_length_feet'],
                    'description': data['description'],
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'[+] Created: {wood_type.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'[*] Updated: {wood_type.name}')
                )

        # Print summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'[+] Created: {created_count} wood types'))
        if updated_count > 0:
            self.stdout.write(self.style.WARNING(f'[*] Updated: {updated_count} wood types'))
        self.stdout.write(self.style.SUCCESS(f'[SUCCESS] Total: {created_count + updated_count} wood types in database'))
        self.stdout.write('='*60)
