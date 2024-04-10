"""Sequent Microsystems Multiio Integration"""

import logging

from homeassistant.helpers import config_validation as cv
import voluptuous as vol

DOMAIN = "SMmultiio"
CONF_STACK = "stack"

"""
SMmultiio:
    -   stack: 0
        sensors:
            led-1:
            led-2:
        numbers:

"""
CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema([vol.Schema({
        vol.Optional(CONF_STACK, default="0"): cv.string,
        vol.Optional("rtd_res", default="-1"): cv.string
    }, extra=vol.ALLOW_EXTRA)])
}, extra=vol.ALLOW_EXTRA)

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

def setup(hass, config):
    hass.data[DOMAIN] = []
    configs = config.get(DOMAIN)
    for conf in configs:
        _LOGGER.error(conf.get("stack"))
        _LOGGER.error(conf.get("led"))
        
    return True
