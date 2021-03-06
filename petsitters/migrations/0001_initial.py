# Generated by Django 3.2.9 on 2022-05-17 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Petsitter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=45)),
                ('title', models.CharField(max_length=150)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('grade', models.CharField(max_length=45)),
                ('count', models.PositiveIntegerField(default=0)),
                ('information', models.TextField(max_length=2000)),
                ('address', models.CharField(max_length=100)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
            options={
                'db_table': 'petsitters',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'types',
            },
        ),
        migrations.CreateModel(
            name='PetsitterType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('petsitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petsitters.petsitter')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petsitters.type')),
            ],
            options={
                'db_table': 'petsitter_types',
            },
        ),
        migrations.CreateModel(
            name='PetsitterImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=1000)),
                ('petsitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petsitters.petsitter')),
            ],
            options={
                'db_table': 'petsitter_images',
            },
        ),
        migrations.AddField(
            model_name='petsitter',
            name='types',
            field=models.ManyToManyField(through='petsitters.PetsitterType', to='petsitters.Type'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', models.CharField(blank=True, max_length=1000)),
                ('petsitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petsitters.petsitter')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
    ]
