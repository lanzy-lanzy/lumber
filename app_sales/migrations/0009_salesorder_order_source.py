# Generated migration file

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_sales', '0008_rename_app_sales_oc_custome_idx_app_sales_o_custome_3a26cb_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorder',
            name='order_source',
            field=models.CharField(
                choices=[('customer_order', 'Customer Order'), ('point_of_sale', 'Point of Sale / Walk-in')],
                default='point_of_sale',
                max_length=20
            ),
        ),
    ]
