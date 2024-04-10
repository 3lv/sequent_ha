"""Sequent Microsystems Multiio Integration"""

import logging

from homeassistant.helpers import config_validation as cv
import voluptuous as vol

DOMAIN = "SMmultiio"
CONF_STACK = "stack"
CONF_TYPE = "type"
CONF_CHAN = "chan"

"""
SMmultiio:
    -   stack: 0
        led-1:
        led-2:

"""
SCHEMA_DICT = {}

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema([vol.Schema({
        vol.Optional(CONF_STACK, default="0"): cv.string,
    }, extra=vol.ALLOW_EXTRA)])
}, extra=vol.ALLOW_EXTRA)

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

def setup(hass, config):
    hass.data[DOMAIN] = []
    card_configs = config.get(DOMAIN)
    for card_config in card_configs:
        stack = int(card_config.pop(CONF_STACK, 0))
        for entity in card_config:
            [type, chan] = entity.rsplit("-", 1)[1]
            entity_config = {
                    CONF_STACK: stack,
                    CONF_TYPE: type,
                    CONF_CHAN: chan
            }
            hass.helpers.discovery.load_platform("sensor", DOMAIN, {}, entity_config)
        
    return True
