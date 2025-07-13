"""
ble_controller_client.py

Implements BLEControllerClient class for connecting to PicoTank and PicoArm BLE servers.
Handles scanning, connecting, service/characteristic discovery, and command sending.
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

class BLEControllerClient:
    """
    BLE client for connecting to PicoTank and PicoArm BLE servers.
    Handles scanning, connecting, service/characteristic discovery, and command sending.
    """
    def __init__(self):
        """
        Initialize BLE client and set up target device UUIDs.
        """
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self._irq)

        self.conn_handle = None
        self.tx_handle = None
        self.rx_handle = None
        self.connected = False

        # Target device name and UUID mappings
        self.target_name = "PicoTank"  # default
        self.target_uuids = None
        self.service_start = None
        self.service_end = None

        self.service_uuids = {
            "PicoTank": {
                "service": bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E"),
                "rx": bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
                "tx": bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
            },
            "PicoArm": {
                "service": bluetooth.UUID("7E400001-B5A3-F393-E0A9-E50E24DCCA9E"),
                "rx": bluetooth.UUID("7E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
                "tx": bluetooth.UUID("7E400003-B5A3-F393-E0A9-E50E24DCCA9E")
            }
        }

        self.switch_target(self.target_name)

    def switch_target(self, name):
        """
        Switch BLE target and update UUIDs.
        Args:
            name (str): Target device name ("PicoTank" or "PicoArm")
        """
        self.target_name = name
        self.target_uuids = self.service_uuids.get(name)
        if self.target_uuids:
            print(f"🎯 Switched target to: {name}")
        else:
            print(f"⚠️ Unknown target: {name}")

    def _irq(self, event, data):
        """
        BLE IRQ event handler. Handles scan, connect, service/characteristic discovery, and notifications.
        Args:
            event (int): BLE event code
            data (tuple): Event data
        """
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, _, _, adv_data = data
            name = self.decode_name(adv_data)
            print("🔍 Found device:", repr(name))
            if name == self.target_name:
                print("✅ Target found. Connecting...")
                self.ble.gap_connect(addr_type, addr)
                self.ble.gap_scan(None)

        elif event == _IRQ_SCAN_DONE:
            print("🔎 Scan complete.")

        elif event == _IRQ_PERIPHERAL_CONNECT:
            conn_handle, _, _ = data
            self.conn_handle = conn_handle
            self.connected = True
            print("🔗 Connected.")
            self.ble.gattc_discover_services(conn_handle)

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            print("❌ Disconnected.")
            self.connected = False
            self.conn_handle = None
            self.tx_handle = None
            self.rx_handle = None

        elif event == _IRQ_GATTC_SERVICE_RESULT:
            conn_handle, start, end, uuid = data
            if uuid == self.target_uuids["service"]:
                self.service_start = start
                self.service_end = end

        elif event == _IRQ_GATTC_SERVICE_DONE:
            if self.service_start and self.service_end:
                self.ble.gattc_discover_characteristics(
                    self.conn_handle, self.service_start, self.service_end
                )

        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            conn_handle, def_handle, value_handle, properties, uuid = data
            if uuid == self.target_uuids["rx"]:
                self.tx_handle = value_handle
            elif uuid == self.target_uuids["tx"]:
                self.rx_handle = value_handle

        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            print("📡 Characteristics discovered. Ready to send commands.")

        elif event == _IRQ_GATTC_NOTIFY:
            conn_handle, value_handle, notify_data = data
            msg = notify_data.decode().strip()
            print(f"📩 Received notification: {msg}")
            if self.on_rx:
                self.on_rx(msg)

    def decode_name(self, adv_data):
        try:
            i = 0
            adv_data = bytes(adv_data)
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
        if self.target_name:
            print(f"🔍 Scanning for {self.target_name}...")
            self.ble.gap_scan(5000, 30000, 30000)

    def disconnect(self):
        if self.connected and self.conn_handle is not None:
            self.ble.gap_disconnect(self.conn_handle)

    def send_command(self, cmd):
        if self.connected and self.tx_handle:
            try:
                self.ble.gattc_write(
                    self.conn_handle, self.tx_handle, cmd.encode(), 1
                )
                print(f"➡️ Sent command: {cmd}")
                time.sleep(0.3)  # 300 ms delay
            except Exception as e:
                print(f"❌ Failed to send command: {e}")
        else:
            print("⚠️ Not connected or TX handle missing.")

    def set_rx_callback(self, callback):
        """Set a callback function to handle incoming notifications."""
        self.on_rx = callback
