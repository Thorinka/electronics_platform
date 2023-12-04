# Generated by Django 4.2.7 on 2023-12-01 15:25

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
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='почта')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('phone', models.CharField(max_length=12)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('role', models.CharField(choices=[('user', 'Пользователь'), ('admin', 'Администратор')], default='user', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
            },
        ),
    ]