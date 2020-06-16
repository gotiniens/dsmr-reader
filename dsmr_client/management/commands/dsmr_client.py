import logging

from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from dsmr_backend.mixins import InfiniteManagementCommandMixin, StopInfiniteRun
from dsmr_mqtt.models.settings.broker import MQTTBrokerSettings
import dsmr_mqtt.services.broker


logger = logging.getLogger('commands')


class Command(InfiniteManagementCommandMixin, BaseCommand):
    help = _('Persistent client for publishing data to external services, when enabled.')
    name = __name__  # Required for PID file.

    # Global during this process' lifetime.
    mqtt_client = None

    def initialize(self):
        """ Set up persistent client. """
        self.sleep_time = MQTTBrokerSettings.get_solo().process_sleep
        self.mqtt_client = dsmr_mqtt.services.broker.initialize()

    def shutdown(self):
        """ Disconnects the client gracefully. """
        if self.mqtt_client:
            self.mqtt_client.disconnect()

    def run(self, **options):
        """ InfiniteManagementCommandMixin listens to handle() and calls run() in a loop. """
        # Check on each run. In case MQTT was either disabled, enabled or settings were changed.
        if MQTTBrokerSettings.get_solo().restart_required:
            MQTTBrokerSettings.objects.update(restart_required=False)
            logger.warning('CLIENT | --- Detected settings change, requiring process restart, stopping...')
            raise StopInfiniteRun()

        dsmr_mqtt.services.broker.run(mqtt_client=self.mqtt_client)
