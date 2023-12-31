# Generated by Django 4.1.9 on 2023-07-16 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auctionlisting_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='comments',
        ),
        migrations.AlterField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.auctionlisting'),
        ),
    ]
