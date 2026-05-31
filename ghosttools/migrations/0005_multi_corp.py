from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eveonline', '0015_factions'),
        ('ghosttools', '0004_ghosttoolsconfiguration_alliances'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ghosttoolsconfiguration',
            name='corporation',
        ),
        migrations.AddField(
            model_name='ghosttoolsconfiguration',
            name='corporations',
            field=models.ManyToManyField(blank=True, to='eveonline.EveCorporationInfo'),
        ),
    ]
