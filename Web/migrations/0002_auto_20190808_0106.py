# Generated by Django 2.1.7 on 2019-08-08 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='major_ngram_keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major', models.CharField(default='', max_length=20)),
                ('keyword', models.CharField(default='', max_length=100)),
                ('word_date', models.DateTimeField(default='')),
                ('count', models.IntegerField(null=True)),
                ('pos_percent', models.FloatField(default=0.0, null=True)),
                ('neg_percent', models.FloatField(default=0.0, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='major_ngram_keyword',
            unique_together={('major', 'keyword', 'word_date')},
        ),
    ]
