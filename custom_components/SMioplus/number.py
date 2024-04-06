import voluptuous as vol
import libioplus
SMioplus = libioplus
import logging

from homeassistant.const import (
	CONF_NAME, CONF_PORT, CONF_VALUE_TEMPLATE
)

from homeassistant.components.light import PLATFORM_SCHEMA
from homeassistant.components.number import NumberEntity
import homeassistant.helpers.config_validation as cv

CONF_OD="od"
CONF_STACK="stack"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
	vol.Required(CONF_OD): cv.string,
#    vol.Optional(CONF_VALUE_TEMPLATE): cv.template,
	vol.Optional(CONF_PORT, default='0x3F'): cv.string,
	vol.Optional(CONF_NAME, default='od'): cv.string,
	vol.Optional(CONF_STACK, default=0): cv.string,
})

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
	"""Setup open drains"""
	add_devices([OpenDrain(
		port=config.get(CONF_PORT),
		name=config.get(CONF_NAME),
        stack=config.get(CONF_STACK),
        od=config.get(CONF_OD)
	)])

class OpenDrain(NumberEntity):
    """Sequent Microsystems Home Automation Open Drain"""
    def __init__(self, port, name, stack, od):
        self._port = int(port, 16)
        self._name = name
        self._stack = int(stack)
        self._native_value = int(0)
        self._od = int(od)
    @property
    def name(self):
        """Return the name of the switch"""
        return self._name
    @property
    def native_step(self):
        return float(0.01)
    @property
    def native_value(self):
        return self._native_value

    def set_native_value(self, value):
        try:
            SMioplus.setOdPwm(self._stack, self._od, value * 100)
            self._native_value = value
        except Exception as ex:
            _LOGGER.error("Od error");
