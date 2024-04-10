"""Sequent Microsystems Multiio Integration"""

DOMAIN = "SMmultiio"

def setup(hass, config):
    hass.data[DOMAIN] = {
            "common_data": 100
    }
    hass.helpers.discovery.load_platform("sensor", DOMAIN, {}, config)
    return True
