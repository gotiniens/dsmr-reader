��          t      �         D     e   V  �   �     G     L     Y  ^   l  �   �  -   L  D   z  �  �  K   c  l   �  �        �  
   �     �  ]   �  �   F  ,   �  +   �                     
                               	        Cached for an hour, to reduce the number of duplicate messages sent. Discarded when there is already another unsent message queued with the exact same topic and contents. It should be already configured while installing or upgrading DSMR-reader and listed running if you execute ``sudo supervisorctl status``. MQTT MQTT caching MQTT messages are: Sent with the ``retain`` flag, asking the broker to cache the latest value sent to each topic. Since DSMR-reader ``v4.x``, you no longer need to manually configure ``dsmr_client`` (formerly known as ``dsmr_mqtt``) for MQTT. The ``dsmr_client`` / ``dsmr_mqtt`` processes This prevents duplicate messages and removes a significant overhead. Project-Id-Version: DSMR Reader
Report-Msgid-Bugs-To: Dennis Siemensma <github@dennissiemensma.nl>
Last-Translator: Dennis Siemensma <github@dennissiemensma.nl>
Language: nl
Language-Team: Dennis Siemensma <github@dennissiemensma.nl>
Plural-Forms: nplurals=2; plural=(n != 1);
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
X-Generator: Poedit 2.0.6
 Gecached gedurende een uur, om het aantal dubbele berichten te verminderen. Genegeerd wanneer er al een soortgelijk onverstuurd bericht klaarstaat, met exact hetzelfde topic en inhoud. Het zou al geconfigureerd moeten zijn bij installatie of upgrade van DSMR-reader. Zie ook of deze getoond wordt bij het uitvoeren van ``sudo supervisorctl status``. MQTT MQTT cache MQTT-berichten worden: Verstuurd met de ``retain`` vlag, waardoor de broker de laatste waarde van elk topic bewaart. Sinds DSMR-reader ``v4.x`` hoef je niet meer handmatig ``dsmr_client`` te configureren (voorheen bekend als ``dsmr_mqtt``) voor MQTT. De ``dsmr_client`` / ``dsmr_mqtt`` processen Dit zorgt voor aanzienlijk minder overhead. 