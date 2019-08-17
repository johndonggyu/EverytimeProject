# Generated by Django 2.2.4 on 2019-08-17 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0002_major_ngram_keyword'),
    ]

    operations = [
        migrations.CreateModel(
            name='ratingProfessor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countEval', models.IntegerField(null=True)),
                ('countKeyword', models.IntegerField(null=True)),
                ('prof', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Web.smu_professor')),
            ],
        ),
    ]
