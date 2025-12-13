# Generated migration to change StockTransaction.product from PROTECT to CASCADE

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app_inventory", "0005_lumberproduct_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stocktransaction",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="stock_transactions",
                to="app_inventory.lumberproduct",
            ),
        ),
    ]
