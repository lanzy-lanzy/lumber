# Generated migration to change SalesOrderItem.product from PROTECT to CASCADE

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app_sales", "0004_shoppingcart_cartitem"),
    ]

    operations = [
        migrations.AlterField(
            model_name="salesorderitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="app_inventory.lumberproduct",
            ),
        ),
    ]
