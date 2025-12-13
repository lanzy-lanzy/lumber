# Generated migration to change supplier and product from PROTECT to CASCADE

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app_supplier", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchaseorder",
            name="supplier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="purchase_orders",
                to="app_supplier.supplier",
            ),
        ),
        migrations.AlterField(
            model_name="purchaseorderitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="app_inventory.lumberproduct",
            ),
        ),
    ]
