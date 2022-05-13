# Generated by Django 4.0.4 on 2022-05-13 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recycling', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatierPremier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.FloatField(default=0.0)),
                ('photo', models.ImageField(upload_to='media/mp')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.FloatField(default=0.0)),
                ('photo', models.ImageField(upload_to='media/product')),
            ],
        ),
    ]
