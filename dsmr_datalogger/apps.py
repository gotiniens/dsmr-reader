from django.apps import AppConfig
from django.conf import settings
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from dsmr_backend.dto import MonitoringStatusIssue
from dsmr_backend.signals import request_status


class DataloggerAppConfig(AppConfig):
    name = 'dsmr_datalogger'
    verbose_name = _('Datalogger')


@receiver(request_status)
def check_recent_readings(**kwargs):
    from dsmr_datalogger.models.reading import DsmrReading

    try:
        latest_reading = DsmrReading.objects.all().order_by('-timestamp')[0]
    except (DsmrReading.DoesNotExist, IndexError):
        return MonitoringStatusIssue(
            __name__,
            _('Waiting for the first reading ever'),
            timezone.now()
        )

    max_slack = timezone.now() - timezone.timedelta(
        minutes=settings.DSMRREADER_STATUS_READING_OFFSET_MINUTES
    )

    if latest_reading.timestamp > max_slack:
        return

    return MonitoringStatusIssue(
        __name__,
        _('No recent readings received'),
        latest_reading.timestamp
    )
