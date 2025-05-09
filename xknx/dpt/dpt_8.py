"""
Implementation of Basic KNX 2-Byte Signed Values.

They correspond the following KNX DPTs:
    8.*** 2-byte/octet signed (2's complement), i.e. percentV16, delta time
"""

from __future__ import annotations

import struct

from xknx.exceptions import ConversionError

from .dpt import DPTNumeric
from .payload import DPTArray, DPTBinary


class DPT2ByteSigned(DPTNumeric):
    """
    Abstraction for KNX 2 Byte signed values.

    DPT 8.***
    """

    dpt_main_number = 8
    dpt_sub_number: int | None = None
    value_type = "2byte_signed"
    payload_length = 2

    value_min = -32768
    value_max = 32767
    resolution: int | float = 1

    # not using DPTStructIntMixin because return type of from_knx can be float when resolution is < 1
    _struct_format = ">h"

    @classmethod
    def from_knx(cls, payload: DPTArray | DPTBinary) -> int | float:
        """Parse/deserialize from KNX/IP raw data."""
        raw = cls.validate_payload(payload)

        try:
            return struct.unpack(cls._struct_format, bytes(raw))[0] * cls.resolution  # type: ignore[no-any-return]
        except struct.error as err:
            raise ConversionError(f"Could not parse {cls.dpt_name()}", raw=raw) from err

    @classmethod
    def to_knx(cls, value: int | float) -> DPTArray:
        """Serialize to KNX/IP raw data."""
        try:
            knx_value = int(float(value) / cls.resolution)
            if not (cls.value_min <= knx_value <= cls.value_max):
                raise ValueError("Value out of range")
            return DPTArray(struct.pack(cls._struct_format, knx_value))
        except (ValueError, struct.error) as err:
            raise ConversionError(
                f"Could not serialize {cls.dpt_name()}", value=value
            ) from err


class DPTValue2Count(DPT2ByteSigned):
    """DPT 8.001 DPT_Value_2_Count (pulses)."""

    dpt_main_number = 8
    dpt_sub_number = 1
    value_type = "pulse_2byte_signed"
    unit = "pulses"


class DPTDeltaTimeMsec(DPT2ByteSigned):
    """DPT 8.002 DPT_DeltaTimeMsec (ms)."""

    dpt_main_number = 8
    dpt_sub_number = 2
    value_type = "delta_time_ms"
    unit = "ms"


class DPTDeltaTime10Msec(DPT2ByteSigned):
    """DPT 8.003 DPT_DeltaTime10Msec (ms)."""

    dpt_main_number = 8
    dpt_sub_number = 3
    value_type = "delta_time_10ms"
    resolution = 10
    unit = "ms"


class DPTDeltaTime100Msec(DPT2ByteSigned):
    """DPT 8.004 DPT_DeltaTime100Msec (ms)."""

    dpt_main_number = 8
    dpt_sub_number = 4
    value_type = "delta_time_100ms"
    resolution = 100
    unit = "ms"


class DPTDeltaTimeSec(DPT2ByteSigned):
    """DPT 8.005 DPT_DeltaTimeSec (s)."""

    dpt_main_number = 8
    dpt_sub_number = 5
    value_type = "delta_time_sec"
    unit = "s"


class DPTDeltaTimeMin(DPT2ByteSigned):
    """DPT 8.006 DPT_DeltaTimeMin (min)."""

    dpt_main_number = 8
    dpt_sub_number = 6
    value_type = "delta_time_min"
    unit = "min"


class DPTDeltaTimeHrs(DPT2ByteSigned):
    """DPT 8.007 DPT_DeltaTimeHrs (h)."""

    dpt_main_number = 8
    dpt_sub_number = 7
    value_type = "delta_time_hrs"
    unit = "h"


class DPTPercentV16(DPT2ByteSigned):
    """DPT 8.010 DPT_Percent_V16 (%)."""

    dpt_main_number = 8
    dpt_sub_number = 10
    value_type = "percentV16"
    resolution = 0.01
    unit = "%"


class DPTRotationAngle(DPT2ByteSigned):
    """DPT 8.011 DPT_Rotation_Angle (°)."""

    dpt_main_number = 8
    dpt_sub_number = 11
    value_type = "rotation_angle"
    unit = "°"


class DPTLengthM(DPT2ByteSigned):
    """DPT 8.012 DPT_Length_m."""

    dpt_main_number = 8
    dpt_sub_number = 12
    value_type = "length_m"
    unit = "m"
    ha_device_class = "distance"
