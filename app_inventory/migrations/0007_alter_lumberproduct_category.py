# Generated migration to change LumberProduct.category from PROTECT to CASCADE

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app_inventory", "0006_alter_stocktransaction_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lumberproduct",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="app_inventory.lumbercategory",
            ),
        ),
    ]
