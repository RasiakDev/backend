# Generated by Django 5.0.3 on 2024-03-13 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eCommerce', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='descritption',
            new_name='description',
        ),
    ]
