# Generated by Django 3.1.1 on 2021-03-25 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('metroevent', '0004_auto_20210324_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('admin', models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('organizer', models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('date_promoted', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.RenameField(
            model_name='request',
            old_name='event_id',
            new_name='event',
        ),
        migrations.RemoveField(
            model_name='event',
            name='organizers',
        ),
        migrations.RemoveField(
            model_name='request',
            name='is_approved',
        ),
        migrations.RemoveField(
            model_name='request',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='request',
            name='user_type',
        ),
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.CharField(blank=True, default='Pending', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='request',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.AddField(
            model_name='organizer',
            name='event',
            field=models.ManyToManyField(blank=True, to='metroevent.Event'),
        ),
        migrations.AddField(
            model_name='administrator',
            name='event',
            field=models.ManyToManyField(blank=True, to='metroevent.Event'),
        ),
    ]