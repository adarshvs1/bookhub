# Generated by Django 5.0.6 on 2024-10-09 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('romance', 'romance'), ('comic', 'comic'), ('novel', 'novel'), ('fantasy', 'fantasy'), ('history', 'history'), ('inspirational', 'inspirational'), ('biography', 'biography'), ('fairytale', 'fairytale'), ('thriller', 'thriller')], default='novel', max_length=200),
        ),
    ]
