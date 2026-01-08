#!/usr/bin/env python
"""
Quick script to populate wood types in the database.

Usage:
    python populate_wood_types.py
    
Or using Django management command:
    python manage.py populate_wood_types
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumber.settings')
django.setup()

from app_round_wood.models import WoodType

# Wood types data
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
]

def main():
    created_count = 0
    updated_count = 0
    
    print(f"\nPopulating {len(wood_types_data)} wood types...")
    print("=" * 60)
    
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
            print(f"[+] Created: {wood_type.name}")
        else:
            updated_count += 1
            print(f"[*] Updated: {wood_type.name}")
    
    print("=" * 60)
    print(f"[+] Created: {created_count} wood types")
    if updated_count > 0:
        print(f"[*] Updated: {updated_count} wood types")
    print(f"[SUCCESS] Total: {created_count + updated_count} wood types in database\n")

if __name__ == '__main__':
    main()
