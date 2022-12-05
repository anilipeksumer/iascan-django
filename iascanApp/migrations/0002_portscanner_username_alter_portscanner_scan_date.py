# Generated by Django 4.1.2 on 2022-10-14 12:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("iascanApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="portscanner",
            name="username",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="portscanner",
            name="scan_date",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Scan Date"),
        ),
    ]
