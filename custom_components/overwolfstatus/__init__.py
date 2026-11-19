from json import JSONDecodeError

from aiohttp import web

from homeassistant.components.webhook import async_register, async_unregister
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_WEBHOOK_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN, EVENT_NAME, TITLE


async def handle_webhook(
    hass: HomeAssistant, webhook_id: str, request: web.Request
) -> web.Response:
    """Forward a validated batch as individual Home Assistant events."""
    try:
        data = await request.json()
    except JSONDecodeError, UnicodeDecodeError:
        return web.Response(text="Failed to parse payload", status=400)
    except web.HTTPException as error:
        # Home Assistant's webhook dispatcher turns raised exceptions into HTTP 200.
        return web.Response(text=error.reason, status=error.status)

    if not isinstance(data, list) or not all(isinstance(event, dict) for event in data):
        return web.Response(text="Payload must be a JSON array of objects", status=400)

    for event in data:
        hass.bus.async_fire(EVENT_NAME, event)
    return web.Response(text="OK")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configure based on config entry."""
    async_register(
        hass,
        DOMAIN,
        TITLE,
        entry.data[CONF_WEBHOOK_ID],
        handle_webhook,
        # Nabu Casa cloudhooks must be able to reach this endpoint.
        local_only=False,
        allowed_methods=("POST",),
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    async_unregister(
        hass,
        entry.data[CONF_WEBHOOK_ID],
    )
    return True


async_remove_entry = config_entry_flow.webhook_async_remove_entry
