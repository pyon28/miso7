# Generated by Django 4.1 on 2024-02-02 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_items_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usedmisodetail',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='used_miso_details', to='accounts.items'),
        ),
    ]
