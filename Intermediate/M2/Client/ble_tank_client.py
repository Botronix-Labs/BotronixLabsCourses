"""
ble_tank_client.py

Implements a BLE (Bluetooth Low Energy) client for connecting to and controlling a PicoTank robot.
Handles BLE scanning, connection, service/characteristic discovery, and sending commands.
"""

import bluetooth
import time
from micropython import const

# BLE IRQ event constants
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)

# UART service and characteristic UUIDs for PicoTank BLE
_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_CHAR = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

class BLETankClient:
    """
    BLE client for connecting to and controlling a PicoTank robot.
    Handles scanning, connecting, service/characteristic discovery, and sending commands.
    """
    def __init__(self):
        """
        Initialize the BLETankClient instance.
        Sets up BLE, IRQ, and initial connection parameters.
        """
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.conn_handle = None
        self.tx_handle = None
        self.connected = False
        self.ble.irq(self._irq)
        self.target_name = "PicoTank"
        self._found_device = False
        self.on_rx = None
    
    def _irq(self, event, data):
        """
        Internal BLE IRQ handler for all BLE events.
        Handles scanning, connecting, service/characteristic discovery, notifications, etc.
        
        Args:
            event (int): The IRQ event type
            data (tuple): The event data
        """
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, _, _, adv_data = data
            print("Raw adv_data:", adv_data)  # Debug print to show raw advertisement data
            name = self.decode_name(adv_data)
            print("🔍 Found device:", repr(name))
            if name == self.target_name:
                print("Found target, connecting...")
                self.ble.gap_connect(addr_type, addr)
                self.ble.gap_scan(None)
        elif event == _IRQ_SCAN_DONE:
            print("Scan complete.")
        elif event == _IRQ_PERIPHERAL_CONNECT:
            conn_handle, _, _ = data
            print("Connected.")
            self.conn_handle = conn_handle
            self.connected = True
            self.ble.gattc_discover_services(conn_handle)
        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            print("Disconnected.")
            self.connected = False
        elif event == _IRQ_GATTC_SERVICE_RESULT:
            conn_handle, start, end, uuid = data
            if uuid == _UART_SERVICE_UUID:
                self.service_start = start
                self.service_end = end
        elif event == _IRQ_GATTC_SERVICE_DONE:
            self.ble.gattc_discover_characteristics(self.conn_handle, self.service_start, self.service_end)
        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            conn_handle, def_handle, value_handle, properties, uuid = data
            if uuid == _UART_RX_UUID:
                self.tx_handle = value_handle
        elif event == _IRQ_GATTC_NOTIFY:
            conn_handle, value_handle, notify_data = data
            if self.on_rx:
                self.on_rx(bytes(notify_data).decode("utf-8"))
        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            print("Ready to send BLE commands.")
    
    def decode_name(self, adv_data):
        """
        Decode the device name from BLE advertisement data.
        
        Args:
            adv_data (bytes): Advertisement data
            
        Returns:
            str or None: Decoded device name, or None if not found
        """
        try:
            i = 0
            adv_data = bytes(adv_data)  # convert memoryview to bytes first
            while i < len(adv_data):
                length = adv_data[i]
                if length == 0:
                    break
                type_ = adv_data[i + 1]
                if type_ == 0x09:  # Complete Local Name
                    return adv_data[i + 2:i + 1 + length].decode("utf-8")
                i += 1 + length
        except Exception as e:
            print("decode_name error:", e)
        return None

    def connect(self):
        """
        Start scanning for BLE devices and connect to the target device.
        """
        print("Scanning...")
        self.ble.gap_scan(5000, 30000, 30000)

    def send_command(self, cmd):
        """
        Send a command string to the connected BLE device.
        
        Args:
            cmd (str): Command to send
        """
        if self.connected and self.tx_handle:
            self.ble.gattc_write(self.conn_handle, self.tx_handle, cmd.encode(), 1)
