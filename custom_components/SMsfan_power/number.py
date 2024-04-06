import voluptuous as vol
import SMsfan
import logging

from homeassistant.const import (
	CONF_NAME, CONF_PORT, CONF_VALUE_TEMPLATE
)

from homeassistant.components.light import PLATFORM_SCHEMA
from homeassistant.components.number import NumberEntity
import homeassistant.helpers.config_validation as cv

CONF_STACK="stack"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
	vol.Optional(CONF_NAME, default='od'): cv.string,
	vol.Optional(CONF_STACK, default=0): cv.string,
})

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
	"""Setup Smart Fan Power"""
	add_devices([Power(
		name=config.get(CONF_NAME),
        stack=config.get(CONF_STACK),
	)])

class Power(NumberEntity):
    """Sequent Microsystems Home Automation Open Drain"""
    def __init__(self, name, stack):
        self._name = name
        self._stack = int(stack)
    @property
    def name(self):
        """Return the name of the switch"""
        return self._name
    @property
    def native_step(self):
        return float(1)
    @property
    def native_value(self):
        try:
            return SMsfan.getPower(self._stack)
        except Exception as ex:
            _LOGGER.error("Fan error %e", ex)

    def set_native_value(self, value):
        try:
            SMsfan.setPower(self._stack, value)
        except Exception as ex:
            _LOGGER.error("Fan error %e", ex)
