import voluptuous as vol
import logging
import time
import types
import inspect
from inspect import signature

import multiio as SMmultiio

from homeassistant.const import (
	CONF_NAME
)

from homeassistant.components.light import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import SensorEntity

NAME_PREFIX = "multiio"
CONF_STACK = "stack"
SM_NUMBER_MAP = {
        "rtd_res": {
                "uom": "Ohm",
                "com": {
                    "get": "get_rtd_res",
                },
                "icon": {
                    "on": "mdi:flash-triangle",
                    "off": "mdi:flash-triangle"
                }
        },
        "rtd_temp": {
                "uom": "°C",
                "com": {
                    "get": "get_rtd_temp",
                },
                "icon": {
                    "on": "mdi:flash-triangle",
                    "off": "mdi:flash-triangle"
                }
        },
        "iin": {
                "uom": "mA",
                "com": {
                    "get": "get_i_in",
                },
                "icon": {
                    "on": "mdi:flash-triangle",
                    "off": "mdi:flash-triangle"
                }
        },
        "uin": {
                "uom": "V",
                "com": {
                    "get": "get_i_in",
                },
                "icon": {
                    "on": "mdi:flash-triangle",
                    "off": "mdi:flash-triangle"
                }
        },
}

#SCHEMA_EXTEND = {
#	vol.Optional(CONF_NAME, default=""): cv.string,
#	vol.Optional(CONF_STACK, default="0"): cv.string,
#}
#for key in SM_NUMBER_MAP:
#    SCHEMA_EXTEND[vol.Optional(key, default="-1")] = cv.string
#PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(SCHEMA_EXTEND)

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    # We want this platform to be setup via discovery
    if discovery_info == None:
        return
    sensor_type = -1
    channel = -1
    for key in SM_NUMBER_MAP:
        val = config.get(key)
        if val != "-1":
            if sensor_type != -1:
                # ALREADY SET RAISE ERROR
                pass
            sensor_type = key
            channel = val
    if sensor_type != -1:
        # NO SWITCH TYPE FOUND, AMBIGUOUS, ERROR
        pass
    add_devices([Sensor(
		name=config.get(CONF_NAME),
        stack=config.get(CONF_STACK) or "0",
        type=sensor_type,
        chan=channel
	)])

class Sensor(SensorEntity):
    """Sequent Microsystems Multiio Sensor"""
    def __init__(self, name, stack, type, chan):
        if name == "":
            name = NAME_PREFIX + "_" + type + chan
        self._name = name
        self._stack = int(stack)
        self._type = type
        self._chan = int(chan)
        self._SM = SMmultiio.SMmultiio(self._stack)
        # Altering class so all functions have the same format
        com = SM_NUMBER_MAP[self._type]["com"]
        self._short_timeout = .05
        self._icons = SM_NUMBER_MAP[self._type]["icon"]
        self._icon = self._icons["off"]
        self._uom = SM_NUMBER_MAP[self._type]["uom"]
        self._value = 0
        self._SM_get = getattr(self._SM, com["get"])
        if len(signature(self._SM_get).parameters) == 0:
            def _aux_SM_get(self, _):
                return getattr(self, com["get"])()
            self._SM_get = types.MethodType(_aux_SM_get, self._SM)

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
    def native_value(self):
        return self._value
