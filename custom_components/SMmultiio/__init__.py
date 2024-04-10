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
        rtd_res-1:
        rtd_temp-1:

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
            try:
                [type, chan] = entity.rsplit("-", 1)
            except:
                _LOGGER.error(entity, " doesn't respect type-chan format")
                continue
            entity_config = {
                    CONF_STACK: stack,
                    CONF_TYPE: type,
                    CONF_CHAN: chan
            }
            _LOGGER.debug("entity_config: %s", entity_config)
            hass.helpers.discovery.load_platform("sensor", DOMAIN, {}, entity_config)
        
    return True
