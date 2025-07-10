
"""
ble_tank_server.py

Implements BLE server for tank robot. Handles BLE communication, command reception, and status notification.
"""

import bluetooth
from ble_advertising import advertising_payload
from micropython import const

# BLE UART service and characteristic UUIDs
_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_CHAR = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE)
_UART_TX_CHAR = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY)
_UART_SERVICE = (_UART_SERVICE_UUID, (_UART_TX_CHAR, _UART_RX_CHAR))

class BLETankServer:
    """
    BLE server for the tank robot. Handles BLE events, command reception, and status notification.
    """
    def __init__(self, ble, on_rx_callback):
        """
        Initialize BLE, register UART service, and start advertising.
        Args:
            ble: bluetooth.BLE instance
            on_rx_callback: function to call when data is received
        """
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._connections = set()
        self._rx_buffer = bytearray()
        self._on_rx = on_rx_callback
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._payload = advertising_payload(name="PicoTank")
        self._advertise()

    def _irq(self, event, data):
        """
        BLE IRQ event handler. Handles connection, disconnection, and write events.
        Args:
            event (int): BLE event code
            data (tuple): Event data
        """
        if event == 1:  # CONNECT
            conn_handle, _, _ = data
            print(f"[BLE] Connected: {conn_handle}")
            self._connections.add(conn_handle)
        elif event == 2:  # DISCONNECT
            conn_handle, _, _ = data
            print(f"[BLE] Disconnected: {conn_handle}")
            self._connections.discard(conn_handle)
            self._advertise()
        elif event == 3:  # WRITE
            conn_handle, attr_handle = data
            if attr_handle == self._rx_handle:
                msg = self._ble.gatts_read(self._rx_handle)
                print(f"[BLE] Received: {msg}")
                if self._on_rx:
                    self._on_rx(msg.decode().strip())

    def send(self, data):
        """
        Send a status message to all connected BLE clients.
        Args:
            data (str): Status message to send
        """
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx_handle, data)

    def _advertise(self):
        """
        Start BLE advertising with the device name.
        """
        # Try to decode the advertised name from the payload
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
            print("[BLE] Failed to parse advertising name:", e)

        print(f"[BLE] Advertising as: {adv_name}")
        self._ble.gap_advertise(500_000, adv_data=self._payload)

