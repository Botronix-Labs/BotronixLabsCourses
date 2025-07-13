

"""
ble_advertising.py

Utility functions for creating BLE advertising payloads for MicroPython BLE applications.
Provides a function to build advertising payloads with device name and service UUIDs.

This module is designed for use on MicroPython devices with BLE support (e.g., Raspberry Pi Pico W).
It provides a helper function to construct advertising payloads for BLE services, including device name and service UUIDs.
"""


# Import MicroPython constants and struct for byte packing
from micropython import const
import struct


# Advertisement types (see Bluetooth Core Specification)
_ADV_TYPE_FLAGS = const(0x01)              # Flags field
_ADV_TYPE_NAME = const(0x09)               # Complete local name
_ADV_TYPE_UUID16_COMPLETE = const(0x03)    # Complete list of 16-bit Service Class UUIDs
_ADV_TYPE_UUID32_COMPLETE = const(0x05)    # Complete list of 32-bit Service Class UUIDs
_ADV_TYPE_UUID128_COMPLETE = const(0x07)   # Complete list of 128-bit Service Class UUIDs


def advertising_payload(limited_disc=False, br_edr=False, name=None, services=None):
    """
    Build a BLE advertising payload for MicroPython BLE applications.

    Args:
        limited_disc (bool): If True, sets the device to limited discoverable mode.
        br_edr (bool): If True, indicates BR/EDR support (not used in MicroPython BLE).
        name (str): Device name to advertise (optional).
        services (list): List of UUID objects to advertise (optional).

    Returns:
        bytearray: The constructed BLE advertising payload.

    This function creates a payload that can be used with BLE advertising APIs.
    It includes flags, device name, and service UUIDs as appropriate.
    """
    payload = bytearray()

    # Add Flags field (required for BLE advertising)
    # 0x02: LE Limited Discoverable Mode, 0x06: LE General Discoverable Mode
    flags = 0x02 if limited_disc else 0x06
    payload += struct.pack("BB", 2, _ADV_TYPE_FLAGS)  # Length, Type
    payload += struct.pack("B", flags)                # Value

    # Add Complete Local Name (if provided)
    if name:
        name_bytes = name.encode()
        payload += struct.pack("BB", len(name_bytes) + 1, _ADV_TYPE_NAME)  # Length, Type
        payload += name_bytes

    # Add Service UUIDs (if provided)
    if services:
        for uuid in services:
            b = bytes(uuid)
            # Determine UUID length and use appropriate advertisement type
            if len(b) == 2:
                # 16-bit UUID
                payload += struct.pack("BB", len(b) + 1, _ADV_TYPE_UUID16_COMPLETE) + b
            elif len(b) == 4:
                # 32-bit UUID
                payload += struct.pack("BB", len(b) + 1, _ADV_TYPE_UUID32_COMPLETE) + b
            elif len(b) == 16:
                # 128-bit UUID
                payload += struct.pack("BB", len(b) + 1, _ADV_TYPE_UUID128_COMPLETE) + b
            # If UUID length is not standard, it is ignored

    return payload  # Return the constructed advertising payload
