# Generated by Django 4.2.8 on 2024-02-28 07:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product_portfolio", "0003_alter_scancodeproject_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scancodeproject",
            name="type",
            field=models.CharField(
                choices=[
                    ("IMPORT_FROM_MANIFEST", "Import from Manifest"),
                    ("LOAD_SBOMS", "Load SBOMs"),
                    ("PULL_FROM_SCANCODEIO", "Pull from ScanCode.io"),
                ],
                db_index=True,
                help_text="The type of import, for the ProjectType choices.",
                max_length=50,
            ),
        ),
    ]
