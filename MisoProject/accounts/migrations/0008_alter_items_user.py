# Generated by Django 4.1 on 2024-01-31 14:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_usedmisodetail_user'),
    ]

    operations = [
        migrations.RunSQL("UPDATE items SET user_id = (SELECT id FROM accounts_users WHERE email = 'miso_app@mail.com') WHERE user_id IS NULL;", reverse_sql=migrations.RunSQL.noop),
        migrations.AlterField(
            model_name='items',
            name='user',
            field=models.ForeignKey(default=datetime.datetime(2024, 1, 31, 14, 13, 2, 290029, tzinfo=datetime.timezone.utc), on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
       
    ]
