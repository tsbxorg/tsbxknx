"""Package for convenience functions for KNX group communication."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from xknx.core.value_reader import ValueReader
from xknx.dpt import DPTArray, DPTBase, DPTBinary
from xknx.telegram import Telegram
from xknx.telegram.address import DeviceAddressableType, parse_device_group_address
from xknx.telegram.apci import GroupValueRead, GroupValueResponse, GroupValueWrite
from xknx.typing import DPTParsable

if TYPE_CHECKING:
    from xknx.xknx import XKNX
logger = logging.getLogger("xknx.tools")


def group_value_read(
    xknx: XKNX,
    group_address: DeviceAddressableType,
) -> None:
    """Send a GroupValueRead telegram."""
    telegram = Telegram(
        destination_address=parse_device_group_address(group_address),
        payload=GroupValueRead(),
    )

    logger.debug("Sending GroupValueRead telegram to %s", group_address)
    xknx.telegrams.put_nowait(telegram)


def group_value_response(
    xknx: XKNX,
    group_address: DeviceAddressableType,
    value: Any,
    value_type: DPTParsable | type[DPTBase] | None = None,
) -> None:
    """Send a GroupValueResponse telegram."""
    payload = _parse_payload(value, value_type)
    telegram = Telegram(
        destination_address=parse_device_group_address(group_address),
        payload=GroupValueResponse(payload),
    )
    logger.debug(
        "Sending GroupValueResponse telegram with value '%s' of type '%s' to %s.",
        value,
        value_type or "raw",
        group_address,
    )
    xknx.telegrams.put_nowait(telegram)


def group_value_write(
    xknx: XKNX,
    group_address: DeviceAddressableType,
    value: Any,
    value_type: DPTParsable | type[DPTBase] | None = None,
) -> None:
    """Send a GroupValueWrite telegram."""
    payload = _parse_payload(value, value_type)
    telegram = Telegram(
        destination_address=parse_device_group_address(group_address),
        payload=GroupValueWrite(payload),
    )
    logger.debug(
        "Sending GroupValueWrite telegram with value '%s' of type '%s' to %s.",
        value,
        value_type or "raw",
        group_address,
    )
    xknx.telegrams.put_nowait(telegram)


async def read_group_value(
    xknx: XKNX,
    group_address: DeviceAddressableType,
    value_type: DPTParsable | type[DPTBase] | None = None,
) -> int | tuple[int, ...] | Any | None:
    """Read a value from a KNX group address."""
    transcoder = _parse_dpt(value_type)
    value_reader = ValueReader(xknx, parse_device_group_address(group_address))
    response = await value_reader.read()
    if response is not None:
        assert isinstance(response.payload, GroupValueWrite | GroupValueResponse)
        if transcoder is not None:
            return transcoder.from_knx(response.payload.value)
        return response.payload.value.value
    return None


def _parse_dpt(value_type: DPTParsable | type[DPTBase] | None) -> type[DPTBase] | None:
    if value_type is None:
        return None
    return DPTBase.get_dpt(value_type)


def _parse_payload(
    value: Any,
    value_type: DPTParsable | type[DPTBase] | None = None,
) -> DPTBinary | DPTArray:
    if isinstance(value, DPTArray | DPTBinary):
        return value
    if transcoder := _parse_dpt(value_type):
        return transcoder.to_knx(value)
    if isinstance(value, int):
        return DPTBinary(value)
    return DPTArray(value)
