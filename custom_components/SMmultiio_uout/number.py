import voluptuous as vol
import multiio as SMmultiio
import logging

from homeassistant.const import (
	CONF_NAME, CONF_PORT, CONF_VALUE_TEMPLATE
)

from homeassistant.components.light import PLATFORM_SCHEMA
from homeassistant.components.number import NumberEntity
import homeassistant.helpers.config_validation as cv

CONF_STACK = "stack"
CONF_CHAN = "chan"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_CHAN): cv.string,
	vol.Optional(CONF_NAME, default='uout'): cv.string,
	vol.Optional(CONF_STACK, default=0): cv.string,
})

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
	"""Setup Multiio output"""
	add_devices([Output(
		name=config.get(CONF_NAME),
        stack=config.get(CONF_STACK),
        chan=config.get(CONF_CHAN),
	)])

class Output(NumberEntity):
    """Sequent Microsystems Home Automation Open Drain"""
    def __init__(self, name, stack, chan):
        self._name = name
        self._stack = int(stack)
        self._chan = int(chan)
        self._SM = SMmultiio.SMmultiio(self._stack)
    @property
    def name(self):
        """Return the name of the switch"""
        return self._name
    @property
    def native_unit_of_measurement(self):
        return "V"
    @property
    def native_step(self):
        return 0.01
    @property
    def native_max_value(self):
        return 10.0
    @property
    def native_value(self):
        try:
            return self._SM.get_u_out(self._chan)
        except Exception as ex:
            _LOGGER.error("Multiio output error %e", ex)

    def set_native_value(self, value):
        try:
            self._SM.set_u_out(self._chan, value)
        except Exception as ex:
            _LOGGER.error("Multiio output error %e", ex)
