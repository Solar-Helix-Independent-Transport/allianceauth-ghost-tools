# Generated by Django 4.0.2 on 2022-08-29 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eveonline', '0015_factions'),
        ('esi', '0011_add_token_indices'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='GhostToolsConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corporations', models.ManyToManyField(blank=True, to='eveonline.EveCorporationInfo')),
            ],
            options={
                'permissions': (('access_ghost_tools', 'Can View Ghost Tools'),),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='GhostKickToken',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='ghost_character', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='esi.token')),
            ],
        ),
    ]
