import voluptuous as vol
import libioplus
SMioplus = libioplus
import logging

from homeassistant.const import (
	CONF_NAME
)

from homeassistant.components.light import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import SwitchEntity

CONF_STACK = "stack"
CONF_CHAN = "chan"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
	vol.Required(CONF_CHAN): cv.string,
	vol.Optional(CONF_NAME, default='relay'): cv.string,
	vol.Optional(CONF_STACK, default=0): cv.string,
})

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
	"""Setup the Home Automation relay switches"""
	add_devices([Relay(
		name=config.get(CONF_NAME),
        stack=config.get(CONF_STACK),
        chan=config.get(CONF_CHAN)
	)])

class Relay(SwitchEntity):
    """Sequent Microsystems Home Automation Relay Switch"""
    def __init__(self, name, stack, chan):
        self._name = name
        self._stack = int(stack)
        self._chan = int(chan)
    @property
    def name(self):
        """Return the name of the switch"""
        return self._name

    @property
    def is_on(self):
        """Return true if relay is on."""
        try:
            if SMioplus.getRelayCh(self._stack, self._chan) == 0:
                return False
            else:
                return True
        except Exception as ex:
            _LOGGER.error("Relay is_on() check failed, %e", ex)
            return False

    def turn_on(self, **kwargs):
        """Turn the relay on."""
        try:
            SMioplus.setRelayCh(self._stack, self._chan, 1)
        except Exception as ex:
            _LOGGER.error("Relay turn ON failed, %e", ex)

    def turn_off(self, **kwargs):
        """Turn the relay off."""
        try:
            SMioplus.setRelayCh(self._stack, self._chan, 0)
        except Exception as ex:
            _LOGGER.error("Relay turn OFF failed, %e", ex);
