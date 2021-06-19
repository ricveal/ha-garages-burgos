"""Binary Sensor platform for Garages Burgos."""
from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_OCCUPANCY,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from . import get_coordinator
from .const import ATTRIBUTION

BINARY_SENSORS = {
    "state",
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Defer sensor setup to the shared sensor module."""
    coordinator = await get_coordinator(hass)

    async_add_entities(
        GaragesburgosBinarySensor(
            coordinator, config_entry.data["name"], info_type
        )
        for info_type in BINARY_SENSORS
    )


class GaragesburgosBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary Sensor representing garages Burgos data."""

    def __init__(
        self, coordinator: DataUpdateCoordinator, name: str, info_type: str
    ) -> None:
        """Initialize garages Burgos binary sensor."""
        super().__init__(coordinator)
        self._unique_id = f"{name}-{info_type}"
        self._info_type = info_type
        self._name = name

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return the unique id of the device."""
        return self._unique_id

    @property
    def is_on(self) -> bool:
        """If the binary sensor is currently on or off."""
        return (
            getattr(self.coordinator.data[self._name], self._info_type) != "Available"
        )

    @property
    def device_class(self) -> str:
        """Return the class of the binary sensor."""
        return DEVICE_CLASS_OCCUPANCY

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return device attributes."""
        return {ATTR_ATTRIBUTION: ATTRIBUTION}
