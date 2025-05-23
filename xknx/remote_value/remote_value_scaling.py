"""
Module for managing a Scaling remote value.

DPT 5.001.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from xknx.dpt import DPTArray, DPTBinary
from xknx.exceptions import CouldNotParseTelegram

from .remote_value import GroupAddressesType, RemoteValue, RVCallbackType

if TYPE_CHECKING:
    from xknx.xknx import XKNX


class RemoteValueScaling(RemoteValue[int]):
    """Abstraction for remote value of KNX DPT 5.001 (DPT_Scaling)."""

    def __init__(
        self,
        xknx: XKNX,
        group_address: GroupAddressesType = None,
        group_address_state: GroupAddressesType = None,
        sync_state: bool | int | float | str = True,
        device_name: str | None = None,
        feature_name: str = "Value",
        after_update_cb: RVCallbackType[int] | None = None,
        range_from: int = 0,
        range_to: int = 100,
    ) -> None:
        """Initialize remote value of KNX DPT 5.001 (DPT_Scaling)."""
        super().__init__(
            xknx,
            group_address,
            group_address_state,
            sync_state=sync_state,
            device_name=device_name,
            feature_name=feature_name,
            after_update_cb=after_update_cb,
        )
        self.range_from = range_from
        self.range_to = range_to

    def to_knx(self, value: float) -> DPTArray:
        """Convert value to payload."""
        knx_value = self._calc_to_knx(self.range_from, self.range_to, value)
        return DPTArray(knx_value)

    def from_knx(self, payload: DPTArray | DPTBinary) -> int:
        """Convert current payload to value."""
        if isinstance(payload, DPTArray) and len(payload.value) == 1:
            return self._calc_from_knx(self.range_from, self.range_to, payload.value[0])
        raise CouldNotParseTelegram("Payload invalid", payload=str(payload))

    @property
    def unit_of_measurement(self) -> str | None:
        """Return the unit of measurement."""
        return "%"

    @staticmethod
    def _calc_from_knx(range_from: int, range_to: int, raw: int) -> int:
        delta = range_to - range_from
        return round((raw / 255) * delta) + range_from

    @staticmethod
    def _calc_to_knx(range_from: int, range_to: int, value: float) -> int:
        delta = range_to - range_from
        return round((value - range_from) / delta * 255)
