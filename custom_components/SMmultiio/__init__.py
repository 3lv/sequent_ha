"""Sequent Microsystems Multiio Integration"""

import logging

from homeassistant.helpers import config_validation as cv
import voluptuous as vol


from homeassistant.const import (
	CONF_NAME
)
CONF_NAME = CONF_NAME
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
    if not card_configs:
        entity_config = {
                CONF_STACK: 0,
                CONF_TYPE: "ALL"
        }
        hass.helpers.discovery.load_platform("sensor", DOMAIN, entity_config, config)
        return
    for card_config in card_configs:
        stack = int(card_config.pop(CONF_STACK, 0))
        if not card_config:
            entity_config = {
                    CONF_STACK: stack,
                    CONF_TYPE: "ALL"
            }
            hass.helpers.discovery.load_platform("sensor", DOMAIN, entity_config, config)
            continue
        for entity in card_config:
            try:
                [type, chan] = entity.rsplit("-", 1)
            except:
                _LOGGER.error(entity, " doesn't respect type-chan format")
                continue
            entity_config = {
                    CONF_NAME: entity,
                    CONF_STACK: stack,
                    CONF_TYPE: type,
                    CONF_CHAN: chan
            }
            hass.helpers.discovery.load_platform("sensor", DOMAIN, entity_config, config)
        
    return True
