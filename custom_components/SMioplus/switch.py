import voluptuous as vol
import libioplus
SMioplus = libioplus
import logging

from homeassistant.const import (
	CONF_NAME, CONF_PORT, CONF_VALUE_TEMPLATE
)

from homeassistant.components.light import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import SwitchEntity

CONF_RELAY="relay"
CONF_STACK="stack"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
	vol.Required(CONF_RELAY): cv.string,
#    vol.Optional(CONF_VALUE_TEMPLATE): cv.template,
	vol.Optional(CONF_PORT, default='0x3F'): cv.string,
	vol.Optional(CONF_NAME, default='relay'): cv.string,
	vol.Optional(CONF_STACK, default=0): cv.string,
})

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
	"""Setup the 8relay platform."""
	add_devices([Relay(
		port=config.get(CONF_PORT),
#        value_template = config.get(CONF_VALUE_TEMPLATE),
		name=config.get(CONF_NAME),
        stack=config.get(CONF_STACK),
        relay=config.get(CONF_RELAY)
	)])

class Relay(SwitchEntity):
    """Sequent Microsystems Home Automation"""
    def __init__(self, port, name, stack, relay):
        self._port = int(port, 16)
        self._name = name
        self._relay = int(relay)
        self._stack = int(stack)
    @property
    def name(self):
        """Return the name of the switch"""
        return self._name

    @property
    def is_on(self):
        """Return true if relay is on."""
        try:
            if SMioplus.getRelayCh(self._stack, self._relay) == 0:
                return False
            else:
                return True
        except Exception as ex:
            _LOGGER.error("Relay is_on() check failed, %e", ex)
            return False

    def turn_on(self, **kwargs):
        """Turn the relay on."""
        try:
            SMioplus.setRelayCh(self._stack, self._relay, 1)
        except Exception as ex:
            _LOGGER.error("Relay turn ON failed, %e", ex)

    def turn_off(self, **kwargs):
        """Turn the relay off."""
        try:
            SMioplus.setRelayCh(self._stack, self._relay, 0)
        except Exception as ex:
            _LOGGER.error("Relay turn OFF failed, %e", ex);
