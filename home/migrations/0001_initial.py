# Generated by Django 4.2.19 on 2025-02-23 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeblogSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255)),
                ('footer', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('keywords', models.TextField()),
                ('author', models.CharField(max_length=255)),
                ('og_title', models.CharField(max_length=255)),
                ('og_description', models.TextField()),
                ('og_url', models.CharField(max_length=255)),
            ],
        ),
    ]
