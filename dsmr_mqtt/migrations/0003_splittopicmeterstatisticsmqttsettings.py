# Generated by Django 2.0.2 on 2018-03-13 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsmr_mqtt', '0002_daytotalsmqttsettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='SplitTopicMeterStatisticsMQTTSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=False, help_text='Whether meter statistics are sent to the broker, having each field sent to a different topic.', verbose_name='Enabled')),
                ('formatting', models.TextField(default='\n[mapping]\n# DATA = TOPIC PATH\ndsmr_version = dsmr/meter-stats/dsmr_version\nelectricity_tariff = dsmr/meter-stats/electricity_tariff\npower_failure_count = dsmr/meter-stats/power_failure_count\nlong_power_failure_count = dsmr/meter-stats/long_power_failure_count\nvoltage_sag_count_l1 = dsmr/meter-stats/voltage_sag_count_l1\nvoltage_sag_count_l2 = dsmr/meter-stats/voltage_sag_count_l2\nvoltage_sag_count_l3 = dsmr/meter-stats/voltage_sag_count_l3\nvoltage_swell_count_l1 = dsmr/meter-stats/voltage_swell_count_l1\nvoltage_swell_count_l2 = dsmr/meter-stats/voltage_swell_count_l2\nvoltage_swell_count_l3 = dsmr/meter-stats/voltage_swell_count_l3\nrejected_telegrams = dsmr/meter-stats/rejected_telegrams\n', help_text='Maps the field names to separate topics sent to the broker.', verbose_name='Formatting')),
            ],
            options={
                'verbose_name': 'MQTT: Meter Statistics (per split topic) configuration',
                'default_permissions': (),
            },
        ),
    ]