# Generated by Django 3.2.9 on 2022-05-17 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kakao_id', models.BigIntegerField(default=0, unique=True)),
                ('name', models.CharField(max_length=45, null=True)),
                ('nickname', models.CharField(max_length=45, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('password', models.CharField(max_length=200, null=True)),
                ('mobile', models.CharField(max_length=45, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
