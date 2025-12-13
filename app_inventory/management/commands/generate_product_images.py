from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from app_inventory.models import LumberProduct
from PIL import Image, ImageDraw, ImageFont
import io
import os


class Command(BaseCommand):
    help = 'Generate placeholder images for products'

    def handle(self, *args, **options):
        # Color mapping for categories
        category_colors = {
            'Hardwood': {'bg': '#8B4513', 'accent': '#D2691E'},
            'Softwood': {'bg': '#CD853F', 'accent': '#F4A460'},
            'Engineered': {'bg': '#696969', 'accent': '#A9A9A9'},
        }

        products = LumberProduct.objects.all()
        created_count = 0

        for product in products:
            # Skip if already has image
            if product.image:
                self.stdout.write(f'Skipping {product.name} - already has image')
                continue

            try:
                # Get category color
                color_info = category_colors.get(product.category.name, {'bg': '#696969', 'accent': '#A9A9A9'})
                bg_color = color_info['bg']
                accent_color = color_info['accent']

                # Create image
                img = Image.new('RGB', (600, 600), color=bg_color)
                draw = ImageDraw.Draw(img)

                # Add gradient-like effect with rectangles
                for i in range(0, 600, 30):
                    draw.rectangle(
                        [(i, 0), (i + 15, 600)],
                        fill=accent_color,
                        outline=None
                    )

                # Add wood texture lines
                for i in range(0, 600, 40):
                    draw.line([(0, i), (600, i)], fill='#000000', width=1)

                # Add lumber icon/text in center
                try:
                    # Try to use default font, fallback if not available
                    font_size = 60
                    font = ImageFont.load_default()
                except:
                    font = ImageFont.load_default()

                # Add dimensions text
                text = f"{product.thickness}\" × {product.width}\" × {product.length}ft"
                text_color = '#FFFFFF'

                # Get text bounding box for centering
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                x = (600 - text_width) // 2
                y = (600 - text_height) // 2

                # Add shadow
                draw.text((x + 2, y + 2), text, fill='#000000', font=font)
                # Add main text
                draw.text((x, y), text, fill=text_color, font=font)

                # Add price label at bottom
                price_text = f"₱{product.price_per_board_foot}/BF"
                bbox = draw.textbbox((0, 0), price_text, font=font)
                price_width = bbox[2] - bbox[0]
                px = (600 - price_width) // 2
                py = 500

                draw.rectangle([(px - 10, py - 10), (px + price_width + 10, py + 30)], fill=accent_color)
                draw.text((px, py), price_text, fill='#FFFFFF', font=font)

                # Save to bytes
                img_io = io.BytesIO()
                img.save(img_io, format='JPEG', quality=85)
                img_io.seek(0)

                # Create filename
                filename = f"product_{product.id}_{product.sku}.jpg"

                # Save to model
                product.image.save(
                    filename,
                    ContentFile(img_io.getvalue()),
                    save=True
                )

                self.stdout.write(
                    self.style.SUCCESS(f'Generated image for: {product.name}')
                )
                created_count += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error generating image for {product.name}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully generated {created_count} product images!')
        )
