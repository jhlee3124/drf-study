# Generated by Django 4.2.5 on 2023-09-21 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0004_post_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='ip',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
