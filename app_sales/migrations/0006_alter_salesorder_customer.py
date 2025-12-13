# Generated migration to change customer from PROTECT to CASCADE

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app_sales", "0005_alter_salesorderitem_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="salesorder",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sales_orders",
                to="app_sales.customer",
            ),
        ),
    ]
