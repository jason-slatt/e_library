# Generated by Django 5.1.2 on 2024-10-28 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('librarian', 'Librarian'), ('user', 'User')], default='user', max_length=20)),
            ],
        ),
    ]