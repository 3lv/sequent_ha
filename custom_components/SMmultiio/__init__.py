"""Sequent Microsystems Multiio Integration"""

import voluptuous as vol

DOMAIN = "SMmultiio"

CONFIG_SCHEMA = vol.Schema({
})

def setup(hass, config):
    hass.data[DOMAIN] = {
            "common_data": 100
    }
    hass.helpers.discovery.load_platform("sensor", DOMAIN, {}, config)
    return True
