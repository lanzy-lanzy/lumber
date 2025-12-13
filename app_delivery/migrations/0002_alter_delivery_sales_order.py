# Generated migration to change sales_order from PROTECT to CASCADE

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app_sales", "0005_alter_salesorderitem_product"),
        ("app_delivery", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="delivery",
            name="sales_order",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="delivery",
                to="app_sales.salesorder",
            ),
        ),
    ]
