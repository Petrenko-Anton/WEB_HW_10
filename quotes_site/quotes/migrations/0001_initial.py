# Generated by Django 4.2.3 on 2023-07-20 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=50)),
                ('born_date', models.CharField(max_length=50)),
                ('born_location', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'authors',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.TextField()),
                ('author', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='quotes.author')),
                ('tags', models.ManyToManyField(to='quotes.tag')),
            ],
            options={
                'db_table': 'quotes',
            },
        ),
    ]