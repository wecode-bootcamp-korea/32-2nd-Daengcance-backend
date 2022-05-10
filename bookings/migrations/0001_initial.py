# Generated by Django 4.0.4 on 2022-05-11 06:46

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('petsitters', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('booking_code', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('checkin_date', models.DateField()),
                ('checkout_date', models.DateField()),
                ('petsitter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petsitters.petsitter')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'bookings',
            },
        ),
    ]
