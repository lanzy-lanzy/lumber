# Generated migration for ID document and approval fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_customuser_user_type_alter_customuser_role_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_approved",
            field=models.BooleanField(
                default=False, help_text="Admin approval for customer registration"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="id_document",
            field=models.FileField(
                blank=True,
                help_text="Upload government ID or valid identification",
                null=True,
                upload_to="id_documents/",
            ),
        ),
    ]
