# Generated by Django 5.2.1 on 2025-05-14 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_uploadedfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='img',
            field=models.ImageField(upload_to='uploaded_images/'),
        ),
    ]
