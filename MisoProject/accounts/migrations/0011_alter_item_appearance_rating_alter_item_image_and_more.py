# Generated by Django 4.1 on 2024-02-19 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_item_remove_usedmisodetail_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='appearance_rating',
            field=models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3')], null=True, verbose_name='見た目'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='item_images/', verbose_name='画像'),
        ),
        migrations.AlterField(
            model_name='item',
            name='taste_rating',
            field=models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3')], null=True, verbose_name='味'),
        ),
        migrations.AlterField(
            model_name='item',
            name='thoughts',
            field=models.TextField(blank=True, null=True, verbose_name='メモ・感想'),
        ),
    ]
