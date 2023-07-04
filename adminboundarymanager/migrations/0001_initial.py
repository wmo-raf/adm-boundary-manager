# Generated by Django 4.2.2 on 2023-07-04 11:05

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0083_workflowcontenttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminBoundary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_0', models.CharField(blank=True, max_length=100, null=True)),
                ('name_1', models.CharField(blank=True, max_length=100, null=True)),
                ('name_2', models.CharField(blank=True, max_length=100, null=True)),
                ('name_3', models.CharField(blank=True, max_length=100, null=True)),
                ('name_4', models.CharField(blank=True, max_length=100, null=True)),
                ('gid_0', models.CharField(blank=True, max_length=100, null=True)),
                ('gid_1', models.CharField(blank=True, max_length=100, null=True)),
                ('gid_2', models.CharField(blank=True, max_length=100, null=True)),
                ('gid_3', models.CharField(blank=True, max_length=100, null=True)),
                ('gid_4', models.CharField(blank=True, max_length=100, null=True)),
                ('level', models.IntegerField(blank=True, null=True)),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Administrative Boundaries',
            },
        ),
        migrations.CreateModel(
            name='AdminBoundarySettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='country')),
                ('parent', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='countries', to='adminboundarymanager.adminboundarysettings')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
