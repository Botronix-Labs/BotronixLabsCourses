
"""
ble_tank_server.py

Implements a BLE UART server for controlling a tank robot using MicroPython BLE APIs.
Handles BLE advertising, connection management, and message reception/notification.
Designed for use on MicroPython devices (e.g., Raspberry Pi Pico W).
"""

import bluetooth
from ble_advertising import advertising_payload
from micropython import const


# Nordic UART Service UUIDs for BLE communication
_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_CHAR = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE)
_UART_TX_CHAR = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY)
_UART_SERVICE = (_UART_SERVICE_UUID, (_UART_TX_CHAR, _UART_RX_CHAR))


class BLETankServer:
    """
    BLE UART server for tank robot control.

    Args:
        ble (bluetooth.BLE): BLE instance from MicroPython.
        on_rx_callback (callable): Function to call when data is received.
    """
    def __init__(self, ble, on_rx_callback):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._connections = set()         # Track active connections
        self._rx_buffer = bytearray()     # Buffer for received data
        self._on_rx = on_rx_callback      # Callback for received data
        # Register UART service and get handles for TX/RX characteristics
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((_UART_SERVICE,))
        # Build advertising payload with device name
        self._payload = advertising_payload(name="PicoTank")
        self._advertise()

    def _irq(self, event, data):
        """
        Internal IRQ handler for BLE events.
        Handles connection, disconnection, and write events.
        """
        if event == 1:  # CONNECT
            conn_handle, _, _ = data
            print(f"✅ Connected: {conn_handle}")
            self._connections.add(conn_handle)
        elif event == 2:  # DISCONNECT
            conn_handle, _, _ = data
            print(f"🔌 Disconnected: {conn_handle}")
            self._connections.discard(conn_handle)
            self._advertise()
        elif event == 3:  # WRITE
            conn_handle, attr_handle = data
            if attr_handle == self._rx_handle:
                msg = self._ble.gatts_read(self._rx_handle)
                print(f"📨 Received: {msg}")
                if self._on_rx:
                    self._on_rx(msg.decode().strip())

    def send(self, data):
        """
        Send data to all connected BLE clients via the TX characteristic.

        Args:
            data (bytes/str): Data to send.
        """
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx_handle, data)

    def _advertise(self):
        """
        Start BLE advertising with the constructed payload.
        Attempts to parse and print the advertised device name.
        """
        adv_name = "<Unknown>"
        try:
            # BLE type for Complete Local Name is 0x09
            i = 0
            while i < len(self._payload):
                length = self._payload[i]
                type_ = self._payload[i + 1]
                if type_ == 0x09:
                    adv_name = self._payload[i + 2:i + 1 + length].decode("utf-8")
                    break
                i += 1 + length
        except Exception as e:
            print("⚠️ Failed to parse advertising name:", e)

        print(f"📢 Advertising as: {adv_name}")
        self._ble.gap_advertise(500_000, adv_data=self._payload)

