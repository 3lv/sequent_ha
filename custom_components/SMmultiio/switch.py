import voluptuous as vol
import multiio as SMmultiio
import logging
import time

from homeassistant.const import (
	CONF_NAME
)

from homeassistant.components.light import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import SwitchEntity

MULTIIO_SWITCH_MAP = {
        "led": {
                "com": {
                    "get": "get_led",
                    "set": "set_led"
                },
                "icon": {
                    "on": "mdi:led-on",
                    "off": "mdi:led-off"
                }
        },
        "relay": {
                "com": {
                    "get": "get_relay",
                    "set": "set_relay"
                },
        }
}
SM_SWITCH_MAP = MULTIIO_SWITCH_MAP

CONF_STACK = "stack"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional("led", default="-1"): cv.string,
    vol.Optional("relay", default="-1"): cv.string,
	vol.Optional(CONF_NAME, default=""): cv.string,
	vol.Optional(CONF_STACK, default="0"): cv.string,
})

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    switch_type = -1
    channel = -1
    for key in SM_SWITCH_MAP:
        val = config.get(key)
        if val != "-1":
            if switch_type != -1:
                # ALREADY SET RAISE ERROR
                pass
            switch_type = key
            channel = val
    if switch_type != -1:
        # NO SWITCH TYPE FOUND, AMBIGUOUS, ERROR
        pass
    add_devices([Switch(
		name=config.get(CONF_NAME),
        stack=config.get(CONF_STACK),
        type=switch_type,
        chan=channel
	)])

class Switch(SwitchEntity):
    """Sequent Microsystems Multiio Switch"""
    def __init__(self, name, stack, type, chan):
        if name == "":
            name = type + chan
        self._name = name
        self._stack = int(stack)
        self._type = type
        self._chan = int(chan)
        self._SM = SMmultiio.SMmultiio(self._stack)
        self._is_on

    def update(self):
        time.sleep(.2)
        com = SM_SWITCH_MAP[self._type]["com"]["get"]
        try:
            self._is_on = getattr(self._SM, com)(self._chan)
        except Exception as ex:
            _LOGGER.error("Multiio Led is_on() check failed, %e, %s, %s", ex, str(self._stack), str(self._chan))

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self, **kwargs):
        try:
            com = SM_SWITCH_MAP[self._type]["com"]["set"]
            getattr(self._SM, com)(self._chan, 1)
        except Exception as ex:
            _LOGGER.error("Multiio Led turn ON failed, %e", ex)

    def turn_off(self, **kwargs):
        try:
            com = SM_SWITCH_MAP[self._type]["com"]["set"]
            getattr(self._SM, com)(self._chan, 0)
        except Exception as ex:
            _LOGGER.error("Multiio Led turn OFF failed, %e", ex);
