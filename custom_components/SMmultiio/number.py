import voluptuous as vol
import multiio as SMmultiio
import logging
import time

from homeassistant.const import (
	CONF_NAME
)

from homeassistant.components.light import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.components.number import NumberEntity

NAME_PREFIX = "multiio"
SM_NUMBER_MAP = {
        "uout": {
                "uom": "V",
                "min_value": 0.0,
                "max_value": 10.0,
                "step": 0.01,
                "com": {
                    "get": "get_u_out",
                    "set": "set_u_out"
                },
                "icon": {
                    "on": "mdi:flash-triangle",
                    "off": "mdi:flash-triangle"
                }
        },
        "iout": {
                "uom": "mA",
                "min_value": 4.0,
                "max_value": 20.0,
                "step": 0.01,
                "com": {
                    "get": "get_i_out",
                    "set": "set_i_out"
                },
                "icon": {
                    "on": "mdi:current-dc",
                    "off": "mdi:current-dc"
                }
        },
        "servo": {
                "uom": "%",
                "min_value": -140.0,
                "max_value": +140.0,
                "step": 0.1,
                "com": {
                    "get": "get_servo",
                    "set": "set_servo"
                },
                "icon": {
                    "on": "mdi:vector-triangle",
                    "off": "mdi:vector-triangle"
                }
        },
}

CONF_STACK = "stack"
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional("uout", default="-1"): cv.string,
    vol.Optional("iout", default="-1"): cv.string,
	vol.Optional(CONF_NAME, default=""): cv.string,
	vol.Optional(CONF_STACK, default="0"): cv.string,
})

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    switch_type = -1
    channel = -1
    for key in SM_NUMBER_MAP:
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
    add_devices([Number(
		name=config.get(CONF_NAME),
        stack=config.get(CONF_STACK),
        type=switch_type,
        chan=channel
	)])

class Number(NumberEntity):
    """Sequent Microsystems Multiio Switch"""
    def __init__(self, name, stack, type, chan):
        if name == "":
            name = NAME_PREFIX + "_" + type + chan
        self._name = name
        self._stack = int(stack)
        self._type = type
        self._chan = int(chan)
        self._SM = SMmultiio.SMmultiio(self._stack)
        com = SM_NUMBER_MAP[self._type]["com"]
        self._SM_get = getattr(self._SM, com["get"])
        self._SM_set = getattr(self._SM, com["set"])
        self._short_timeout = .05
        self._icons = SM_NUMBER_MAP[self._type]["icon"]
        self._icon = self._icons["off"]
        self._uom = SM_NUMBER_MAP[self._type]["uom"]
        self._min_value = SM_NUMBER_MAP[self._type]["min_value"]
        self._max_value = SM_NUMBER_MAP[self._type]["max_value"]
        self._step = SM_NUMBER_MAP[self._type]["step"]
        self._value = 0

    def update(self):
        time.sleep(self._short_timeout)
        try:
            self._value = self._SM_get(self._chan)
        except Exception as ex:
            _LOGGER.error(NAME_PREFIX + " %s update() failed, %e, %s, %s", self._type, ex, str(self._stack), str(self._chan))
            return
        if self._value != 0:
            self._icon = self._icons["on"]
        else:
            self._icon = self._icons["off"]

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def native_unit_of_measurement(self):
        return self._uom

    @property
    def native_step(self):
        return self._step

    @property
    def native_min_value(self):
        return self._min_value

    @property
    def native_max_value(self):
        return self._max_value

    @property
    def native_value(self):
        return self._value

    def set_native_value(self, value):
        try:
            self._SM_set(self._chan, value)
        except Exception as ex:
            _LOGGER.error(NAME_PREFIX + " %s setting value failed, %e", self._type, ex)
