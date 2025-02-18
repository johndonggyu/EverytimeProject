# Generated by Django 2.2.4 on 2019-08-26 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0004_auto_20190817_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='neg_percent',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='board',
            name='pos_percent',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='eval',
            name='neg_percent',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='eval',
            name='pos_percent',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
